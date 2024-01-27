""" TODO: Add module docstring.

The numpy's main module docstring is a good example to follow:
https://github.com/numpy/numpy/blob/main/numpy/__init__.py

"""
from .data_acquisition.query_interface import QueryHandler
from .data_acquisition.query_interface.cross_matching import cross_match
from .data_acquisition.spectra_data_retrieval import get_spectra_data
from .data_processing.data_preprocessing import DataPreprocessing
from .data_acquisition.query_interface.cross_matching import cross_match
from .data_visualization.spectral_visualization import plot
from .data_processing.metadata_extractor import MetaDataExtractor
from .data_manipulation.machine_learning import MachineLearning

__all__ = [
    "QueryHandler",
    "get_spectra_data",
    "DataPreprocessing",
    "cross_match",
    "MetaDataExtractor",
    "plot",
    "MachineLearning",
]
