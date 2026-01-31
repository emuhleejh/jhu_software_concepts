import subprocess

# Class Clean to handle data processed in from 'filename' file
class Clean():
    def __init__(self, filename):
        self.filename = filename

    # Runs 'filename' file through local LLM 'app.py'
    def llm_clean(self):
        subprocess.call(["py", "llm_hosting/app.py", "--file", self.filename, "--out", "llm_extend_applicant_data.json"])