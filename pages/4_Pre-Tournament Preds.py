import streamlit as st
import pandas as pd
import time
from utils.utils import *
from datetime import datetime
import pytz

@st.cache_data
def get_squads(foo=1):
    squads = read_squads()
    return squads

@st.cache_data
def get_pretournament_preds(foo=1):
    preds = read_all_pretournament()
    return preds

if 'user_info' not in st.session_state:
    st.write("### Log in on the **Hello** page")
else:

    SQUADS = get_squads()
    TEAMS = SQUADS['team.name'].sort_values(ascending=True).unique().tolist()
    PLAYERS = SQUADS.sort_values(by=['team.name', 'player.name'], ascending=[True, True])['player.name'].tolist()

    st.title('Pre-Tournament Guesses')
    st.write('''
    You have a chance to boost your tally by correctly answering the below seven questions.  
    Deadline for submitting answers is 2 hours before the kick-off of the opening game:  
    **14.06.2024 19:00 CEST**
            
    Use the form below to submit your answers. You can change your answers as many times as you wish before the deadline. After deadline your latest submission will be used.
    ''')

    _, _column, _ = st.columns([1,3,1])
    with _column:
        with st.form(key='pre-tournament-preds'):

            st.write('For the tournament podium questions, please select **three different** teams')

            first = st.selectbox(
                label='**Who will win the Euros?**',
                options=TEAMS
            )

            second = st.selectbox(
                label='**Who will finish second?**',
                options=TEAMS
            )

            # third = st.selectbox(
            #     label='**Who will get the third place?**',
            #     options=TEAMS
            # )

            # podium_check = len(set([first, second, third])) == 3
            podium_check = len(set([first, second])) == 2

            top_gs = st.selectbox(
                label='**Who will score the most goals?**',
                options=PLAYERS
            )

            mvp = st.selectbox(
                label='**Who will be the MVP of the torunament?**',
                options=PLAYERS
            )

            lewy_goals = st.number_input(
                label='**How many goals will Robert Lewandowski score?**',
                value=0, min_value=0, step=1
            )

            poland = st.selectbox(
                label='**How far will Poland advance?**',
                options=['Group Stage', 'Round of 16', 'Quarterfinals', 'Semifinals', 'Final']
            )

            send = st.form_submit_button("Submit")
            
            if send:
                if not podium_check:
                    st.error('Select two different teams you cheeky cunt')
                else:
                    cest = pytz.timezone('Europe/Warsaw')
                    if datetime.now(cest) > datetime(2024,6,14,19,0,0,tzinfo=cest):
                        st.error('Too late bro')
                    else:
                        row_to_insert = dict(
                            userId=st.session_state['user_info']['localId'],
                            first=first, second=second, #third=third,
                            top_gs=top_gs, mvp=mvp,
                            lewy_goals=lewy_goals, poland=poland,
                            timestamp=time.time()
                        )
                        send_to_bq('pretournament_preds', row_to_insert)

    if 'pre_tour_preds' not in st.session_state:
        _PRE_TOUR_PREDS = get_pretournament_preds()
        st.session_state['pre_tour_preds'] = _PRE_TOUR_PREDS
    else:
        _PRE_TOUR_PREDS = st.session_state['pre_tour_preds']

    st.write('---')
    st.write('If you cannot see Your Hero after choosing him, use the below refresh button')
    refresh = st.button(label='Refresh')
    st.write('---')

    st.write("### Your Pre-Tournament Preds")
    if refresh:
        _PRE_TOUR_PREDS = get_pretournament_preds(time.time())
        st.session_state['pre_tour_preds'] = _PRE_TOUR_PREDS
    if _PRE_TOUR_PREDS.loc[_PRE_TOUR_PREDS['userId']==st.session_state['user_info']['localId']].shape[0] < 1:
        st.write("You have not submitted Pre-Tournaments Preds yet")
    else:
        USER_PRE_TOUR_PREDS = _PRE_TOUR_PREDS.loc[_PRE_TOUR_PREDS['userId']==st.session_state['user_info']['localId']].sort_values('timestamp', ascending=False)
        USER_PRE_TOUR_PREDS = USER_PRE_TOUR_PREDS.iloc[0][1:-1].rename('Predictions')
        USER_PRE_TOUR_PREDS.index = [
            'Winner', 'Second Place', 
            'Top Scorer', 'MVP',
            "Lewandowski's goals",
            "How far will Poland advance?"
        ]
        st.dataframe(USER_PRE_TOUR_PREDS)
