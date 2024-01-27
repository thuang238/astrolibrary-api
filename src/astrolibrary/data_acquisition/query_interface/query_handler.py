"""Query Handler Module.

Allows end-users to:
    - Instantiate a query handler for a given dataset: SDSS, for example.
    - Run a query.
    - Check the status of a query, useful for long-running queries.
    - Get the results of a query.

Advantages/Design Considerations:
    - Make the library more user-friendly, as the users only interact with the
      high-level `QueryHandler` class without needing to understand the
      underlying details.
    - The `QueryHandler` class is dataset-agnostic, i.e. it can be used to
      query any dataset without having the client/user to memorize specific
      api calls for each dataset: simply query it with ADQL & SQL.
    - This design allows for the addition of new datasets without modifying
      the existing codebase.
    - Can be easily extended to support users' own provided datasets in
      addition to core ones like SDSS.

Limitations and Future Work:
    - Currently, supports SDSS dataset through the `SDSSConnector` class, but
      can be extended to support other datasets as explained above.
    - Currently, the `QueryHandler` supports synchronous queries only, but the
      design can be extended to support asynchronous queries as well.
      This means `run_query` will wait for the query to finish and sets
      the appropriate attributes.

"""
from astropy.table import Table
from ._sdss_connector import SDSSConnector
from ._connector import Connector


class QueryHandler:
    """A class for handling queries to a given `dataset_name`."""

    def __init__(
        self,
        dataset_name: str,
    ):
        """Initialize a query handler for a given `dataset_name`.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset to query. Currently, only "SDSS" is
            supported.
        Returns
        -------
        QueryHandler
            An instance of the `QueryHandler` class initialized with the
            given `dataset_name`'s connector.

        Raises
        ------
        ValueError : If the given `dataset_name` is not supported/valid.

        """
        match dataset_name:
            case "SDSS":
                self.connector = SDSSConnector()
            # With software extensibility in mind, we can add more datasets
            # support here.
            case _:
                raise ValueError(f"Dataset '{dataset_name}' is not supported.")

        self.jobs: dict[str, Connector] = {}

    def run_query(self, query: str, *args, **kwargs) -> str:
        """Runs the given query against `self.dataset_name`.

        Uses the connector of `self.dataset_name` to run the query. To make
        this function dataset-agnostic, we will require the `_name_connector`
        modules to inherit from a base class `Connector` that has a `run_query`
        method.

        Parameters
        ----------
        query : str
            The query to run.
        *args : iterable
            Other arguments. For future extensibility.
        **kwargs : dict
            Other keyword arguments. For future extensibility.

        Returns
        -------
        query_id : str
            A unique identifier for the query that can be used to check the
            status of the query and get the results

        Raises
        ------
        ValueError : If the given `query` is invalid.

        Examples
        --------
        These are written in doctest format, and should illustrate how to
        use the function.

        >>> from astrolibrary.query_interface.query_handler import QueryHandler
        >>> qh = QueryHandler(dataset_name="sdss")
        >>> qh.run_query("SELECT * FROM table LIMIT 10")
        '12345'

        Notes
        -----
        The main reason for `query_id` is to allow future extensibility to
        support asynchronous queries, while also keeping backward compatibility
        with synchronous queries.

        """
        self.connector.run_query(
            query, *args, **kwargs
        )  # Should raise appropriate exceptions, if any.
        self.jobs[query_id := str(hash(query))] = self.connector
        return query_id

    def check_status(self, query_id: str) -> str:
        """Check the status of a query given its `query_id`.

        Parameters
        ----------
        query_id : str
            The unique identifier of the query to check its status.

        Returns:
        --------
        status : str
            The status of the query. This can be one of the following:
                - "COMPLETED": The query completed successfully.
                - "ERROR": The query failed with an error.
                - "RUNNING": The query is still running.

        Raises:
        -------
        ValueError:
            If the given `query_id` is not found in `self.statuses`.

        """
        if query_id not in self.jobs:
            raise ValueError(f"Query ID '{query_id}' not found")
        return self.jobs[query_id].check_status()

    def get_results(self, query_id: str) -> Table:
        """Get the results of a query.

        Parameters:
        -----------
        query_id : str
            The unique identifier of the query to get its results.

        Returns:
        --------
        table : astropy.table.Table
            The results of the query as an astropy table.

        Raises:
        -------
        ValueError:
            If the given `query_id` is not found in `self.results`.

        """
        if query_id not in self.jobs:
            raise ValueError(f"Query ID '{query_id}' not found.")
        return self.jobs[query_id].get_results()
