import streamlit as st
from utils.utils import *
from datetime import datetime
import time
import pytz

@st.cache_data
def get_fixtures(foo=1):
    fixtures = read_fixtures()
    return fixtures

@st.cache_data
def get_all_scored_preds(foo=1):
    df = read_all_scored_preds()
    return df

@st.cache_data
def get_last_pretournament_preds(foo=1):
    preds = read_all_pretournament()
    idx = preds.groupby('userId')['timestamp'].idxmax()
    preds = preds.loc[idx].reset_index(drop=True)
    preds = preds.drop(columns=['timestamp'])
    preds.columns = ['Player', 'Winner', '2nd Place', 'Top Scorer', 'MVP', "Lewandowski's goals", "Poland Exit Phase"]
    return preds

if 'fixtures' not in st.session_state:
    fixtures = get_fixtures(time.time())
    st.session_state['fixtures'] = fixtures
else:
    fixtures = st.session_state['fixtures']

if 'scored_preds' not in st.session_state:
    preds = get_all_scored_preds(time.time())
    st.session_state['scored_preds'] = preds
else:
    preds = st.session_state['scored_preds']

if 'pretour' not in st.session_state:
    pretour = get_last_pretournament_preds(time.time())
    st.session_state['pretour'] = pretour
else:
    pretour = st.session_state['pretour']

st.title('Dashboard')
st.write('''
Data here is updated every 15 minutes.  
Data about Hero Points is updated after given game is finished.
''')

#TODO: Punkty usera (Suma, Breakdown per Gameday)
#TODO: Tabela - punkty wszystkich zawodnikow
#TODO: Predykcje innych per Gameday
#TODO: Heros innych
#TODO: PreTour innych
#TODO: Najlepsi Heros

if 'user_info' not in st.session_state:
    st.write("### Log in on the **Hello** page")
else:

    st.write('Use this button to refresh the data')
    refresh = st.button(
        label='Refresh'
    )
    if refresh:
        fixtures = get_fixtures(time.time())
        st.session_state['fixtures'] = fixtures

        preds = get_all_scored_preds(time.time())
        st.session_state['scored_preds'] = preds

        pretour = get_last_pretournament_preds(time.time())
        st.session_state['pretour'] = pretour


    with st.expander('#### Your Points'):
        # SELECT GAMEDAY
        gameday = st.selectbox(
            label='Select Gameday',
            options=['All']+fixtures['fixture.gameday.name'].unique().tolist(),
            key='points-select-gameday'
        )

        # SELECT FIXTURE
        fixtures_to_show = ['All'] + fixtures.loc[fixtures['fixture.gameday.name']==gameday,'fixture.id'].to_list() if gameday != "All" else ['All'] + fixtures['fixture.id'].to_list()
        fixture = st.selectbox(
            label='Select Fixture',
            # options=['All']+fixtures.loc[fixtures['fixture.gameday.name']==gameday,'fixture.id'].to_list(),
            options=fixtures_to_show,
            format_func=lambda x: nice_fixture(fixtureId=x,fixtures=fixtures),
            key='points-select-fixture'
        )

        # FILTER FIXTURES
        if fixture != 'All':
            fixtures_to_filter = [fixture]
        elif gameday == 'All':
            fixtures_to_filter = fixtures['fixture.id'].to_list()
        else:
            fixtures_to_filter = fixtures.loc[fixtures['fixture.gameday.name']==gameday,'fixture.id'].to_list()

        # st.dataframe(read_all_scored_preds())
        st.write('Work In Progress')

    with st.expander("#### Players' Preds"):
        # SELECT USER
        # user = st.selectbox(
        #     label='Select Gameday',
        #     options=['All']+fixtures['fixture.gameday.name'].unique().tolist(),
        #     key='playerpreds-select-user'
        # )

        # # SELECT GAMEDAY
        # gameday = st.selectbox(
        #     label='Select Gameday',
        #     options=['All']+fixtures['fixture.gameday.name'].unique().tolist(),
        #     key='playerpreds-select-gameday'
        # )

        # SELECT FIXTURE
        # fixtures_to_show = ['All'] + fixtures.loc[fixtures['fixture.gameday.name']==gameday,'fixture.id'].to_list() if gameday != "All" else ['All'] + fixtures['fixture.id'].to_list()
        fixtures_to_show = fixtures['fixture.id'].to_list()
        fixture = st.selectbox(
            label='Select Fixture',
            # options=['All']+fixtures.loc[fixtures['fixture.gameday.name']==gameday,'fixture.id'].to_list(),
            options=fixtures_to_show,
            format_func=lambda x: nice_fixture(fixtureId=x,fixtures=fixtures),
            key='playerpreds-select-fixture'
        )

        # FILTER FIXTURES
        if fixture != 'All':
            fixtures_to_filter = [fixture]
        elif gameday == 'All':
            fixtures_to_filter = fixtures['fixture.id'].to_list()
        else:
            fixtures_to_filter = fixtures.loc[fixtures['fixture.gameday.name']==gameday,'fixture.id'].to_list()

        # st.dataframe(read_all_scored_preds())
        st.write('Work In Progress')

    with st.expander('#### Leaderboard'):
        st.selectbox(
            label='Select Gameday',
            options=['All']+fixtures['fixture.gameday.name'].unique().tolist(),
            key='leaderboard-select-gameday'
        )
        st.checkbox(
            label='Include Hero Points',
            value=False
        )
        st.write('Work In Progress')

    with st.expander('#### Pre-Torunament Preds'):
        if datetime.now(pytz.timezone("Europe/Warsaw")) > datetime(2024,6,14,19,0,tzinfo=pytz.timezone("Europe/Warsaw")):
            st.dataframe(pretour)
        st.write("You will be able to see other Players' Pre-Tournament Preds after the submission deadline")

    with st.expander('#### Best Heroes'):
        st.write('Work In Progress')