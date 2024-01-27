import os
import sys

import numpy as np
import pandas as pd
from astropy import units as u
from astropy.cosmology import WMAP9
from astropy.io import fits


class DataPreprocessing:
    def __init__(
        self,
        file_path,
        min_target_wavelength: float,
        max_target_wavelength: float,
        redshift=0.0,
    ):
        self.MIN_TARGET_WAVELENGTH = min_target_wavelength
        self.MAX_TARGET_WAVELENGTH = max_target_wavelength
        self.df = None
        self.redshift = redshift

        self.read_data(file_path)

    def read_data(self, file_path):
        """Ensure the reading of FITS and CSV files.

        Especially, FITS files are not read by default by Pandas
        and passing them to `pd.read_csv` will raise an error mostly
        depending on compiler of the user. the following error is
        common:
        `ValueError: Big-endian buffer not supported on little-endian compiler`
        """
        if file_path.endswith(".fits"):
            with fits.open(file_path) as hdul:
                data = hdul[1].data

                # Create an empty dictionary for converted data
                converted_data = {}

                # Determine the native byte order
                native_byte_order = (">", "<")[sys.byteorder == "little"]

                # Iterate through columns and convert data if necessary
                for (
                    colname
                ) in data.names:  # Use `data.names` to get column names
                    coldata = data[colname]
                    # Check if data byte order matches the system's native byte order
                    if coldata.dtype.byteorder not in (
                        native_byte_order,
                        "=",
                        "|",
                    ):
                        coldata = coldata.byteswap().newbyteorder()
                    converted_data[colname] = coldata

                # Create DataFrame from converted data
                self.df = pd.DataFrame(converted_data)
        elif file_path.endswith(".csv"):
            try:
                self.df = pd.read_csv(file_path)
            except Exception as e:
                raise ValueError(
                    f"the relative path is not correct, we are running on path: {os.getcwd()}"
                )
        else:
            raise ValueError(
                f"""
            Unsupported file format for the file: '{file_path}'.
            Please provide a FITS or CSV file."""
            )

    def normalize_column(self, column_name):
        if column_name not in self.df.columns:
            raise ValueError(
                f"Column '{column_name}' does not exist in the DataFrame."
            )

        column_values = self.df[column_name]

        std_value = np.std(column_values)

        normalized_values = (
            column_values - np.mean(column_values)
        ) / std_value
        self.df[column_name] = normalized_values

    def remove_outliers_column(self, column_name):
        if column_name not in self.df.columns:
            raise ValueError(
                f"Column '{column_name}' does not exist in the DataFrame."
            )

        column_values = self.df[column_name]

        # Calculate Q1, Q3, and IQR using NumPy
        q1 = np.percentile(column_values, 25)
        q3 = np.percentile(column_values, 75)
        iqr = q3 - q1

        # Calculate lower and upper bounds for outliers
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Filter out outliers based on the IQR rule
        self.df = self.df[
            (column_values >= lower_bound) & (column_values <= upper_bound)
        ]
        return lower_bound, upper_bound

    def correct_redshift(
        self, wavelength_column="Wavelength", flux_column="Flux"
    ):
        if (
            wavelength_column not in self.df.columns
            or flux_column not in self.df.columns
        ):
            raise ValueError(
                f"Specified columns '{wavelength_column}' and '{flux_column}' must exist in the DataFrame."
            )

        # Create a new column for corrected flux
        corrected_redshift_column = f"{flux_column}_corrected"
        self.df[corrected_redshift_column] = None

        if (
            wavelength_column not in self.df.columns
            and wavelength_column != "Wavelength"
        ):
            raise ValueError(
                f"Specified column '{wavelength_column}' must exist in the DataFrame."
            )

        # Convert wavelengths to observed frame
        observed_wavelengths = self.df[wavelength_column].values * (
            1 + self.redshift
        )

        # Create an instance of WMAP9
        cosmo = WMAP9

        # Calculate redshifted wavelengths using luminosity distance
        luminosity_distance = cosmo.luminosity_distance(self.redshift).to(
            u.Mpc
        )
        redshifted_wavelengths = self.df[wavelength_column].values * (
            1 + self.redshift
        )

        # Use the redshifted wavelengths to correct the flux
        corrected_flux = self.df[flux_column].values / redshifted_wavelengths

        # Update the DataFrame with corrected flux values
        self.df[corrected_redshift_column] = corrected_flux

    def wave_align(
        self, wavelength_column="Wavelength", loglam_column="LOGLAM"
    ):
        """
        Align spectra wavelengths within a predefined range.
        """
        if loglam_column in self.df.columns:
            # If LogLam column is present, use it to calculate 'Wavelength'
            self.df[wavelength_column] = 10 ** self.df[loglam_column]

        # Filter wavelengths within the specified range
        self.df = self.df[
            (self.df[wavelength_column] >= self.MIN_TARGET_WAVELENGTH)
            & (self.df[wavelength_column] <= self.MAX_TARGET_WAVELENGTH)
        ]
