import pandas as pd
import pytest
from astropy.io import fits
from astropy.table import Table
from astroquery.sdss import SDSS

from astrolibrary import MetaDataExtractor

# Load the FITS file
FITS_FILE_PATH = "tests/data_processing/dr18webexample.fits"

data = {
    "objid": [1237645879551066262],
    "ra": [348.902530171573],
    "dec": [1.27188624932946],
    "u": [19.38905],
    "g": [18.24496],
    "r": [17.58728],
    "i": [17.20807],
    "z": [16.90905],
    "run": [94],
    "rerun": [301],
    "camcol": [6],
    "field": [94],
    "specobjid": [430194949951088640],
    "class": ["GALAXY"],
    "redshift": [0.03212454],
    "plate": [382],
    "mjd": [51816],
    "fiberid": [368],
}

mocked_sdss_data = Table(data)


@pytest.fixture
def fits_extractor():
    return MetaDataExtractor(FITS_FILE_PATH)


def test_get_metadata_invalid_columns(fits_extractor):
    with pytest.raises(ValueError):
        fits_extractor.get_metadata(["INVALID_COLUMN"])


def test_extract_metadata_empty_file():
    with pytest.raises(Exception):  # Replace with specific exception if known
        MetaDataExtractor("path/to/empty_or_corrupted_file.fits")


def test_get_coordinates(fits_extractor):
    coordinates = fits_extractor.get_coordinates()
    assert len(coordinates) == 2
    assert coordinates


def get_identifiers(fits_extractor, monkeypatch):
    monkeypatch.setattr(SDSS, "query_sql", lambda x: mocked_sdss_data)
    identifiers = fits_extractor.get_identifiers()
    assert "PLATE" in identifiers
    assert "MJD" in identifiers


def test_get_class_of_object(fits_extractor, monkeypatch):
    monkeypatch.setattr(SDSS, "query_sql", lambda x: mocked_sdss_data)
    class_of_object = fits_extractor.get_class_of_object()
    assert class_of_object in ["STAR", "GALAXY", "QSO"]


def test_get_redshift(fits_extractor, monkeypatch):
    monkeypatch.setattr(SDSS, "query_sql", lambda x: mocked_sdss_data)
    redshift = fits_extractor.get_redshift()
    assert redshift


def test_extract_metadata(fits_extractor):
    metadata = fits_extractor.get_metadata(
        ["PLATE", "DESIGNID", "MJD", "RUN2D", "RUN1D"]
    )
    for key in ["PLATE", "DESIGNID", "MJD", "RUN2D", "RUN1D"]:
        assert key in metadata.columns


def test_query_handler_mocked_response(fits_extractor, monkeypatch):
    monkeypatch.setattr(SDSS, "query_sql", lambda x: Table())
    result = fits_extractor._extract_more_metadata()
    assert result is None or result.empty


def test_extract_more_metadata_exception_handling(fits_extractor, monkeypatch):
    def mock_query_exception(query):
        raise Exception("Mocked query exception")

    monkeypatch.setattr(SDSS, "query_sql", mock_query_exception)
    with pytest.raises(Exception):
        fits_extractor._extract_more_metadata()


def test_invalid_file_path():
    with pytest.raises(FileNotFoundError):
        MetaDataExtractor("nonexistent/path/to/file.fits")
