import pandas as pd
from astropy.io import fits

from astrolibrary import QueryHandler


class MetaDataExtractor:
    def __init__(self, file_path):
        """
        Initialize the MetaDataExtractor.

        Parameters:
        - file_path (str): Path to the data file (FITS or CSV).
        """
        hdul = fits.open(file_path)
        data = hdul[1].data
        self.df = pd.DataFrame(data)
        self.metadata = None

    def get_coordinates(self):
        """
        Get the coordinates of the data.

        Returns:
        - tuple: Tuple containing the coordinates.
                 Also can be accessed by calling
                 get_metadata(df[["RACEN", "DECCEN"]]) as dataframe.
        """
        return (self.df["RACEN"], self.df["DECCEN"])

    def get_identifiers(self):
        """
        Get the identifiers of the data.

        Returns:
        - dataframe: Dataframe containing the identifiers of the data.
        """
        return self.df[["PLATE", "MJD"]]

    def get_class_of_object(self):
        """
        Get the class of the object.

        Returns:
        - str: a string containing the class of the object.
        """

        data = self._extract_more_metadata()
        return data["class"]

    def get_redshift(self):
        """
        Get the redshift of the data.

        Returns:
        """
        data = self._extract_more_metadata()
        return self._extract_more_metadata()["redshift"]

    def _extract_more_metadata(self):
        """
        Extract more metadata from the data.
        """

        plate = int(self.df["PLATE"])
        ra, de = int(self.df["RACEN"]), int(self.df["DECCEN"])

        qh = QueryHandler(dataset_name="SDSS")
        qid = qh.run_query(
            f"""
            SELECT p.objid,p.ra,p.dec,p.u,p.g,p.r,p.i,p.z,
            p.run, p.rerun, p.camcol, p.field,
            s.specobjid, s.class, s.z as redshift,
            s.plate, s.mjd, s.fiberid
            FROM PhotoObj AS p
            JOIN SpecObj AS s ON s.bestobjid = p.objid
            WHERE s.plate = {plate}
            AND p.ra = {ra}
            AND p.dec = {de}
            """
        )
        return qh.get_results(qid)

    def get_metadata(self, list_of_columns):
        """
        Get the extracted metadata. For other metadata, clients
        can call the this method with the appropriate list of columns.

        Returns:
        - dict: Dictionary containing the extracted metadata.
        """

        try:
            res = self.df[list_of_columns]
        except Exception as err:
            raise ValueError(
                "one or more field names you provided do not exist in the metadata."
            ) from err

        return res
