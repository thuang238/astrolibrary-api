import numpy as np
from astroquery.gaia import Gaia
from astroquery.sdss import SDSS

""" Cross Matching Module
Allows end user to cross-reference astronomical objects
from the SDSS and Gaia catalogs, prioritizing match purity. 
Percise criteria is based on the angular distance.
"""


def cross_match(spec_objid_list, angular_distance_max=2.0, *args):
    """
            Parameters
            ----------
            spec_objid_list: list
                - List of spectroscopic object identifiers from the SDSS catalog we will cross-reference

            angular_distance_max: optional float
                - Describes the maximim angular distance between a Gaia source and the external catalouge SDSS.
                - Measures the degree of separation bewtween celestial objects measured in arcseconds.
                - Default maximum is 2.00 arcseconds.
            Returns
            -------
            Astropy Table
                Table of cross-match results between Gaia and SDSS

            Example Usage
            -------------
                >>>> from astrolibrary import cross_match
                >>>> spec_objid_list = [
                    1237645879551066262,1237645879578460255, 
                    1237645941291614227, 1237645941824356443]
                >>>> table = cross_match(spec_objid_list, 3.0)
                >>>> print(table[])

    Cross-match results:
        Output wil be a table with the following columns:
        source_id, clean_sdssdr13_oid, original_ext_source_id,
        angular_distance, number_of_neighbours, number_of_mates xm_flag arcsec
 
    """

    # Check for empty input
    if not spec_objid_list:
        raise TypeError(
            "Missing required positional arguments: spec_objid_list"
        )

    # Check for empty list
    if len(spec_objid_list) == 0:
        raise TypeError

    # Check for type error
    if not isinstance(spec_objid_list, list):
        raise TypeError("spec_objid_list must be a list")

    # Check for too many positional arguments
    if args:
        raise ValueError("Too many positional arguments. Expected at most 2.")

    # Check for negative values in spec_objid_list
    if (
        spec_objid_list
        and len(spec_objid_list) != 0
        and isinstance(spec_objid_list, list)
        and not args
    ):
        sort_spec_objid_list = sorted(spec_objid_list)
        if sort_spec_objid_list[0] < 0:
            raise ValueError("specObjID values cannot be negative")

    str_objid = ",".join(map(str, spec_objid_list))
    query = f"SELECT * FROM gaiadr3.sdssdr13_best_neighbour WHERE angular_distance < {angular_distance_max} AND original_ext_source_id IN ({str_objid})"
    run_query = Gaia.launch_job_async(query)
    if run_query:
        return run_query.get_results()
    print("No matches were found")
    return None

