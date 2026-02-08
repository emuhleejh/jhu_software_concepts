import subprocess

# Class Clean to handle data processed in from 'filename' file
class Clean():
    def __init__(self, filename):
        self.filename = filename

    # Runs 'filename' file through local LLM 'app.py'
    def clean_data(self):
        subprocess.call(["py", "app/llm_hosting/app.py", "--file", self.filename, "--out", "llm_extend_applicant_data1.txt"])