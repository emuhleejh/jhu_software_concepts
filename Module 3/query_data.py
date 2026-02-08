import psycopg
import json

class Query():
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

    def run_query(self):
        connection = psycopg.connect(dbname = self.dbname, user = self.user, password = self.password)

        with connection.cursor() as c:
            
            # Count of entries that have applied for Fall 2026
            c.execute("""SELECT COUNT(p_id)
                    FROM results
                    WHERE term = 'Fall 2026';
                    """)   
            row = c.fetchone()
            self.ct_applicants_f26 = row[0]
            
            # Percentage of entries from international students
            c.execute("""SELECT us_or_international, COUNT(p_id)
                    FROM results
                    GROUP BY us_or_international
                    ORDER BY us_or_international desc;
                    """)
            rows = c.fetchall()
        #     print(rows)
            intl, us = rows[0][1], rows[1][1]
            self.pct_intl = round(100 * intl / (us + intl), 2)
            
            # Average GPA, GRE, GRE V, and GRE AW of applicants
            c.execute("""SELECT avg(gpa), avg(gre), avg(gre_v), avg(gre_aw)
                    FROM results;
                    """)
            row = c.fetchone()
            self.avg_gpa, self.avg_gre, self.avg_gre_v, self.avg_gre_aw = row[0], row[1], row[2], row[3]

            # Average GPA of American students in Fall 2026
            c.execute("""SELECT avg(gpa)
                    FROM results
                    WHERE term = 'Fall 2026' AND us_or_international = 'American';
                    """)
            row = c.fetchone()
            self.avg_us_gpa_f26 = row[0]
            
            # Percent of entries in Fall 2025 that are Acceptances
            c.execute("""SELECT status, COUNT(p_id)
                    FROM results
                    WHERE term = 'Fall 2025'
                    GROUP BY status
                    ORDER BY status asc;
                    """)
            row = c.fetchall()
            accepted, all_others = row[0][1], (row[1][1] + row[2][1] + row[3][1])
            self.pct_accepted_f25 = round(100 * accepted / (accepted + all_others), 2)
            
            # Average GPA of accepted students in Fall 2026
            c.execute("""SELECT avg(gpa)
                    FROM results
                    WHERE term = 'Fall 2026' AND status = 'accepted';
                    """)
            row = c.fetchone()
            self.avg_accept_gpa_f26 = row[0]

            # Count of applicants to JHU for a Masters in Computer Science
            c.execute("""SELECT COUNT(p_id)
                    FROM results
                    WHERE degree = 'Masters' AND degree IN ('Computer Science') AND program IN ('Johns Hopkins');
                    """)
            row = c.fetchone()
            self.ct_jhu_ms_cs = row[0]

            # Count of applicants to selected universities for a PhD in Computer Science
            c.execute("""SELECT COUNT(p_id)
                    FROM results
                    WHERE degree = 'PhD' AND program IN ('Computer Science') AND program IN ('Georgetown', 'MIT', 'Stanford', 'Carnegie Mellon');
                    """)
            row = c.fetchone()
            self.ct_select_phd_cs = row[0]

            # Count of applicants to selected universities for a PhD in Computer Science using LLM answers
            c.execute("""SELECT COUNT(p_id)
                    FROM results
                    WHERE degree = 'PhD' AND llm_generated_program IN ('Computer Science') AND llm_generated_university IN ('Georgetown', 'MIT', 'Stanford', 'Carnegie Mellon');
                    """)
            row = c.fetchone()
            self.ct_select_phd_cs_llm = row[0]

            # Program with the most acceptances
            c.execute("""SELECT llm_generated_program, COUNT(p_id) as total_count
                    FROM results
                    WHERE status = 'Accepted'
                    GROUP BY llm_generated_program
                    ORDER BY total_count desc;
                    """)
            row = c.fetchone()
            self.prog_most_accept, self.prog_accept_ct = row[0], row[1]

            # Program with the most rejections
            c.execute("""SELECT llm_generated_program, COUNT(p_id) as total_count
                    FROM results
                    WHERE status = 'Rejected'
                    GROUP BY llm_generated_program
                    ORDER BY total_count desc;
                    """)
            row = c.fetchone()
            self.prog_most_reject, self.prog_reject_ct = row[0], row[1]

            # University with the most acceptances
            c.execute("""SELECT llm_generated_university, COUNT(p_id) as total_count
                    FROM results
                    WHERE status = 'Accepted'
                    GROUP BY llm_generated_university
                    ORDER BY total_count desc;
                    """)
            row = c.fetchone()
            self.uni_most_accept, self.uni_accept_ct = row[0], row[1]

            # University with the most rejections
            c.execute("""SELECT llm_generated_university, COUNT(p_id) as total_count
                    FROM results
                    WHERE status = 'Rejected'
                    GROUP BY llm_generated_university
                    ORDER BY total_count desc;
                    """)
            row = c.fetchone()
            self.uni_most_reject, self.uni_reject_ct = row[0], row[1]

            connection.commit()

        c.close()
        connection.close()

        return self
