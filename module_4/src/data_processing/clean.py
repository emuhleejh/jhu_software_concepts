import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import subprocess

# Class Clean to handle data processed in from 'filename' file
class Clean():
    """
    Cleans given data by processing it through a local LLM.

    :param filename: File name to be run through LLM
    """
    def __init__(self, filename):
        self.filename = filename

    # Runs 'filename' file through local LLM 'app.py'
    def clean_data(self):
        """
        Function runs file through local LLM to auto-detect programs and universities for each row. \
        Creates a .txt file with original data and extended generated data.
        """

        subprocess.call(["py", "src/llm_hosting/app.py", "--file", self.filename, "--out", "llm_extend_applicant_data.txt"])