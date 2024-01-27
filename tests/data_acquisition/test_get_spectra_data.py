from unittest.mock import patch

import pytest
import requests

from astrolibrary import get_spectra_data


def test_invalid_id_types():
    with pytest.raises(ValueError):
        get_spectra_data(
            survey="eboss",
            run2d="v5_13_2",
            plateid="abc",
            mjd="123",
            fiberid="xyz",
            dr_number="18",
        )


def test_invalid_id_values():
    with pytest.raises(ValueError):
        get_spectra_data(
            survey="eboss",
            run2d="v5_13_2",
            plateid=None,
            mjd=None,
            fiberid=None,
            dr_number=None,
        )


def test_invalid_id_values():
    with pytest.raises(ValueError):
        get_spectra_data(
            survey="eboss",
            run2d="v5_13_2",
            plateid=-1,
            mjd=-1,
            fiberid=-1,
            dr_number=-1,
        )
    with pytest.raises(ValueError):
        get_spectra_data(
            survey="eboss",
            run2d="v5_13_2",
            plateid=0,
            mjd=0,
            fiberid=0,
            dr_number=0,
        )


sample_valid_args = {
    "survey": "eboss",
    "run2d": "v5_13_2",
    "plateid": 123,
    "mjd": 45678,
    "fiberid": 789,
    "dr_number": "18",
}


def test_invalid_spec_value():
    with pytest.raises(ValueError):
        # make a copy of sample_valid_args
        args = sample_valid_args.copy()
        args["spec"] = "abc"
        get_spectra_data(**args)


def test_invalid_output_format():
    with pytest.raises(ValueError):
        # make a copy of sample_valid_args
        args = sample_valid_args.copy()
        args["output_format"] = "abc"
        get_spectra_data(**args)


def test_invalid_none_parameters():
    with pytest.raises(ValueError):
        # make a copy of sample_valid_args
        args = sample_valid_args.copy()
        args["survey"], args["run2d"], args["dr_number"] = None, None, None
        get_spectra_data(**args)


@patch("requests.get")
def test_successful_api_call(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"some data"
    file_path = get_spectra_data(**sample_valid_args)
    assert file_path.endswith(".fits")


@patch("requests.get", side_effect=requests.exceptions.Timeout)
def test_timeout_exception(mock_get):
    with pytest.raises(RuntimeError):
        get_spectra_data(**sample_valid_args)
