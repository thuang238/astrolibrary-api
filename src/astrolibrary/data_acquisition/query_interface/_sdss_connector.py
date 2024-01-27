"""A connector to the SDSS database API.

Responsibilities:
    - Manages the connection and communication with the SDSS API.
    - Error and exeption handling with the SDSS API. Can be extended to
        handle retries, etc.

"""

from astropy.table import Table
from astroquery.sdss import SDSS

from ._connector import Connector


class SDSSConnector(Connector):
    """A connector to the SDSS database API.

    This is a concrete implementation of the `Connector` class specifically
    for the SDSS dataset. See `Connector` module for more details.

    """

    def __init__(self):
        """Initialize an SDSS connector."""
        self.status: str = ""
        self.results: Table = Table()

    def run_query(self, query, *args, **kwargs):
        """Runs the given query against the SDSS database."""
        try:
            self.results = SDSS.query_sql(query)
        except Exception as e:
            raise e

        if not self.results:
            self.status = "SUCCESS_NO_RESULTS"
            self.results = None
            return self
        if "error_message" in self.results.colnames:
            self.status = "ERROR"
            raise ValueError

        self.status = "COMPLETED"
        return self

    def check_status(self):
        """Checks the status of the given query ID."""
        return self.status

    def get_results(self):
        """Gets the results of the given query ID."""
        return self.results
