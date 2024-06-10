import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import storage

st.set_page_config(layout="wide")

st.title('Fixtures & Results')
st.write('''
Here you can see the results of the past games and check what games are yet to be played.
''')

creds = service_account.Credentials.from_service_account_file('/Users/jakubpaczusko/Desktop/gcp/eurobox24/.streamlit/eurobox24-9e51d9d0d968.json')
client = storage.Client(project='eurobox24', credentials=creds)

def add_custom_sort(x):
    if x == 'FT':
        return 0
    elif x == 'PST':
        return 1
    else:
        return 2

@st.cache_data
def get_fixtures_and_results(foo=1):
    
    df = pd.read_csv(
        '/Users/jakubpaczusko/Desktop/gcp/eurobox24/data/fixtures.csv',
        # 'gs://eurobox24/data/fixtures.csv',
        # storage_options={'token':'/Users/jakubpaczusko/Desktop/gcp/eurobox24/.streamlit/eurobox24-9e51d9d0d968.json'},
        parse_dates=['fixture.date']
    )

    return df

RAW_FIXTURES = get_fixtures_and_results()

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
