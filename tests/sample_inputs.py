""" Sample inputs for tests 

We will use some dummy data, real data derived from class, and also
real data from SDSS.

"""

# From Lecture 12
lec12_link = "https://dr17.sdss.org/sas/dr17/eboss/spectro/redux/v5_20_13_2/spectra/lite/7644/spec-7644-57327-0528.fits"
dr18_link = (
    "https://dr18.sdss.org/sas/dr18/spectro/boss/redux/eFEDS/conflist.fits"
)


def sample_n_objects_query(class_name, n):
    """Returns a sample of n objects of a given class."""
    query = f"""
    SELECT TOP {n}
    p.objid,p.ra,p.dec,p.u,p.g,p.r,p. i,p.z,
    p. run, p. rerun, p.camcol, p.field,
    s. specobjid, s.class, s.z as redshift, s.plate, s.mjd, s.fiberid
    as fiberid
    FROM Photoobj AS p
    JOIN Specobj AS s ON s.bestobjid = p.objid
    WHERE
    p.u BETWEEN 0 AND 19.6
    AND g BETWEEN 0 AND 20
    AND s.class = '{class_name}'
    """
    return query
