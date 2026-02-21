import sys
from os.path import dirname
sys.path.append(dirname(__file__))

project = 'module_4'
copyright = '2026, ehammer5'
author = 'ehammer5'
release = '1.0'

import os 
import sys
sys.path.insert(0, os.path.abspath(".."))

# -- General configuration ---------------------------------------------------
extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
