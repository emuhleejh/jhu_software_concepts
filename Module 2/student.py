# Class Student for information gathered about a student
class Student():
    def __init__(self):
        self.program = ""
        self.university = ""
        self.comments = ""
        self.date_added = ""
        self.results_url = ""
        self.applicant_status = ""
        self.acceptance_date = ""
        self.rejection_date = ""
        self.program_start = ""
        self.location = ""
        self.gre = ""
        self.gre_v = ""
        self.degree = ""
        self.gpa = ""
        self.gre_aw = ""

    # Format stored data about each Student object
    def format(self):
        student_data = {"program": self.program,
                        "university": self.university,
                        "comments": self.comments,
                        "date_added": self.date_added,
                        "url": self.results_url,
                        "status": self.applicant_status,
                        "acceptance_date": self.acceptance_date,
                        "rejection_date": self.rejection_date,
                        "term": self.program_start,
                        "US/International": self.location,
                        "degree": self.degree,
                        "gpa": self.gpa,
                        "gre": self.gre,
                        "gre v": self.gre_v,
                        "gre aw": self.gre_aw
        }

        return student_data