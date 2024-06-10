import streamlit as st
import pandas as pd
import time
from utils.utils import *
import datetime

st.set_page_config(layout="wide")

@st.cache_data
def get_squads(foo=1):
    squads = pd.read_csv('/Users/jakubpaczusko/Desktop/gcp/eurobox24/data/squads.csv')
    return squads

@st.cache_data
def get_squads(foo=1):
    squads = pd.read_csv('/Users/jakubpaczusko/Desktop/gcp/eurobox24/data/squads.csv')
    return squads


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
    **14.07.2024 19:00 CEST**
            
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

            third = st.selectbox(
                label='**Who will get the third place?**',
                options=TEAMS
            )

            podium_check = len(set([first, second, third])) == 3

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
                    st.error('Select three different teams you cheeky cunt')
                else:
                    if datetime.datetime.now() > datetime.datetime(2024,6,14,19,0,0):
                        st.error('Too late bro')
                    else:
                        row_to_insert = dict(
                            userId=st.session_state['user_info']['localId'],
                            first=first, second=second, third=third,
                            top_gs=top_gs, mvp=mvp,
                            lewy_goals=lewy_goals, poland=poland,
                            timestamp=time.time()
                        )
                        send_to_bq('pretournament_preds', row_to_insert)