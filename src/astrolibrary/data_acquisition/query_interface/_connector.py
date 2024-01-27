""" An abstract class for a connector to a database.

This is to enforce consistency between different connectors: SDSS, Gaia, or
even user-provided datasets in the future. Hence, having a software thats
extensible and easy to maintain.

To achieve this, this will act as a base class for any connector to a dataset
and it can be added to `QueryHandler` with minimal/no modifications. Allowing
separation of concerns.

"""
from abc import ABC, abstractmethod


class Connector(ABC):
    """An abstract class for a connector to a database."""

    @abstractmethod
    def run_query(self, query, *args, **kwargs):
        """Runs the given query against the database.

        Parameters
        ----------
        query : str
            The query to run.
        *args : iterable
            Other arguments.
        **kwargs : dict
            Other keyword arguments.

        Returns
        -------
        Connector
            Should return it`self` to allow for method chaining and ease of
            use in `QueryHandler`.

        Raises
        ------
        ValueError : If the given query is invalid.

        """

    @abstractmethod
    def check_status(self):
        """Checks the status of the given query ID.

        Returns
        -------
        str
            The status of the query. Should be one of the following:
            ["COMPLETED", "RUNNING", "ERROR"].
        """

    @abstractmethod
    def get_results(self):
        """Gets the results of the given query ID.

        Returns
        -------
        astropy.table.Table
            The query results.

        """
