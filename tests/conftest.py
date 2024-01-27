import os
import sys

# Add the src directory to the PYTHONPATH
# This allows us to import the modules from src in the tests since
# `conftest.py` is executed before the tests are run.
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)
