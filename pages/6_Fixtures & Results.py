import streamlit as st
import pandas as pd
from st_files_connection import FilesConnection

st.set_page_config(layout="wide")
conn = st.connection('gcs', type=FilesConnection)

@st.cache_data
def get_fixtures(foo=1):
    fixtures = conn.read('eurobox24/data/fixtures.csv', input_format='csv')
    fixtures['fixture.date'] = pd.to_datetime(fixtures['fixture.date'])
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
    RAW_FIXTURES.loc[RAW_FIXTURES['fixture.status.short']=='FT', cols_to_show].rename(columns=renames_dict),
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

st.subheader('Postponed')
st.write('Postponed games that do not have a new scheduled date')
st.dataframe(
    RAW_FIXTURES.loc[RAW_FIXTURES['fixture.status.short']=='PST', cols_to_show].rename(columns=renames_dict),
    use_container_width=True,
    hide_index=True
)
