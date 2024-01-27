"""
This test suite (a module) runs tests for query_interface/query_handler.py
module.
"""
import pytest
from astropy.table import Table
from astroquery.sdss import SDSS
from astrolibrary import QueryHandler


@pytest.fixture
def query_handler():
    """Returns an instance of QueryHandler."""
    return QueryHandler(dataset_name="SDSS")


def mocked_exception():
    """Used to simulate exceptions from the SDSS API or other APIs."""
    raise Exception()


query_input = """
                SELECT top 10 z, ra, dec, bestObjID
                FROM specObj
                WHERE class = 'galaxy' AND z > 0.3 AND zWarning = 0
              """
success_results = Table({"z": [0.3], "ra": [0.3], "dec": [0.3], "bestObjID": [0.3]})

# This is how SDSS query_sql returns errors
errored_results = Table({"error_message": ["error"]})


class TestQueryHandler:
    """Tests for the QueryHandler class."""

    def test_query_handler_handles_invalid_dataset(self):
        """Tests that the query handler raises appropriate exceptions."""
        # Test invalid dataset
        with pytest.raises(ValueError):
            QueryHandler(dataset_name="invalid_dataset")

        # Test empty dataset
        with pytest.raises(ValueError):
            QueryHandler(dataset_name="")

    def test_query_handler_runs_valid_query(self, query_handler, monkeypatch):
        """Tests that the query handler runs a query."""
        # Mock the SDSS.query_sql method
        monkeypatch.setattr(SDSS, "query_sql", lambda x: success_results)
        query_id = query_handler.run_query(query_input)
        assert query_id

    def test_query_handler_runs_invalid_query(self, query_handler, monkeypatch):
        """Tests that the query handler raises appropriate exceptions."""

        monkeypatch.setattr(SDSS, "query_sql", lambda x: errored_results)

        # Test invalid query
        with pytest.raises(Exception):
            query_handler.run_query("invalid_query")

        # Test empty query
        with pytest.raises(ValueError):
            query_handler.run_query("")

    def test_query_handler_run_query_handles_api_exceptions(
        self, query_handler, monkeypatch
    ):
        """Test handling of exceptions such as network/connection issues."""
        # Mock the SDSS.query_sql method
        monkeypatch.setattr(SDSS, "query_sql", lambda x: mocked_exception())
        with pytest.raises(Exception):
            query_handler.run_query(query_input)

    def test_query_handler_valid_check_status(self, query_handler, monkeypatch):
        """Tests that the query handler checks the status of a query."""

        monkeypatch.setattr(SDSS, "query_sql", lambda x: success_results)

        query_id = query_handler.run_query(query_input)
        status = query_handler.check_status(query_id)
        assert status in ["COMPLETED", "RUNNING"]

    def test_query_handler_invalid_check_status(self, query_handler):
        """Tests that the query handler raises appropriate exceptions."""
        # Test invalid status
        with pytest.raises(ValueError):
            query_handler.check_status("invalid_status")

        # Test empty status
        with pytest.raises(ValueError):
            query_handler.check_status("")

    def test_query_handler_get_results_valid_case(self, query_handler, monkeypatch):
        """Tests that the query handler gets the results of a query."""

        monkeypatch.setattr(SDSS, "query_sql", lambda x: success_results)

        query_id = query_handler.run_query(query_input)
        result = query_handler.get_results(query_id)
        assert isinstance(result, Table)
        assert len(result) > 0
        assert "z" in result.colnames
        assert "ra" in result.colnames
        assert "dec" in result.colnames
        assert "bestObjID" in result.colnames

    def test_query_handler_get_results_invalid_case(self, query_handler):
        """Tests that the query handler raises appropriate exceptions."""
        # Test invalid results
        with pytest.raises(ValueError):
            query_handler.get_results("invalid_results")

        # Test empty results
        with pytest.raises(ValueError):
            query_handler.get_results("")
