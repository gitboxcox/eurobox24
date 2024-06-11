import streamlit as st

st.set_page_config(layout="wide")

st.write('''
# EuroBox24 Rules
---
The sign-up fee is 20 PLN
Price split:  
- 1st place: 50%
- 2nd place: 30%
- 3rd place: 20%
         
You can score points in 3 different ways:
1. Pre-tournament predictions about (each worth 10 points) -> Submit by **14/06/2024 19:00 CEST**
    - Winner & Runner-up
    - Top goal scorer
    - Player of the torunament
    - Phase of the tournament at which Poland will exit
    - How many goals will Robert Lewandowski score
2. Your Hero -> Submit by **14/06/2024 19:00 CEST**
    - You will select one player for which you will score points like in the [Fantasy Premier League](https://www.premierleague.com/news/2174909) (**no bonus points**)
    - Events are collected using [API-Football](https://www.api-football.com), so blame them if you're unsatisfied :grinning:
3. Game predictions -> Submit by **2 hours before first game of each Gameday**
    - 1 point for correctly indicating Home Team score
    - 1 point for correctly indicating Away Team score
    - 1 point for correctly predicting outcome of the game (Home Team win, Away Team win, draw)
    - 1 bonus point if you get the get the exact score
    - 1 point for correctly indicating first team to score
    - 1 point for correctly indicating player that will score the first goal of the game (own goal = 2 points)
    - If you manage to get everything right, you'll get double points
''')