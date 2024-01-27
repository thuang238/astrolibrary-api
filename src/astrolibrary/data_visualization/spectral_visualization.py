import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import uniform_filter1d

"""
Data Visualization Module:
    Provides a matplotlib-based interface for spectral visualization with an overlay of the
    inferred continuum
"""


def plot (data, window_size = 1):
    """
        Parameters
        ----------
        data: pd.DataFrame
            Dataframe containing spectral data from the SDSS catalog

        attributes: list 
            List of attributes that will be extracted from the 'data' dictionary

        Returns 
        ----------
        A matplotlib that displays the spectral data with inferred continuum

        Examples
        ---------
        >>> data = pd.DataFrame(
                        {
                            "wavelength": np.array([1,2,3,4]),
                            "flux": np.array([1,2,3,4]),
                            # More stuff
                        }
        >>> vs = Visualizer(type="Inferred Continuum")

        # This should plot/show the graph, without saving x
        >>> vs.plot_spectra(data, window_size = 0.5, should_plot=True) 

        # This should save plot and return filename, without plotting it
        >>> vs.plot_spectra(data, type="Inferred Continuum", should_plot=False)  
        )
    """
    if window_size < 1:
        raise ValueError("Window size must be greater than or equal to 1.")
    
    # Extract meta data
    try:
        wavelength = data['Wavelength']
        flux= data['flux']
    except KeyError as e:
        raise ValueError(f"The DataFrame must contain 'Wavelength' and 'flux' columns. Error: {e}")


    # Add inferred continuum 
    continuum = uniform_filter1d(flux, size=window_size)

    # Plot the data 
    fig, ax = plt.subplots()
    ax.plot(wavelength, flux, label='Spectrum')
    ax.plot(wavelength, continuum, label='Inferred Continuum', linestyle='--', color='blue')
    
    # Label axes and add title
    ax.set_title('Spectral Visualization')
    ax.set_xlabel('Wavelength')
    ax.set_ylabel('Flux')
    ax.legend()
    
    plt.show()

    return fig, ax

