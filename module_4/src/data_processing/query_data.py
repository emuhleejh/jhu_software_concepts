import psycopg

class Query():
    """
    Docstring for Query
    """
    def __init__(self, dbname, user, password):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.ct_applicants_f26 = ""
        self.pct_intl = ""
        self.avg_gpa = ""
        self.avg_gre = ""
        self.avg_gre_v = ""
        self.avg_gre_aw = ""
        self.avg_us_gpa_f26 = ""
        self.pct_accepted_f25 = ""
        self.avg_accept_gpa_f26 = ""
        self.ct_jhu_ms_cs = ""
        self.ct_select_phd_cs = ""
        self.ct_select_phd_cs_llm = ""
        self.prog_most_accept = ""
        self.prog_accept_ct = ""
        self.prog_most_reject = ""
        self.prog_reject_ct = ""
        self.uni_most_accept = ""
        self.uni_accept_ct = ""
        self.uni_most_accept = ""
        self.uni_accept_ct = ""


    # Series of analysis SQL calls
    def run_query(self):
        """
        Queries data in database for analysis.
        """

        # Connect to database
        connection = psycopg.connect(dbname = self.dbname, 
                                     user = self.user, 
                                     password = self.password)

        with connection.cursor() as c:
            
            # Count of entries that have applied for Fall 2026
            c.execute("""SELECT COUNT(p_id)
                    FROM results
                    WHERE term = 'Fall 2026';
                    """)   
            row = c.fetchone()
            self.ct_applicants_f26 = row[0]
            print(f"Fall 2026 applicant count: {self.ct_applicants_f26}")
            
            # Percentage of entries from international students
            c.execute("""SELECT us_or_international, COUNT(p_id)
                    FROM results
                    GROUP BY us_or_international
                    ORDER BY us_or_international desc;
                    """)
            rows = c.fetchall()
            intl = 0
            us = 0
            for row in rows:
                if row[0] == "International":
                    intl = row[1]
                else:
                    us = row[1]
            if intl == 0 and us == 0:
                self.pct_intl = "0.00"
            else:
                self.pct_intl = f"{(100 * intl / (us + intl)):.2f}"
            print(f"Percent International: {self.pct_intl}")
            
            # Average GPA, GRE, GRE V, and GRE AW of applicants
            c.execute("""SELECT COALESCE(avg(gpa), 0), COALESCE(avg(gre), 0), COALESCE(avg(gre_v), 0), COALESCE(avg(gre_aw), 0)
                    FROM results;
                    """)
            row = c.fetchone()
            self.avg_gpa, self.avg_gre, self.avg_gre_v, self.avg_gre_aw = \
                f"{row[0]:.2f}", f"{row[1]:.2f}", f"{row[2]:.2f}", f"{row[3]:.2f}"
            print(f"Avg GPA: {self.avg_gpa}, Avg GRE: {self.avg_gre}, " 
                  f"Avg GRE V: {self.avg_gre_v}, Avg GRE AW: {self.avg_gre_aw}")

            # Average GPA of American students in Fall 2026
            c.execute("""SELECT COALESCE(avg(gpa), 0)
                    FROM results
                    WHERE term = 'Fall 2026' 
                      AND us_or_international = 'American';
                    """)
            row = c.fetchone()
            self.avg_us_gpa_f26 = f"{row[0]:.2f}"
            print(f"Average Fall 2026 American GPA: {self.avg_us_gpa_f26}")
            
            # Percent of entries in Fall 2025 that are Acceptances
            c.execute("""SELECT status, COUNT(p_id)
                    FROM results
                    WHERE term = 'Fall 2025'
                    GROUP BY status
                    ORDER BY status asc;
                    """)
            row = c.fetchall()
            
            accepted = 0
            all_others = 0
            length = len(row)
            
            if length >= 1:
                accepted = row[0][1]

            if length >= 2:
                all_others += row[1][1]

            if length >= 3:
                all_others += row[2][1]

            if length >= 4:
                all_others += row[3][1]
            
            if accepted == 0 and all_others == 0:
                self.pct_accepted_f25 = "0.00"
            else:
                self.pct_accepted_f25 = f"{(100 * accepted / (accepted + all_others)):.2f}"
            print(f"Fall 2025 acceptance percent: {self.pct_accepted_f25}%")
            
            # Average GPA of accepted students in Fall 2026
            c.execute("""SELECT COALESCE(avg(gpa), 0)
                    FROM results
                    WHERE term = 'Fall 2026' AND status = 'Accepted';
                    """)
            row = c.fetchone()
            if row is None:
                self.avg_accept_gpa_f26 = "0.00"
            else:
                self.avg_accept_gpa_f26 = f"{row[0]:.2f}"
            print(f"Average GPA acceptance: {self.avg_accept_gpa_f26}")

            # Count of applicants to JHU for a Masters in Computer Science
            c.execute("""SELECT COUNT(p_id)
                    FROM results
                    WHERE degree = 'Masters' 
                      AND program LIKE ('Computer Science%') 
                      AND (program LIKE ('%Johns Hopkins%') 
                      OR program LIKE ('%JHU%') 
                      OR program LIKE ('%Hopkins%'));
                    """)
            row = c.fetchone()
            self.ct_jhu_ms_cs = row[0]
            print(f"JHU Masters Computer Science count: {self.ct_jhu_ms_cs}")

            # Count of applicants to selected universities for a PhD in Computer Science
            c.execute("""SELECT COUNT(p_id)
                    FROM results
                    WHERE degree = 'PhD' 
                      AND program LIKE ('Computer Science%') 
                      AND (program LIKE ('%Georgetown%') 
                      OR program LIKE ('%MIT%') 
                      OR program LIKE ('%Stanford%') 
                      OR program LIKE ('%Carnegie%'));
                    """)
            row = c.fetchone()
            if row is None:
                self.ct_select_phd_cs = "0"
            else:
                self.ct_select_phd_cs = row[0]
            print(f"Selected university applicant count: {self.ct_select_phd_cs}")

            # Count of applicants to selected universities for a PhD in Computer Science using LLM answers
            c.execute("""SELECT COUNT(p_id)
                    FROM results
                    WHERE degree = 'PhD' 
                      AND llm_generated_program LIKE ('Computer Science%') 
                      AND (llm_generated_university LIKE ('%George town%') 
                      OR llm_generated_university LIKE ('%Massachusetts Institute of Technology%') 
                      OR llm_generated_university LIKE ('%Stanford%') 
                      OR llm_generated_university LIKE ('%Carnegie%'));
                    """)
            row = c.fetchone()
            if row is None:
                self.ct_select_phd_cs_llm = "0"
            else:
                self.ct_select_phd_cs_llm = row[0]
            print(f"Selected university applicant count via LLM: {self.ct_select_phd_cs_llm}")

            # Program with the most acceptances
            c.execute("""SELECT llm_generated_program, COUNT(p_id) as total_count
                    FROM results
                    WHERE status = 'Accepted'
                    GROUP BY llm_generated_program
                    ORDER BY total_count desc;
                    """)
            row = c.fetchone()
            if row is None:
                self.prog_most_accept = "None" 
                self.prog_accept_ct = "0"
            else:
                self.prog_most_accept, self.prog_accept_ct = row[0], row[1]
            print(f"Program with most acceptances: {self.prog_most_accept}, {self.prog_accept_ct}")

            # Program with the most rejections
            c.execute("""SELECT llm_generated_program, COUNT(p_id) as total_count
                    FROM results
                    WHERE status = 'Rejected'
                    GROUP BY llm_generated_program
                    ORDER BY total_count desc;
                    """)
            row = c.fetchone()
            if row is None:
                self.prog_most_reject = "None"
                self.prog_reject_ct = "0"
            else:
                self.prog_most_reject, self.prog_reject_ct = row[0], row[1]
            print(f"Program with most rejections: {self.prog_most_reject}, {self.prog_reject_ct}")

            # University with the most acceptances
            c.execute("""SELECT llm_generated_university, COUNT(p_id) as total_count
                    FROM results
                    WHERE status = 'Accepted'
                    GROUP BY llm_generated_university
                    ORDER BY total_count desc;
                    """)
            row = c.fetchone()
            if row is None:
                self.uni_most_accept = "None"
                self.uni_accept_ct = "0"
            else:
                self.uni_most_accept, self.uni_accept_ct = row[0], row[1]
            print(f"University with most acceptances: {self.uni_most_accept}, {self.uni_accept_ct}")

            # University with the most rejections
            c.execute("""SELECT llm_generated_university, COUNT(p_id) as total_count
                    FROM results
                    WHERE status = 'Rejected'
                    GROUP BY llm_generated_university
                    ORDER BY total_count desc;
                    """)
            row = c.fetchone()
            if row is None:
                self.uni_most_reject = "None"
                self.uni_reject_ct = "0"
            else:
                self.uni_most_reject, self.uni_reject_ct = row[0], row[1]
            print(f"University with most rejections: {self.uni_most_reject}, {self.uni_reject_ct}")

            connection.commit()

        c.close()
        connection.close()

        return self
