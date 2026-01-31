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

    def __str__(self):
        return (f"Program: {self.program}\n" +
                f"University: {self.university}\n" +
                f"Comments: {self.comments}\n" + 
                f"Date added: {self.date_added}\n"
                f"URL: {self.results_url}\n" +
                f"Applicant status: {self.applicant_status}\n" +
                f"Acceptance date: {self.acceptance_date}\n" +
                f"Rejection date: {self.rejection_date}\n" +
                f"Program start: {self.program_start}\n" +
                f"Location: {self.location}\n" +
                f"GRE: {self.gre}\n" +
                f"GRE V: {self.gre_v}\n" +
                f"Degree: {self.degree}\n" +
                f"GPA: {self.gpa}\n" +
                f"GRE AW: {self.gre_aw}\n")