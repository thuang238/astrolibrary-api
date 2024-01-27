import pytest
from astropy.table import Table
import requests_mock
from astroquery.sdss import SDSS
from astrolibrary import cross_match


non_empty_objid_list = [1237645879551066262,1237645879578460255, 1237645941291614227, 1237645941824356443]
empty_objid_list = [1237661957220991253, 1237661957220991253, 1237669516362318531, 1237661957220336714]
negative_objid_list = [1237661957220991253, -1237661957220991253, 1237669516362318531, 1237661957220336714]
def test_cross_match_data_invalid():
 
    with pytest.raises(TypeError):
        invalid2 = cross_match()
    
    with pytest.raises(TypeError):
        invalid3 = cross_match()
    
    with pytest.raises(TypeError):
        invalid4 = cross_match([])

    with pytest.raises(ValueError):
        invalid5 = cross_match(empty_objid_list, 2.0, 3)
    
    with pytest.raises(ValueError):
        invalid6 = cross_match(negative_objid_list)
        
def test_cross_match_data_valid_crossmatch():
    valid1 = cross_match(non_empty_objid_list)
    assert valid1 

def test_cross_match_data_valid_no_crossmatch_one_arg():
    valid2 = cross_match(empty_objid_list)
    assert len(valid2) == 0

def test_cross_match_data_valid_no_crossmatch_two_args():
    valid3 = cross_match(non_empty_objid_list, angular_distance_max=5.0)
    assert valid3




