"""
Tools for analysing wind speed data from crete

Data can be downloaded from
https://mesonet.agron.iastate.edu/sites/locate.php?network=GR__ASOS
The file format is known as asos
station,valid, tmpc ,  drct ,  sknt ,  gust
LGIR,2011-08-22 19:20,25.00,320.00,12.00,M
LGSA,2011-08-22 19:20,24.00,0.00,0.00,M

The fields are location, date, temperature c, direction, speed and gust kts
There are other fields available.
"""

import matplotlib
# sudo apt-get install tcl-dev tk-dev python-tk python3-tk
# had to install ipykernel due ImportError: No module named 'ipykernel'
matplotlib.use('TkAgg')  # make perm  by reinstalling matplotlib
import numpy as np
# matplotlib.get_backend()
import matplotlib.pyplot as plt
import pandas



df = pandas.read_csv(
    'asos_winds.csv',
    # header=5, older file had a header
    na_values=['M'],
    parse_dates=[1]
)
df.columns = [x.lower().strip() for x in df.columns]
print(df.info())
# Some windpseeds are very large - remove them
bad = df['sknt'] > 100
print('sknt>100\n', df.loc[bad, 'sknt'], 'end')
df.loc[bad, 'sknt'] = np.nan
# Some gust speeds are very large - remove them
bad = df['gust'] > 100
print('gust>100\n', df.loc[bad, 'gust'], df[bad], 'end')
df.loc[bad, 'gust'] = np.nan

df['date'] = df['valid'].dt.strftime('%d %b')
df['minuteofyear'] =\
    (df['valid'].dt.dayofyear * 24 + df['valid'].dt.hour) * 60 \
    + df['valid'].dt.minute

cols_to_write = ['valid', 'tmpc', 'drct', 'sknt',
                 'gust', 'date', 'minuteofyear']

for filename in df['station'].unique():
    sel = df['station'] == filename
    df[sel][cols_to_write].to_csv(
        '~/Projects/crete/%s.csv' % filename,
        index=False
    )

print(df.info())
print(df.head())

df = pandas.read_csv(
    'LGIR.csv',
    na_values=['M'],
    parse_dates=[0]
)

# df.sknt.plot()
# plt.show()
df['year'] = df['valid'].dt.year
df['month'] = df['valid'].dt.month
df['week'] = df['valid'].dt.week
df['day'] = df['valid'].dt.dayofyear

g = df.groupby(['day', 'year'])
weekly_averages = g.aggregate({'sknt': np.mean})
weekly_averages.plot()
plt.show()
#print(weekly_averages)


# df['sknt'].astype(float).plot()
# df['sknt'][:12].astype(float).plot()
# df['sknt'][:12].astype(float).plot()
# plt.show()
# df[mdfs]=np.nan
# df['sknt'].astype(float).plot()
# plt.show()
# df['tmpc'].astype(float).plot()
# tb=df['sknd']>100
# tb=df['sknt']>100
# tb=df['sknt']>'100'
# df[tb]
# df['valid']
# df['sknt']
# df['sknt'].unique()
# %history