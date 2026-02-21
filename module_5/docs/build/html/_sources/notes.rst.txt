Operational Notes
======================
Busy-state Policy
-----------------------
While the program is busy pulling data or updating the analysis, the system will disable the ability to request another pull or another update.

Deduplication Strategy
-----------------------
Before inserting an entry into the database, the program checks to see if it has already been entered into the database using the URL for the entry, which is unique for each entry and can be treated as a Unique ID.