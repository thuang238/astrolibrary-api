import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from astrolibrary import DataPreprocessing

data = {
    "Column1": [1, 2, 3, 10, 15, 20, 1000],
    "Column2": [0.5, 1.5, 2.5, 9.5, 14.5, 19.5, 999.5],
}
df = pd.DataFrame(data)
df.to_csv("mock_data.csv", index=False)

data2 = {
    "Wavelength": [100, 200, 300, 400, 500],
    "LOGLAM": [2, 2.301, 2.477, 2.602, 2.699],
}
df = pd.DataFrame(data2)
df.to_csv("mock_data_wave_align.csv", index=False)


@pytest.fixture
def sample_data():
    return {"FLUX": [1, 2, 3], "LOGLAM": [4, 5, 6]}


def test_read_data_fits(sample_data):
    with patch("astropy.io.fits.open") as mock_fits_open:
        # Mock the FITS file opening
        mock_fits_open.return_value.__getitem__.return_value.data = sample_data
        data_processor = DataPreprocessing(
            file_path="sample.fits",
            min_target_wavelength=100,
            max_target_wavelength=700,
        )
        assert data_processor.df is not None


def test_read_data_csv(sample_data):
    with patch("pandas.read_csv") as mock_read_csv:
        # Mock the CSV file reading
        mock_read_csv.return_value = pd.DataFrame(sample_data)
        data_processor = DataPreprocessing(
            file_path="sample.csv", min_target_wavelength=100, max_target_wavelength=700
        )
        pd.testing.assert_frame_equal(data_processor.df, pd.DataFrame(sample_data))


def test_read_data_unsupported_format():
    # Initialize DataPreprocessing with an unsupported file format
    file_path = "sample.txt"
    min_target_wavelength = 100
    max_target_wavelength = 700

    # Test ValueError for unsupported file format
    with pytest.raises(ValueError):
        data_processor = DataPreprocessing(
            file_path=file_path,
            min_target_wavelength=min_target_wavelength,
            max_target_wavelength=max_target_wavelength,
        )
        data_processor.read_data(file_path)


def test_remove_outliers_column():
    # Initialize DataPreprocessing with sample DataFrame and wavelength parameters
    min_target_wavelength = 100
    max_target_wavelength = 700
    file_path = "mock_data.csv"
    data_processor = DataPreprocessing(
        file_path,
        min_target_wavelength=min_target_wavelength,
        max_target_wavelength=max_target_wavelength,
    )

    # Call read_data to populate self.df
    data_processor.read_data("mock_data.csv")

    # Call _remove_outliers_column method
    column_name = "Column1"
    data_processor.remove_outliers_column(column_name)

    # Check if outliers are removed
    assert all(data_processor.df[column_name] <= 20)
    assert 1000 not in data_processor.df[column_name].values


def test_remove_outliers_invalid_column():
    # Initialize DataPreprocessing with sample DataFrame and wavelength parameters
    min_target_wavelength = 100
    max_target_wavelength = 700
    file_path = "mock_data.csv"
    data_processor = DataPreprocessing(
        file_path,
        min_target_wavelength=min_target_wavelength,
        max_target_wavelength=max_target_wavelength,
    )

    # Call read_data to populate self.df
    data_processor.read_data("mock_data.csv")

    # Call _remove_outliers_column method
    column_name = "Column 3"
    with pytest.raises(
        ValueError, match=f"Column '{column_name}' does not exist in the DataFrame."
    ):
        data_processor.normalize_column(column_name)


def test_normalize_column(sample_data):
    file_path = "mock_data.csv"
    min_target_wavelength = 100
    max_target_wavelength = 700
    data_processor = DataPreprocessing(
        file_path=file_path,
        min_target_wavelength=min_target_wavelength,
        max_target_wavelength=max_target_wavelength,
    )

    # Call read_data to populate self.df
    data_processor.read_data("mock_data.csv")

    # Call normalize_column method
    column_name = "Column1"
    data_processor.normalize_column(column_name)

    # Check if the mean is close to 0 and std is close to 1
    np.testing.assert_allclose(data_processor.df[column_name].mean(), 0, atol=0.1)
    np.testing.assert_allclose(data_processor.df[column_name].std(), 1, atol=0.1)


def test_normalize_column_missing_column():
    file_path = "mock_data.csv"
    min_target_wavelength = 100
    max_target_wavelength = 700
    data_processor = DataPreprocessing(
        file_path=file_path,
        min_target_wavelength=min_target_wavelength,
        max_target_wavelength=max_target_wavelength,
    )

    # Call read_data to populate self.df
    data_processor.read_data("mock_data.csv")

    column_name = "Column3"
    with pytest.raises(
        ValueError, match=f"Column '{column_name}' does not exist in the DataFrame."
    ):
        data_processor.normalize_column(column_name)


def test_remove_outliers_missing_column():
    file_path = "mock_data.csv"
    min_target_wavelength = 100
    max_target_wavelength = 700
    data_processor = DataPreprocessing(
        file_path=file_path,
        min_target_wavelength=min_target_wavelength,
        max_target_wavelength=max_target_wavelength,
    )

    # Call read_data to populate self.df
    data_processor.read_data("mock_data.csv")

    column_name = "Column3"
    with pytest.raises(
        ValueError, match=f"Column '{column_name}' does not exist in the DataFrame."
    ):
        data_processor.remove_outliers_column(column_name)


@pytest.fixture
def sample_data_wave_align():
    return {
        "Wavelength": [100, 200, 300, 400, 500],
        "LOGLAM": [2, 2.301, 2.477, 2.602, 2.699],
    }


def test_wave_align(sample_data_wave_align):
    # Initialize DataPreprocessing with sample DataFrame and file path
    file_path = "mock_data_wave_align.csv"
    min_target_wavelength = 200
    max_target_wavelength = 500
    data_processor = DataPreprocessing(
        file_path=file_path,
        min_target_wavelength=min_target_wavelength,
        max_target_wavelength=max_target_wavelength,
    )
    data_processor.df = pd.DataFrame(sample_data_wave_align)

    # Call _wave_align method
    wavelength_column = "Wavelength"
    loglam_column = "LOGLAM"
    data_processor.wave_align(wavelength_column, loglam_column)

    # Check if wavelengths are within the specified range
    assert all(data_processor.df[wavelength_column] >= min_target_wavelength)
    assert all(data_processor.df[wavelength_column] <= max_target_wavelength)


def test_input_validation_missing_flux_column(sample_data_wave_align):
    # Initialize DataPreprocessing with sample DataFrame and file path
    file_path = "mock_data_wave_align.csv"
    min_target_wavelength = 200
    max_target_wavelength = 500
    data_processor = DataPreprocessing(
        file_path=file_path,
        min_target_wavelength=min_target_wavelength,
        max_target_wavelength=max_target_wavelength,
    )
    data_processor.df = pd.DataFrame(sample_data_wave_align)

    # Test with missing flux column
    wavelength_column = "Wavelength"
    flux_column = "NonexistentColumn"

    # Assert that ValueError is raised
    with pytest.raises(
        ValueError,
        match=f"Specified columns '{wavelength_column}' and '{flux_column}' must exist in the DataFrame.",
    ):
        data_processor.correct_redshift(wavelength_column, flux_column)


def test_correct_redshift_with_flux_column(sample_data_wave_align):
    file_path = "mock_data_wave_align.csv"
    min_target_wavelength = 200
    max_target_wavelength = 500
    data_processor = DataPreprocessing(
        file_path=file_path,
        min_target_wavelength=min_target_wavelength,
        max_target_wavelength=max_target_wavelength,
    )
    data_processor.df = pd.DataFrame(sample_data_wave_align)

    wavelength_column = "Wavelength"
    flux_column = "LOGLAM"

    data_processor.correct_redshift(wavelength_column, flux_column)

    corrected_column_name = "LOGLAM_corrected"
    assert corrected_column_name in data_processor.df.columns
