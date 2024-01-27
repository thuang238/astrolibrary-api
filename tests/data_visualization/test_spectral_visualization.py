import pytest
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch
from astrolibrary import plot

def test_plot_invalid_input():
    # Empty DataFrame
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="The DataFrame must contain 'Wavelength' and 'flux' columns."):
        plot(empty_df)

    # Missing positional arguments for Wavelength' and 'flux'
    invalid_df_no_flux_or_wavelength = pd.DataFrame([[1, 8, 3, 10], [3, 10, 9, 7]],
        index=[0, 1],
        columns=['fakeWavelength', 'fakeflux', 'objID', 'fiberID'])
    with pytest.raises(ValueError, match="The DataFrame must contain 'Wavelength' and 'flux' columns."):
        plot(invalid_df_no_flux_or_wavelength)

def test_plot_valid_input():      
    # Valid DataFrame
    single_point_df = pd.DataFrame([[1, 8, 3, 10]], columns=['Wavelength', 'flux', 'objID', 'fiberID'])
    with patch('matplotlib.pyplot.show') as mock_show:
        result = plot(single_point_df)
        assert result
        
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], plt.Figure)
    assert isinstance(result[1], plt.Axes)


