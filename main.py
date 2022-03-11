import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.utils import median_survival_times

# Create a SQL connection to our SQLite database
con_2021 = sqlite3.connect("./db/drive_stats_2021.db")
con_2020 = sqlite3.connect("./db/drive_stats_2020.db")
con_2019 = sqlite3.connect("./db/drive_stats_2019.db")
# con = sqlite3.connect("./db/drive_stats_2021_q3.db")
# con = sqlite3.connect("./db/drive_stats_2021_q4.db")
# con = sqlite3.connect('./db/testdb.db')

cur_2021 = con_2021.cursor()
cur_2020 = con_2020.cursor()
cur_2019 = con_2019.cursor()

# sel = ['capacity_bytes', 'failure', 'smart_1_normalized', 'smart_4_raw', 'smart_5_raw', 'smart_9_raw', 'smart_187_raw', 'smart_188_raw', 'smart_193_raw', 'smart_197_raw', 'smart_198_raw', 'smart_240_raw', 'smart_241_raw', 'smart_242_raw']
sel = ['failure', 'model', 'smart_5_raw', 'smart_9_raw', 'smart_187_raw', 'smart_188_raw', 'smart_197_raw', 'smart_198_raw']#'smart_9_raw']

remove_blanks = " AND ".join([col + ' != "" AND ' + col + ' IS NOT NULL' for col in sel]) #+ ' AND smart_9_raw < 72500'
data_2021_q1 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2021_q1 WHERE {remove_blanks};', con_2021)
data_2021_q2 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2021_q3 WHERE {remove_blanks};', con_2021)
data_2021_q3 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2021_q2 WHERE {remove_blanks};', con_2021)
data_2021_q4 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2021_q4 WHERE {remove_blanks};', con_2021)
print('=====2021 DATA LOADED=====')

data_2021_frames = [data_2021_q1, data_2021_q2, data_2021_q3, data_2021_q4]
data_2021 = pd.concat(data_2021_frames)

data_2020_q1 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2020_q1 WHERE {remove_blanks};', con_2020)
data_2020_q2 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2020_q3 WHERE {remove_blanks};', con_2020)
data_2020_q3 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2020_q2 WHERE {remove_blanks};', con_2020)
data_2020_q4 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2020_q4 WHERE {remove_blanks};', con_2020)
print('=====2020 DATA LOADED=====')

data_2020_frames = [data_2020_q1, data_2020_q2, data_2020_q3, data_2020_q4]
data_2020 = pd.concat(data_2020_frames)

data_2019_q1 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2019_q1 WHERE {remove_blanks};', con_2019)
data_2019_q2 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2019_q3 WHERE {remove_blanks};', con_2019)
data_2019_q3 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2019_q2 WHERE {remove_blanks};', con_2019)
data_2019_q4 = pd.read_sql_query(f'SELECT {", ".join(sel)} from drive_stats_2019_q4 WHERE {remove_blanks};', con_2019)
print('=====2019 DATA LOADED=====')

data_2019_frames = [data_2019_q1, data_2019_q2, data_2019_q3, data_2019_q4]
data_2019 = pd.concat(data_2021_frames)

# con_2021.close()
# con_2020.close()
# con_2019.close()

print(data_2021.head(1))
print(data_2020.head(1))
print(data_2019.head(1))

# data_2019_q1.loc[(data_2019_q1['model'].str.startswith('ST', na=False)) | (data_2019_q1['model'].str.startswith('Seagate', na=False))].sum()
# data_2019_q1.loc[(data_2019_q1['model'].str.startswith('WD', na=False))].sum()
# data_2019_q1.loc[(data_2019_q1['model'].str.startswith('HGST', na=False))].sum()
# data_2019_q1.loc[(data_2019_q1['model'].str.startswith('TOSHIBA', na=False))].sum()
data_of_interest = 'smart_5_raw'

data_2021_filt = data_2021.loc[(data_2021[data_of_interest] != '') & (data_2021['smart_9_raw'] != '')]# & (data_2021['failure'] == 1)] #"smart_9_raw"]
T_2021 = data_2021_filt[data_of_interest]
E_2021 = data_2021_filt["failure"]
plt.hist(T_2021, bins = 240, alpha=0.5, label='2021')

data_2020_filt = data_2020.loc[(data_2020[data_of_interest] != '') & (data_2020['smart_9_raw'] != '')]# & (data_2020['failure'] == 1)] #"smart_9_raw"]
T_2020 = data_2020_filt[data_of_interest]
E_2020 = data_2020_filt["failure"]
plt.hist(T_2020, bins = 240, alpha=0.5, label='2020')

data_2019_filt = data_2019.loc[(data_2019[data_of_interest] != '') & (data_2019['smart_9_raw'] != '')]# & (data_2019['failure'] == 1)] #"smart_9_raw"]
T_2019 = data_2019_filt[data_of_interest]
E_2019 = data_2019_filt["failure"]
plt.hist(T_2019, bins = 240, alpha=0.5, label='2019')

plt.title("Data Time Distribution")
plt.xlabel('Hours')
plt.legend(loc='upper right')
plt.show()

kmf_2021 = KaplanMeierFitter()
kmf_2021.fit(durations = T_2021, event_observed = E_2021)

kmf_2020 = KaplanMeierFitter()
kmf_2020.fit(durations = T_2020, event_observed = E_2020)

kmf_2019 = KaplanMeierFitter()
kmf_2019.fit(durations = T_2019, event_observed = E_2019)

kmf_2021.plot_survival_function(label='2021')
kmf_2020.plot_survival_function(label='2020')
kmf_2019.plot_survival_function(label='2019')
plt.title('Survival function')
plt.xlabel('Hours')
plt.show()

# kmf_2021.survival_function_.plot()
# plt.title('Survival function')
# plt.xlabel('Hours')

kmf_2021.plot_cumulative_density()
plt.title('Cumulative Failure Curve')
plt.show()

median_ = kmf_2021.median_survival_time_
median_confidence_interval_ = median_survival_times(kmf_2021.confidence_interval_)
print(median_)
print(median_confidence_interval_)
print(len(T_2021))

# cph = CoxPHFitter(penalizer=0.0000000000001)
# cph.fit(data, duration_col = 'smart_9_raw', event_col = 'failure', show_progress=True)
# cph.print_summary()
# Be sure to close the connection
