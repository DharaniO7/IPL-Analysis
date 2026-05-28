
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================

matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

# =========================
# TITLE
# =========================

st.title("🏏 IPL Data Analysis Dashboard")

st.write(
    "This dashboard analyzes IPL data using Python, Pandas, Seaborn, and Streamlit."
)
# =========================
# KPI CARDS
# =========================

total_matches = matches.shape[0]
total_seasons = matches['season'].nunique()
total_teams = pd.concat([
    matches['team1'],
    matches['team2']
]).nunique()

highest_win_margin = matches['win_by_runs'].max()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Matches", total_matches)
col2.metric("Total Seasons", total_seasons)
col3.metric("Total Teams", total_teams)
col4.metric("Highest Win Margin", highest_win_margin)
# =========================
# SIDEBAR
# =========================

st.sidebar.title("Filter")

selected_season = st.sidebar.selectbox(
    "Select Season",
    sorted(matches['season'].unique())
)

filtered_matches = matches[
    matches['season'] == selected_season
]

st.write(f"Showing data for IPL Season {selected_season}")

st.dataframe(filtered_matches.head())
teams = sorted(pd.concat([
    matches['team1'],
    matches['team2']
]).unique())

selected_team = st.sidebar.selectbox(
    "Select Team",
    teams
)
team_matches = matches[
    (matches['team1'] == selected_team) |
    (matches['team2'] == selected_team)
]

team_wins = team_matches[
    team_matches['winner'] == selected_team
].shape[0]

st.subheader(f"📊 {selected_team} Analysis")

st.metric("Matches Played", team_matches.shape[0])

st.metric("Matches Won", team_wins)
# =========================
# INTERACTIVE TEAM WINS CHART
# =========================

team_wins = matches['winner'].value_counts()

fig = px.bar(
    x=team_wins.values,
    y=team_wins.index,
    orientation='h',
    labels={'x': 'Wins', 'y': 'Teams'},
    title='Most Successful IPL Teams'
)
# =========================
# TOSS IMPACT
# =========================

labels = ['Won Match', 'Lost Match']

values = [
    (matches['toss_winner'] == matches['winner']).sum(),
    (matches['toss_winner'] != matches['winner']).sum()
]

fig2 = px.pie(
    names=labels,
    values=values,
    title='Impact of Toss on Match Result'
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# TOP RUN SCORERS
# =========================
top_batsmen = deliveries.groupby(
    'batsman'
)['batsman_runs'].sum()

top_batsmen = top_batsmen.sort_values(
    ascending=False
).head(10)

fig2 = px.bar(
    x=top_batsmen.values,
    y=top_batsmen.index,
    orientation='h',
    labels={'x': 'Runs', 'y': 'Batsman'},
    title='Top 10 IPL Run Scorers'
)

# =========================
# TOP WICKET TAKERS
# =========================

wickets_data = deliveries[
    deliveries['dismissal_kind'] != 'run out'
]

top_bowlers = wickets_data.groupby(
    'bowler'
)['player_dismissed'].count()

top_bowlers = top_bowlers.sort_values(
    ascending=False
).head(10)

fig3 = px.bar(
    x=top_bowlers.values,
    y=top_bowlers.index,
    orientation='h',
    labels={'x': 'Wickets', 'y': 'Bowler'},
    title='Top IPL Wicket Takers'
)

# =========================
# HIGHEST SCORING VENUES
# =========================

merged_data = deliveries.merge(
    matches[['id', 'venue']],
    left_on='match_id',
    right_on='id'
)

venue_scores = merged_data.groupby(
    'venue'
)['total_runs'].sum()

venue_scores = venue_scores.sort_values(
    ascending=False
).head(10)

fig4 = px.bar(
    x=venue_scores.values,
    y=venue_scores.index,
    orientation='h',
    labels={'x': 'Runs', 'y': 'Venue'},
    title='Highest Scoring IPL Venues'
)
# =========================
# DASHBOARD LAYOUT
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Most Successful Teams")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏏 Top IPL Run Scorers")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("🎯 Top IPL Wicket Takers")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🎉High scoring IPL venues")
    st.plotly_chart(fig4, use_container_width=True)
st.markdown("---")
st.write("Created by Dharani using Python, Pandas, Plotly & Streamlit 🚀")
