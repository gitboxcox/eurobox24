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
def get_heroes(foo=1):
    heroes = read_all_heroes()
    return heroes

@st.cache_data
def get_fixtures(foo=1):
    fixtures = read_fixtures()
    return fixtures

st.title('Your Hero')
st.write('''
You can additionally score points with Your Hero.  
Points are calculated based on Regular + potential Extra Time.  
Select one player for the whole torunament.  
Deadline for choosing Your Hero is 2 hours before the kick-off of the opening game:  
**14.06.2024 19:00 CEST**  
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
    | For each assist for a goal*                               | 3      |
    | For a clean sheet by a a goalkeeper or defender           | 4      |        
    | For a clean sheet by a midfielder                         | 1      |
    | For every 3 shots saved by a goalkeeper                   | 1      |
    | For each penalty save                                     | 5      |
    | For each penalty miss                                     | -2     |
    | For every 2 goals conceded by a goalkeeper or defender    | -1     |
    | For each yellow card                                      | -1     |
    | For each red card                                         | -3     |
    | For each own goal                                         | -2     |
    ''')
    st.caption('''
    * Won penalties may not be counted as assists.  
    The app rely on how API-Football defines an assist in their data :grinning:
    ''')

if 'user_info' not in st.session_state:
    st.write("### Log in on the **Hello** page")
else:

    if 'squads' not in st.session_state:
        SQUADS = get_squads()
        st.session_state['squads'] = SQUADS
    else:
        SQUADS = st.session_state['squads']

    if 'heroes' not in st.session_state:
        HEROES = get_heroes(time.time())
        st.session_state['heroes'] = HEROES
    else:
        HEROES = st.session_state['heroes']

    if 'fixtures' not in st.session_state:
        FIXTURES = get_fixtures()
        st.session_state['fixtures'] = FIXTURES
    else:
        FIXTURES = st.session_state['fixtures']

    if datetime.now(pytz.timezone("Europe/Warsaw")) > datetime(2024,6,14,19,0,tzinfo=pytz.timezone("Europe/Warsaw")):
        st.info(
            '''Ups... It's past the deadline. Unfortunately, you cannot select Your Hero now''',
            icon='🕐'
        )
    else:

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
            cest = pytz.timezone('Europe/Warsaw')
            if datetime.now(cest) > datetime(2024,6,14,19,0,0,tzinfo=cest):
                st.error('Too late bro')
            else:
                row_to_insert = dict(
                    userId=st.session_state['user_info']['localId'],
                    heroName=player, heroId=int(playerId),
                    timestamp=time.time()
                )
                send_to_bq('heroes', row_to_insert)
                HEROES = get_heroes(time.time())
                st.session_state['heroes'] = HEROES

    st.write('---')
    st.write('If you cannot see Your Hero after choosing him, use the below refresh button')
    refresh = st.button(label='Refresh')
    st.write('---')
    
    st.write('### Your Hero is:')
    if refresh:
        SQUADS = get_squads(time.time())
        st.session_state['squads'] = SQUADS
        HEROES = get_heroes(time.time())
        st.session_state['heroes'] = HEROES
    if HEROES.loc[HEROES['userId'] == st.session_state['user_info']['localId']].shape[0] < 1:
        st.write("You have not selected Your Hero yet")
    else:
        _HERO = HEROES.loc[HEROES['userId'] == st.session_state['user_info']['localId']].sort_values('timestamp', ascending=False)['heroName'].iloc[0]
        HERO = SQUADS.loc[SQUADS['player.name']==_HERO]
        st.write(f'''
        #### {HERO['player.name'].iloc[0]} 
        ##### _{HERO['team.name'].iloc[0]}_  
        ##### _{HERO['player.position'].iloc[0]}_
        ---
        ''')
        st.write('''### Your Hero's games''')
        for idx, fixture in FIXTURES[(FIXTURES['teams.home.name']==HERO['team.name'].iloc[0]) | (FIXTURES['teams.away.name']==HERO['team.name'].iloc[0])].iterrows():
            st.write(
                f"{fixture['fixture.date_nice']} - {fixture['teams.home.name']} vs {fixture['teams.away.name']}"
            )
    

    
