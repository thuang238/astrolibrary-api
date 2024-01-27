# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Make the src/ directory the target
sys.path.insert(0, os.path.abspath("../../src"))

project = "astrolibrary"
copyright = "2023, team15_2023"
author = "team15_2023"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "__pycache__"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# ------- Option 1: default sphinx theme -------
# html_theme = "pyramid"

# ------- Option 2: readthedocs theme -------
import sphinx_rtd_theme

pygments_style = "sphinx"
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# ------- Option 3: Others?  -------


html_static_path = ["_static"]
