import sqlite3
import pandas as pd
from lifelines import CoxPHFitter

# Create a SQL connection to our SQLite database
con = sqlite3.connect("./db/testdb.db")

cur = con.cursor()

sel = ['capacity_bytes', 'failure', 'smart_1_normalized', 'smart_3_normalized', 'smart_4_raw', 'smart_5_raw', 'smart_7_normalized', 'smart_9_raw', 'smart_10_raw', 'smart_12_raw', 'smart_187_raw', 'smart_188_raw', 'smart_190_normalized', 'smart_192_raw', 'smart_193_raw', 'smart_194_raw', 'smart_197_raw', 'smart_198_raw', 'smart_200_raw', 'smart_240_raw', 'smart_241_raw', 'smart_242_raw']
rows = list(cur.execute('PRAGMA table_info(drive_stats_2021_q4);'))
# sel.extend([row[1] for row in rows[0:5] if row[1] not in ['serial_number', 'model', 'date']])
# # The result of a "cursor.execute" can be iterated over by row
# for row in rows:
#     if 'normalized' in row[1]:
#         sel.append(row[1])
# sel.append('smart_9_raw')
# sel.remove('smart_9_normalized')
remove_blanks = " AND ".join([col + ' != "" AND ' + col + ' IS NOT NULL' for col in sel])
data = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2021_q4 WHERE {remove_blanks} ;', con)
con.close()
print(data.head(1))
cph = CoxPHFitter(penalizer=0.00000000001)
cph.fit(data, duration_col = 'smart_9_raw', event_col = 'failure')
cph.print_summary()
# Be sure to close the connection
