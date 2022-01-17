import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Fantasy Basketball Dashboard')
st.markdown('''
Monitor Fantasy Basketball PLayers
Built using base64, pandas, streamlit \n
Data collected from [Basketballreference.com](https://www.basketball-reference.com/)
''')

st.sidebar.header('User Options')
selected_year = st.sidebar.selectbox('Year Selected', list(reversed(range(2016, 2023))))

#webscraping stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team Selected', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
df_selected_team = df_selected_team.drop(columns=['FG%', '3P%', '2P%', 'FT%', 'eFG%'])
dataFrame_selTeam = pd.DataFrame(df_selected_team)
new_df = pd.DataFrame()

fantasy_players = ['James Harden', 'LaMelo Ball']

playernames = dataFrame_selTeam['Player']

for i in fantasy_players:
    index_num = list(playernames).index('James Harden')
    new_df.append(dataFrame_selTeam.loc[[index_num]])

st.dataframe(new_df)

