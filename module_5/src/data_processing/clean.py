"""
Module hosts function to clean data from file.
"""

import subprocess
import sys

from os.path import dirname
sys.path.append(dirname(__file__))

# Function clean to handle data processed in from 'filename' file
def clean(filename):
    """
    Function runs file through local LLM to auto-detect programs \
        and universities for each row. Creates a .txt file with \
                original data and extended generated data.

    :param filename: File name to be run through LLM
    :type filename: str
    """

    subprocess.call(["py", "src/llm_hosting/app.py", "--file", \
                        filename, "--out", "llm_extend_applicant_data.txt"])
