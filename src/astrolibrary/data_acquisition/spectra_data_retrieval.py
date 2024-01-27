"""Spectra Data Retrieval Module.

Allows end-users to:
    - Retrieve spectra data from SDSS using provided identifiers: Plate, Modified Julian Date (MJD), and Fiber ID.
    - Specify optional parameters such as data reduction version (RUN2D), output format ('fits' or 'csv'), 
        SDSS survey type (SURVEY), spectrograph type (SPEC), and data release number (dr_number).
    - Save the downloaded data locally with customizable output directory.

Advantages/Design Considerations:
    - Simplifies the retrieval process through function, `get_spectra_data`, abstracting the details of SDSS data access.
    - Flexible optional parameters that is adaptable to different SDSS configurations.
    - Supports both FITS and CSV output formats, depending on user preference.
    - Handles error conditions, raising specific exceptions.

Limitations and Future Work:
    - Currently supports SDSS dataset only.
    - Assumes default values for optional parameters if not specified.
    - Limited to synchronous data retrieval; does not support asynchronous queries.
    - May not be optimized for large-scale data retrieval scenarios.
    - The module design may need extension for compatibility with future SDSS releases or other datasets.

"""

import csv
import os

import requests
from requests.exceptions import RequestException


def get_spectra_data(
    survey=None,
    run2d=None,
    spec="lite",
    plateid=None,
    mjd=None,
    fiberid=None,
    dr_number=None,
    output_format="fits",
    output_dir=".",
):
    """
    Retrieve spectra data from SDSS.

    Parameters:
    -----------
    plateid, mjd, fiberid: int
        Identifiers for SDSS data. Plate, Modified Julian Date, and Fiber ID.
    run2d: str, optional
        Data reduction version (default: 'v5_13_2')
    output_format: str, optional
        Output format ('fits' or 'csv') (default: 'fits')
    survey: str, optional
        SDSS survey type (default: 'eboss')
    spec: str, optional
        Spectrograph type (default: 'lite')
    dr_number: str, optional
        Data release number (default: '18')
    output_dir:
        Directory location where spectra data is outputted (default: current directory)

    Returns:
    --------
    file_path: path to downloaded data

    Raises:
    -------
    ValueError:
        - If plateid, mjd, or fiberid are not integers.
        - If plateid, mjd, or fiberid are less than 1.
        - If the provided format is not supported.
        - If run2d value is not valid, according to SDSS website
        - If spec value is not valid, according to SDSS website

    RuntimeError:
        - If there is an error in data downloading or processing.

    Timeout:
        - By default, timeout at 30

    Examples:
    ---------
    CSV data
    Retrieving file_path
    >>> file_path_to_csv = get_spectra_data(
            plateid=7644,
            mjd=57327,
            fiberid=528,
            output_format='csv',
            dr_number=18,
        )
    Output: './spec-7644-57327-0528.csv'
    Generating data:
        import pandas as pd
        data = pd.read_csv(file_path_to_csv)
        data.head()

    FITS data
    Retrieving file_path
    >>> file_path_to_fits = get_spectra_data(
            plateid=7644,
            mjd=57327,
            fiberid=528,
            output_format='fits',

            dr_number=17,
        )
    Output: './spec-7644-57327-0528.fits'
    Generating data:
        from astropy.io import fits
        import pandas as pd
        hdul=fits.open(file_path)
        print(hdul)
    """
    if not plateid or not mjd or not fiberid:
        raise ValueError("PLATEID, MJD, and FIBERID must be provided")
    if not survey or not run2d or not dr_number:
        raise ValueError("SURVEY, RUN2D, and DR_NUMBER must be provided")

    if (
        not isinstance(plateid, int)
        or not isinstance(mjd, int)
        or not isinstance(fiberid, int)
    ):
        raise ValueError("PLATEID, MJD, and FIBERID must be of type integer")
    if plateid < 1 or mjd < 1 or fiberid < 1:
        raise ValueError("ID must be a positive number")
    if output_format not in ["fits", "csv"]:
        raise ValueError(
            "Unsupported output format. Supported formats: 'fits', 'csv'"
        )


    # Valid run2d values according to SDSS Website
    if spec not in ["lite", "full"]:
        raise ValueError("Invalid spec value")

    plateid = str(plateid).zfill(4)
    mjd = str(mjd)
    fiberid = str(fiberid).zfill(4)

    dr17_link = (
        f"http://dr17.sdss.org/sas/dr17/{survey}/spectro/redux/{run2d}/spectra/"
        f"{spec}/{plateid}/spec-{plateid}-{mjd}-{fiberid}.fits"
    )
    dr18_link = (
        f"http://dr18.sdss.org/optical/spectrum/view/data/format={output_format}/"
        f"spec={spec}?plateid={plateid}&mjd={mjd}&fiberid={fiberid}"
    )
    link = dr17_link if dr_number == 17 else dr18_link

    try:
        response = requests.get(link, timeout=30)
        response.raise_for_status()

        file_name = f"spec-{plateid}-{mjd}-{fiberid}.{output_format}"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "wb") as file:
            file.write(response.content)

        return file_path

    except RequestException as e:
        raise RuntimeError(f"Data downloading error:{str(e)}") from e
