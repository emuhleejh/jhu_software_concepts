import sys
from os.path import dirname
sys.path.append(dirname(__file__))

# Define the __all__ variable
__all__ = ["data_processing", "llm_hosting", "templates"]

# Import the submodules
from src import data_processing
from src import llm_hosting
from src import templates
