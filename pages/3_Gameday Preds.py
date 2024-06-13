import streamlit as st
import pandas as pd
import numpy as np
from utils.utils import *
from datetime import datetime
import pytz

@st.cache_data
def get_fixtures(foo=1):
    fixtures = read_fixtures()
    return fixtures

@st.cache_data
def get_squads(foo=1):
    squads = read_squads()
    return squads

@st.cache_data
def get_preds(foo=1):
    preds = read_all_preds()
    return preds

@st.cache_data
def get_latest_preds(preds, foo=1):
    idx = preds.groupby(['userId', 'fixtureId'])['timestamp'].idxmax()
    latest_preds = preds.loc[idx]
    return latest_preds

@st.cache_data
def get_latest_user_preds(latest_preds, userId):
    latest_user_preds = latest_preds.loc[latest_preds['userId']==userId]
    return latest_user_preds

st.write('''
# Gameday Preds 
#### Use this page to submitt predictions for each gameday. You can check your points, position, as well as other players' predictions on the Dashboard page.
---
''')

if 'user_info' not in st.session_state:
    st.write("### Log in on the **Hello** page")
else:

    if 'data' not in st.session_state:
        RAW_FIXTURES = get_fixtures()
        SQUADS = get_squads()
        RAW_PREDS = get_preds(time.time())
        LATEST_PREDS = get_latest_preds(RAW_PREDS, time.time())
        st.session_state['data'] = {'raw_fixtures':RAW_FIXTURES, 'squads':SQUADS, 'raw_preds':RAW_PREDS, 'latest_preds':LATEST_PREDS}
    else:
        RAW_FIXTURES, SQUADS, RAW_PREDS, LATEST_PREDS = st.session_state['data']['raw_fixtures'], st.session_state['data']['squads'], st.session_state['data']['raw_preds'], st.session_state['data']['latest_preds']

    # USER_PREDS = get_latest_user_preds(LATEST_PREDS, st.session_state['user_info']['localId'])
            
    st.write("If you cannot see your latest predictions, use the button below to refresh data")
    refresh = st.button(label='Refresh', key='refresh')
    if refresh:
        RAW_FIXTURES = get_fixtures(time.time())
        SQUADS = get_squads(time.time())
        RAW_PREDS = get_preds(time.time())
        LATEST_PREDS = get_latest_preds(RAW_PREDS, time.time())
        st.session_state['data'] = {'raw_fixtures':RAW_FIXTURES, 'squads':SQUADS, 'raw_preds':RAW_PREDS, 'latest_preds':LATEST_PREDS}
        # USER_PREDS = get_latest_user_preds(LATEST_PREDS, st.session_state['user_info']['localId'], time.time())

    USER_PREDS = get_latest_user_preds(LATEST_PREDS, st.session_state['user_info']['localId'])

    available_gamedays = RAW_FIXTURES.loc[pd.to_datetime(RAW_FIXTURES['fixture.date']).dt.tz_localize(None)-pd.Timedelta(hours=2)>pd.to_datetime('now'), 'fixture.gameday.name'].unique().tolist()

    gameday = st.selectbox(
        label='Select a Gameday from this list',
        options=available_gamedays
    )

    GAMEDAY_FIXTURES = RAW_FIXTURES.loc[RAW_FIXTURES['fixture.gameday.name']==gameday]

    st.write('Games during selected Gameday:')
    GAMEDAY_FIXTURES_SHOW = GAMEDAY_FIXTURES.merge(USER_PREDS, how='left', left_on='fixture.id', right_on='fixtureId')
    GAMEDAY_FIXTURES_SHOW['is.predicted'] = np.where(GAMEDAY_FIXTURES_SHOW['userId'].isna(), 'NOT PREDICTED ❌', 'PREDICTED ✅')
    GAMEDAY_FIXTURES_SHOW = GAMEDAY_FIXTURES_SHOW.rename(columns={'ftts_x':'ftts_act', 'fpts_x':'fpts_act', 'ftts_y':'ftts', 'fpts_y':'fpts'})
    cols_to_show = ['fixture.date_nice', 'teams.home.name', 'teams.away.name', 'is.predicted', 'hts', 'ats', 'ftts', 'fpts']
    renames = ['Date', 'Home Team', 'Away Team', 'Did you predict?', 'Home Team Score', 'Away Team Score', 'First Team to Score', 'First Player to Score']
    renames_dict = dict(zip(cols_to_show, renames))

    st.dataframe(
        GAMEDAY_FIXTURES_SHOW[cols_to_show].rename(columns=renames_dict),
        hide_index=True
    )

    st.write(f'''
    **DEADLINE FOR SUBMITTING**:   
    {GAMEDAY_FIXTURES['fixture.gameday.deadline'].iloc[0]}
    ''')

    st.write("---")

    _, _column, _ = st.columns([1,3,1])
    with _column:

        st.write('## Predict!')

        for id in GAMEDAY_FIXTURES['fixture.id'].to_list():

            home_team_name, away_team_name = GAMEDAY_FIXTURES.loc[GAMEDAY_FIXTURES['fixture.id']==id,'teams.home.name'].iloc[0], GAMEDAY_FIXTURES.loc[GAMEDAY_FIXTURES['fixture.id']==id,'teams.away.name'].iloc[0]
            home_team_id, away_team_id = GAMEDAY_FIXTURES.loc[GAMEDAY_FIXTURES['fixture.id']==id,'teams.home.id'].iloc[0], GAMEDAY_FIXTURES.loc[GAMEDAY_FIXTURES['fixture.id']==id,'teams.away.id'].iloc[0]
            gameday_deadline = GAMEDAY_FIXTURES.loc[GAMEDAY_FIXTURES['fixture.id']==id, 'fixture.gameday.deadline'].iloc[0]

            with st.expander(f"{GAMEDAY_FIXTURES.loc[GAMEDAY_FIXTURES['fixture.id']==id,'teams.home.name'].iloc[0]} :crossed_swords: {GAMEDAY_FIXTURES.loc[GAMEDAY_FIXTURES['fixture.id']==id,'teams.away.name'].iloc[0]}"):

                # st.write(gameday_deadline)
                form_key = str(id)

                with st.form(form_key):

                    hts = st.number_input(label=home_team_name, min_value=0)
                    ats = st.number_input(label=away_team_name, min_value=0)
                    ftts = st.selectbox(
                        label='First Team to Score', 
                        options=[home_team_name, away_team_name, 'No Goals'],
                        key=f"ftts-{form_key}"
                    )

                    fixture_players = SQUADS.loc[SQUADS['team.id']==home_team_id, 'player.name'].to_list() + SQUADS.loc[SQUADS['team.id']==away_team_id, 'player.name'].to_list()
                    fpts = st.selectbox(
                        label='First Player to Score',
                        options=fixture_players + ['Own Goal', 'No Goals']
                    )

                    submit = st.form_submit_button("Submit")
                    if submit:
                        # check if after deadline
                        cest = pytz.timezone('Europe/Warsaw')
                        if datetime.now(cest) > datetime(
                            gameday_deadline.year,
                            gameday_deadline.month,
                            gameday_deadline.day,
                            gameday_deadline.hour,
                            gameday_deadline.minute,
                            tzinfo=cest
                        ):
                            st.error('Too late bro')
                        else:
                            row_to_insert = {
                                "userId": st.session_state['user_info']['localId'],
                                "fixtureId": id,
                                "hts": hts,
                                "ats": ats,
                                "ftts": ftts,
                                "fpts": fpts,
                                "timestamp": time.time()
                            }
                            send_to_bq('preds', row_to_insert)
                            RAW_FIXTURES = get_fixtures(time.time())
                            SQUADS = get_squads(time.time())
                            RAW_PREDS = get_preds(time.time())
                            LATEST_PREDS = get_latest_preds(RAW_PREDS, time.time())
                            st.session_state['data'] = {'raw_fixtures':RAW_FIXTURES, 'squads':SQUADS, 'raw_preds':RAW_PREDS, 'latest_preds':LATEST_PREDS}
                            USER_PREDS = get_latest_user_preds(LATEST_PREDS, st.session_state['user_info']['localId'])

