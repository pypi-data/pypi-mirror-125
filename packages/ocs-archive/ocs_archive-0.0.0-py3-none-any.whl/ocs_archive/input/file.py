from datetime import datetime, timedelta
from contextlib import contextmanager
import tarfile
import hashlib
import os
import io

from dateutil.parser import parse
from astropy import wcs, units
from astropy.coordinates import Angle
from astropy.io import fits

from ocs_archive.settings import settings
from ocs_archive.input.headerdata import HeaderData

from abc import ABC, abstractmethod


class FileSpecificationException(Exception):
    pass


class File:
    """
    Operates on an open file-like object to extract its extension and retreive its metadata
    """
    def __init__(self, fileobj, path=None):
        self.fileobj = fileobj
        self.path = path
        self.basename, self.extension = self.get_basename_and_extension(self.filename)

    def get_from_start(self):
        self.fileobj.seek(0)
        return self.fileobj

    def get_md5(self):
        return hashlib.md5(self.get_from_start().read()).hexdigest()

    def __len__(self):
        self.fileobj.seek(0, os.SEEK_END)
        length = self.fileobj.tell()
        self.fileobj.seek(0)
        return length

    @property
    def filename(self):
        # The filename, can be a full path or at least the basename plus the extension
        filename = None
        if self.path is not None:
            filename = self.path
        elif hasattr(self.fileobj, 'name'):
            filename = self.fileobj.name
        elif hasattr(self.fileobj, 'filename'):
            filename = self.fileobj.filename
        return filename

    @staticmethod
    def get_basename_and_extension(path):
        basename, extension = None, None
        if path is not None:
            filename = os.path.basename(path)
            if filename.find('.') > 0:
                basename = filename[:filename.index('.')]
                extension = filename[filename.index('.'):]
            else:
                basename = filename
                extension = ''
        return basename, extension


class EmptyFile(File):
    """
    Implements the file methods but has no open file, just the supplied filename
    """
    def __init__(self, path):
        super().__init__(io.BytesIO(b''), path=path)

    def get_md5(self):
        return hashlib.md5(self.filename).hexdigest()

    @property
    def filename(self):
        # The filename, can be a full path or at least the basename plus the extension
        filename = 'dummy_file.fits'
        if self.path is not None:
            filename = self.path
        return filename


class DataFile:
    """
    Base class for extracting metadata needed to store and filter data from an input file-like object.
    This class should be subclassed and methods overriden to support other input data formats in the archive.
    """
    def __init__(self, open_file: File, file_metadata: dict = {}, blacklist_headers: tuple = settings.HEADER_BLACKLIST, required_headers: tuple = settings.REQUIRED_HEADERS):
        self.open_file = open_file
        self.blacklist_headers = blacklist_headers
        self.required_headers = required_headers
        self._create_header_data(file_metadata)
        self._repair_observation_day()
        self._repair_public_date()

    def _create_header_data(self, file_metadata: dict):
        if self._is_valid_file_metadata(file_metadata):
            self.header_data = HeaderData(file_metadata)
            return
        # Missing one or more required headers in the input file_metadata
        raise FileSpecificationException('Could not find required keywords in headers!')

    def get_header_data(self):
        # This should return the header values you want to store in the archive.
        # For a fits file, this would be the dictionary of all header values
        return self.header_data

    def _repair_observation_day(self):
        """
        Set observation day from the headers of date
        :return: Day in YYYYMMDD format
        """
        if not self.header_data.get_observation_day():
            observation_date = self.header_data.get_observation_date()
            if observation_date:
                observation_day = observation_date.split('T')[0].replace('-', '')
                self.header_data.update_headers({settings.OBSERVATION_DAY_KEY: observation_day})

    def _repair_public_date(self):
        # Set the public date based on observation date. Should be overriden if you have another method
        # of specifying the public date in your file type
        if not self.header_data.get_public_date():
            if (self.header_data.get_configuration_type() in settings.CALIBRATION_TYPES or
                    (self.header_data.get_proposal_id() and any([prop in self.header_data.get_proposal_id() for prop in settings.PUBLIC_PROPOSALS]))):
                public_date = self.header_data.get_observation_date()
            elif ((self.header_data.get_proposal_id() and any([prop in self.header_data.get_proposal_id() for prop in settings.PRIVATE_PROPOSALS])) or
                    any([chars in self.open_file.basename for chars in settings.PRIVATE_FILE_TYPES])):
                # This should be private, set it to 999 years from observation date
                public_date = (parse(self.header_data.get_observation_date()) + timedelta(days=365 * 999)).isoformat()
            else:
                # This should be proprietary, set it to X days from observation date
                public_date = (parse(self.header_data.get_observation_date()) + timedelta(days=settings.DAYS_UNTIL_PUBLIC)).isoformat()
            self.header_data.update_headers({settings.PUBLIC_DATE_KEY: public_date})

    def _is_valid_file_metadata(self, metadata_dict: dict):
        """
        Check some file metadata for required headers.

        :param metadata_dict: dictionary of file metadata
        :return True if required headers are present, False if not
        """
        if any([k for k in self.required_headers if k not in metadata_dict]):
            return False
        else:
            return True

    def get_wcs_corners(self):
        """
        Returns a dict with a type and coordinates of the wcs coordinates if possible for this data type

        Take a fits dictionary and pick out the RA, DEC of each of the four corners.
        Then assemble a Polygon following the GeoJSON spec: http://geojson.org/geojson-spec.html#id4
        Note there are 5 positions. The last is the same as the first. We are defining lines,
        and you must close the polygon.

        If a RADIUS, RA, and DEC are set in the header, it will use that for a circular fov. Otherwise
        It will search for the standard header keys to build a polygon fov.
        """
        headers = self.header_data.get_headers()
        if settings.RADIUS_KEY in headers and settings.RA_KEY in headers and settings.DEC_KEY in headers:
            ra = headers[settings.RA_KEY]
            dec = headers[settings.DEC_KEY]
            r = headers[settings.RADIUS_KEY]

            radius_in_degrees = Angle(r, units.arcsecond).deg
            ra_in_degrees = Angle(ra, units.hourangle).deg
            dec = Angle(dec, units.deg).deg

            c1 = (ra_in_degrees - radius_in_degrees, dec + radius_in_degrees)
            c2 = (ra_in_degrees + radius_in_degrees, dec + radius_in_degrees)
            c3 = (ra_in_degrees + radius_in_degrees, dec - radius_in_degrees)
            c4 = (ra_in_degrees - radius_in_degrees, dec - radius_in_degrees)

        elif (
                self.header_data.headers_are_set(['CD1_1', 'CD1_2', 'CD2_1', 'CD2_2', 'NAXIS1', 'NAXIS2'])
                and not self.header_data.headers_are_set(['NAXIS3'])
        ):
            # Find the RA and Dec coordinates of all 4 corners of the image
            try:
                w = wcs.WCS(headers)
                c1 = w.all_pix2world(1, 1, 1)
                c2 = w.all_pix2world(1, headers['NAXIS2'], 1)
                c3 = w.all_pix2world(headers['NAXIS1'], headers['NAXIS2'], 1)
                c4 = w.all_pix2world(headers['NAXIS1'], 1, 1)
            except ValueError:
                return None

        else:
            # This file doesn't have sufficient information to provide an area
            return None

        return {
            'type': 'Polygon',
            'coordinates': [
                [
                    [
                        float(c1[0]),
                        float(c1[1])
                    ],
                    [
                        float(c2[0]),
                        float(c2[1])
                    ],
                    [
                        float(c3[0]),
                        float(c3[1])
                    ],
                    [
                        float(c4[0]),
                        float(c4[1])
                    ],
                    [
                        float(c1[0]),
                        float(c1[1])
                    ]
                ]
            ]
        }

    def get_filestore_path(self):
        """
        Creates a path to use in the file store using the metadata of this file 
        """
        datatype = 'raw' if self.header_data.get_reduction_level() == 0 else 'processed'
        # Default directory is site/instrument/obsday/datatype/
        return '/'.join((self.header_data.get_site_id(), self.header_data.get_instrument_id(), self.header_data.get_observation_day(), datatype, self.open_file.basename)) + self.open_file.extension

    def get_filestore_content_type(self):
        return ''
