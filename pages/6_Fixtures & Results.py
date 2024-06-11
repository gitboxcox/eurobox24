import streamlit as st
import pandas as pd
from utils.utils import *

@st.cache_data
def get_fixtures(foo=1):
    fixtures = read_fixtures()
    return fixtures

def add_custom_sort(x):
    if x == 'FT':
        return 0
    elif x == 'PST':
        return 1
    else:
        return 2


st.title('Fixtures & Results')
st.write('''
Here you can see the results of the past games and check what games are yet to be played.
''')

RAW_FIXTURES = get_fixtures()

cols_to_show = ['fixture.date_nice', 'fixture.gameday.name', 'fixture.venue.name', 'teams.home.name', 'goals.home', 'goals.away', 'teams.away.name']
renames = ['Date', 'Gameday', 'Stadium', 'Home Team', 'Home Team Score', 'Away Team Score', 'Away Team']
renames_dict = dict(zip(cols_to_show, renames))

st.subheader('Results')
st.write('Finished games with scores')
st.dataframe(
    RAW_FIXTURES.loc[RAW_FIXTURES['fixture.status.short'].isin(['FT', 'AET', 'PEN']), cols_to_show].rename(columns=renames_dict),
    use_container_width=True,
    hide_index=True
)

st.subheader('Fixtures')
st.write('Games yet to be played with scheduled date')
st.dataframe(
    RAW_FIXTURES.loc[RAW_FIXTURES['fixture.status.short']=='NS', cols_to_show].rename(columns=renames_dict),
    use_container_width=True,
    hide_index=True
)

st.subheader('Live')
st.write('Postponed games that do not have a new scheduled date')
live_status = ['1H', 'HT', '2H', 'ET', 'BT', 'P', 'SUSP', 'INT']
st.dataframe(
    RAW_FIXTURES.loc[RAW_FIXTURES['fixture.status.short'].isin(live_status), cols_to_show].rename(columns=renames_dict),
    use_container_width=True,
    hide_index=True
)
