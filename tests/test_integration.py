""" Tests for end-to-end integration of the library.

In this test module, we test the integration between components of our 
library's pipeline, from data acquisition to visualization. This involves 
testing for the full workflow of the pipeline to ensure that data flows 
smoothly between components and produces expected results.

While unit tests focus on isolating each component and often require mocking 
external dependencies, integration tests will aim to verify how different parts
of our library work together, including interactions with external systems. 

The workflow of the pipeline is as follows:

          +---------------------------------+  
          |       Data Acquisition          |
          +---------------------------------+
Client -> | QueryHandler --> crossmatching  |   
          |         |         |             | 
          |         V         V             |
          |_______ get_spectra_data ________|
                       |                   
                       |
          _____________|________________
         |                              |        
         V                              V    
+----------------------+        +------------------+
DataPreprocessing      |        | 5. Visualization |
+----------------------+        +------------------+
- Normalization        |        |     - Plotting   |     
- Remove outliers      |        +------------------+
- Correct redshift     |  
- Wavelength alignment |        +----------------------+
- Metadata extraction  | ---->  | 6. Data Manipulation |
+----------------------+        +----------------------+
                                | ML Prediction Module |
                                +----------------------+

"""

import numpy as np
import pandas as pd
import pytest
from astropy.io import fits
from astropy.table import Table
from sample_inputs import sample_n_objects_query

from astrolibrary import (
    DataPreprocessing,
    QueryHandler,
    cross_match,
    get_spectra_data,
)

# Sample queries
star_query = sample_n_objects_query("STAR", 10)
galaxy_query = sample_n_objects_query("GALAXY", 10)
quasar_query = sample_n_objects_query("QSO", 10)

# A correct result from runing that query should result in a table with
# the following columns:
#           objid	ra	dec	u	g	r	i	z	run	rerun	camcol	field
#           specobjid	class	redshift	plate	mjd	fiberid


@pytest.fixture
def query_handler():
    """Returns an instance of QueryHandler."""
    return QueryHandler(dataset_name="SDSS")


@pytest.fixture
def data_preprocessing():
    """Returns an instance of DataPreprocessing."""
    return DataPreprocessing()


valid_fits_file_path = None  # To be set upon the first successful download


class TestsEndtoEndIntegration:
    # -------------------------------------------------------------
    #   Integration within Data Acquisition workflow
    # -------------------------------------------------------------
    def test_query_handler_handles_invalid_dataset(self):
        # Test invalid dataset
        with pytest.raises(ValueError):
            QueryHandler(dataset_name="invalid_dataset")

        # Test empty dataset
        with pytest.raises(ValueError):
            QueryHandler(dataset_name="")

    def test_queryhandler_handles_valid_query(self, query_handler):
        query_id = query_handler.run_query(star_query)
        assert query_id

        results = query_handler.get_results(query_id)
        assert isinstance(results, Table)
        assert "objid" in results.colnames
        assert "ra" in results.colnames
        assert "dec" in results.colnames
        assert "class" in results.colnames

    def test_query_handler_and_get_spectra_data(self, query_handler):
        # Run query
        query_id = query_handler.run_query(
            """SELECT TOP 1000 s.plate, s.mjd, s.fiberid as fiberid
                FROM Specobj AS s"""
        )
        query_results = query_handler.get_results(query_id)

        survey = "eboss"
        plateid = 7644
        mjd = 57327
        fiberid = 528
        run2d = "v5_13_2"
        dr_number = 17
        survey = "eboss"

        # Get fits file from spectra_data
        file_path = get_spectra_data(
            survey=survey,
            run2d=run2d,
            plateid=plateid,
            mjd=mjd,
            fiberid=fiberid,
            dr_number=dr_number,
        )
        assert file_path
        assert file_path.endswith(".fits")
        # assert that it can be opened
        with fits.open(file_path) as hdul:
            assert hdul
            assert isinstance(hdul, fits.hdu.hdulist.HDUList)
            # If this went through, we can asssme we have a valid file
            # fit file to reuse in testing. So that we limit the number
            # of downloads, we will save the file path to use in other
            # tests.
            global valid_fits_file_path
            valid_fits_file_path = file_path

    def test_query_handler_and_crossmatching(self, query_handler):
        s_id = query_handler.run_query(star_query)
        g_id = query_handler.run_query(galaxy_query)
        q_id = query_handler.run_query(quasar_query)

        assert s_id
        assert g_id
        assert q_id

        # Crossmatching
        stars, galaxies, qsos = (
            query_handler.get_results(s_id),
            query_handler.get_results(g_id),
            query_handler.get_results(q_id),
        )
        # Make a list of all mixed ids of stars, galaxies, and qsos
        objid_list = (
            [star["objid"] for star in stars]
            + [galaxy["objid"] for galaxy in galaxies]
            + [qso["objid"] for qso in qsos]
        )

        # Crossmatching SDSS and GAIA
        gia_sdss_crossmatch_table = cross_match(
            objid_list[:4], angular_distance_max=1.8
        )

        if not gia_sdss_crossmatch_table:  # If no matches were found
            return

        assert isinstance(gia_sdss_crossmatch_table, Table)

        list_to_check = [
            "source_id",
            "clean_sdssdr13_oid",
            "original_ext_source_id",
            "angular_distance",
            "number_of_neighbours",
            "number_of_mates",
            "xm_flag",
        ]
        colnames = gia_sdss_crossmatch_table.colnames
        # Check if all elements in list_to_check are in colnames
        assert all(element in colnames for element in list_to_check)

    def test_data_acquisation_workflow(self, query_handler):
        """Get spectra data for Gaia-SDSS crossmatched objects.

        This will cover the integration between QueryHandler,
        crossmatching, and get_spectra_data. Hence, confirming the
        end-to-end integration of data acquisition workflow.

        """
        s_id = query_handler.run_query(star_query)
        g_id = query_handler.run_query(galaxy_query)
        q_id = query_handler.run_query(quasar_query)

        s_objids = query_handler.get_results(s_id)["objid"]
        g_objids = query_handler.get_results(g_id)["objid"]
        q_objids = query_handler.get_results(q_id)["objid"]

        # Get crossmatched table
        matches_table = cross_match(
            [*s_objids, *g_objids, *q_objids], angular_distance_max=1.8
        )

        # Use query_handler to identify the PLATEID, MJD, FIBERID for each
        # matched object to get spectra data
        objids_with_matches = matches_table["clean_sdssdr13_oid"]

        count = 0
        for objid in objids_with_matches:
            if count == 1:  # Only download 1 file due to time out issues
                # One file is enough to test the integration
                break

            # Get fits file from spectra_data
            q_id = query_handler.run_query(
                f"SELECT plate, mjd, fiberid FROM Specobj WHERE specobjid = {objid}"
            )

            if not q_id:
                continue

            res = query_handler.get_results(q_id)
            if not res:
                continue

            plate, mjd, fiberid = (
                res[0]["plate"],
                res[0]["mjd"],
                res[0]["fiberid"],
            )

            file_path = get_spectra_data(
                int(plate), int(mjd), int(fiberid), output_format="fits"
            )
            assert file_path
            assert file_path.endswith(".fits")

    # ----------------------------------------------------------------
    #    Integration between Data Acquisition and Data Preprocessing
    # ----------------------------------------------------------------

    def test_data_acquisation_and_read_data(self):
        file_path = valid_fits_file_path
        data_processor = DataPreprocessing(
            file_path=file_path,
            min_target_wavelength=100,
            max_target_wavelength=700,
        )

        assert data_processor.df is not None
        assert isinstance(data_processor.df, pd.DataFrame)

    def test_data_acquisation_and_normalize(self):
        file_path = valid_fits_file_path
        data_processor = DataPreprocessing(
            file_path=file_path,
            min_target_wavelength=100,
            max_target_wavelength=700,
        )
        # Call normalize_column method
        column_name = "flux"
        data_processor.normalize_column(column_name)

        # Check if the mean is close to 0 and std is close to 1
        np.testing.assert_allclose(
            data_processor.df[column_name].mean(), 0, atol=0.1
        )
        np.testing.assert_allclose(
            data_processor.df[column_name].std(), 1, atol=0.1
        )

    def test_data_acquisation_and_remove_outliers(self):
        file_path = valid_fits_file_path
        data_processor = DataPreprocessing(
            file_path=file_path,
            min_target_wavelength=100,
            max_target_wavelength=700,
        )

        # Call _remove_outliers_column method
        column_name = "flux"
        l_bound, u_bound = data_processor.remove_outliers_column(column_name)

        # Check if outliers are removed
        # Check if all values in the Series are within the bounds
        assert (
            (data_processor.df[column_name] >= l_bound)
            & (data_processor.df[column_name] <= u_bound)
        ).all()

    def test_data_acquisation_and_wave_align(self):
        file_path = "tests/sample_test_csv.csv"
        min_target = 200
        max_target = 500
        data_processor = DataPreprocessing(
            file_path=file_path,
            min_target_wavelength=min_target,
            max_target_wavelength=max_target,
        )

        # Call _wave_align method
        wavelength_column = "Wavelength"
        loglam_column = "LOGLAM"
        data_processor.wave_align(wavelength_column, loglam_column)

        # Check if wavelengths are within the specified range
        assert all(data_processor.df[wavelength_column] >= min_target)
        assert all(data_processor.df[wavelength_column] <= max_target)

    def test_data_acquisation_and_correct_redshift(self):
        file_path = "tests/sample_test_csv.csv"
        data_processor = DataPreprocessing(
            file_path=file_path,
            min_target_wavelength=100,
            max_target_wavelength=700,
        )

        wavelength_column = "Wavelength"
        flux_column = "Flux"

        data_processor.correct_redshift(wavelength_column, flux_column)
        corrected_column_name = f"{flux_column}_corrected"
        assert corrected_column_name in data_processor.df.columns


def clean_up_downloads():
    """Cleans up downloaded files."""
    import glob
    import os

    # Get list of downloaded files: all .fits and .csv
    downloaded_files = glob.glob("*.fits") + glob.glob("*.csv")

    # Remove downloaded files
    for file in downloaded_files:
        os.remove(file)
    print("Cleaned up downloaded files.")
    return True
