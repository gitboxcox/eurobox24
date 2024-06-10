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
def get_heroes(foo=1):
    heroes = read_all_heroes()
    return heroes

st.title('Your Hero')
st.write('''
You can additionally score points with Your Hero.  
Select one player for the whole torunament.  
Deadline for choosing Your Hero is 2 hours before the kick-off of the opening game:  
**14.07.2024 19:00 CEST**  
''')

with st.expander('How to score points?'):
    st.write('''
    | Action                                                    | Points |
    |-----------------------------------------------------------|--------|
    | For playing up to 60 minutes                              | 1      |
    | For playing 60 minutes or more (excluding stoppage time)  | 2      |
    | For each goal scored by a goalkeeper or defender          | 6      |
    | For each goal scored by a midfielder                      | 5      |
    | For each goal scored by an attacker                       | 4      |
    | For each assist for a goal                                | 3      |
    | For a clean sheet by a midfielder                         | 1      |
    | For every 3 shots saved by a goalkeeper                   | 1      |
    | For each penalty save                                     | 5      |
    | For each penalty miss                                     | -2     |
    | For every 2 goals conceded by a goalkeeper or defender    | -1     |
    | For each yellow card                                      | -1     |
    | For each red card                                         | -3     |
    | For each own goal                                         | -2     |
    ''')

if 'user_info' not in st.session_state:
    st.write("### Log in on the **Hello** page")
else:

    SQUADS = get_squads()
    HEROES = get_heroes()

    st.write(
    '''
    Use form below to choose Your Hero. You can change your mind as many times as you wish before the deadline.
    Use filters below to narrow your search or simply start typing in the surname.
    ''')


    # country filter
    country = st.selectbox(
        label='Filter by Country',
        options=SQUADS['team.name'].sort_values(ascending=True).unique().tolist(),
        # index=None
    )

    # position filter
    position = st.selectbox(
        label='Filter by Position',
        options=SQUADS['player.position'].sort_values(ascending=True).unique().tolist(),
        # index=None
    )

    country_filter = SQUADS['team.name'] == country if country!='' else pd.Series([True]*SQUADS.shape[0])
    position_filter = SQUADS['player.position'] == position if position!='' else pd.Series([True]*SQUADS.shape[0])
    filter = (country_filter) & (position_filter)

    player = st.selectbox(
        label='Choose Player',
        options=SQUADS.sort_values(['team.name', 'player.name']).loc[filter, 'player.name'].tolist()
    )
    playerId = SQUADS.loc[SQUADS['player.name']==player, 'player.id'].iloc[0]
    
    st.caption('Use button below to submit')
    submit = st.button(
        label=f"I'm choosing :star: **{player}** :star:"
    )
    if submit and player:
        if datetime.datetime.now() > datetime.datetime(2024,6,14,19,0,0):
            st.error('Too late bro')
        else:
            row_to_insert = dict(
                userId=st.session_state['user_info']['localId'],
                heroName=player, heroId=int(playerId),
                timestamp=time.time()
            )
            send_to_bq('heroes', row_to_insert)

    st.write('---')
    st.write('If you cannot see Your Hero after choosing him, use the below refresh button')
    refresh = st.button(label='Refresh')
    st.write('---')
    
    st.write('## Your Hero is:')
    if refresh:
        SQUADS = get_squads(time.time())
        HEROES = get_heroes(time.time())
    if HEROES.loc[HEROES['userId'] == st.session_state['user_info']['localId']].shape[0] < 1:
        st.write("You have not selected Your Hero yet")
    else:
        _HERO = HEROES.loc[HEROES['userId'] == st.session_state['user_info']['localId']].sort_values('timestamp', ascending=False)['heroName'].iloc[0]
        HERO = SQUADS.loc[SQUADS['player.name']==_HERO]
        st.write(f'''
        ---
        ### {HERO['player.name'].iloc[0]} 
        #### _{HERO['team.name'].iloc[0]}_  
        #### _{HERO['player.position'].iloc[0]}_
        ---
        ''')