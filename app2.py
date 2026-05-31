import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# Load Data
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

merged = deliveries.merge(
    matches,
    left_on="match_id",
    right_on="id"
)

# Title
st.title("🏏 IPL Analytics Dashboard")

st.markdown("Interactive IPL Analysis Dashboard")
total_matches = matches.shape[0]
total_seasons = matches["season"].nunique()
total_teams = len(pd.unique(matches[["team1","team2"]].values.ravel()))
highest_win_margin = matches["win_by_runs"].max()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Matches", total_matches)
col2.metric("Total Seasons", total_seasons)
col3.metric("Total Teams", total_teams)
col4.metric("Highest Win Margin", highest_win_margin)
st.sidebar.header("Filters")

season = st.sidebar.selectbox(
    "Select Season",
    ["All"] + sorted(matches["season"].unique().tolist())
)

team = st.sidebar.selectbox(
    "Select Team",
    ["All"] + sorted(pd.unique(matches[["team1","team2"]].values.ravel()).tolist())
)


wins = matches["winner"].value_counts().head(10)

fig1 = px.bar(
    wins,
    orientation="h"
)

toss_win_match_win = matches[matches["toss_winner"] == matches["winner"]].shape[0]
toss_win_match_lose = matches.shape[0] - toss_win_match_win

fig2 = px.pie(
    values=[toss_win_match_win, toss_win_match_lose],
    names=["Won Match","Lost Match"],
    title="Impact of Toss on Match Result"
)

top_runs = (
    deliveries.groupby("batsman")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig3 = px.bar(
    x=top_runs.values,
    y=top_runs.index,
    orientation="h"
)


wickets = deliveries[deliveries["player_dismissed"].notna()]

top_wickets = (
    wickets["bowler"]
    .value_counts()
    .head(10)
)

fig4 = px.bar(
    x=top_wickets.values,
    y=top_wickets.index,
    orientation="h",
    labels={"x": "Wickets", "y": "Bowler"}
)
venue_runs = merged.groupby("venue")["total_runs"].sum()

venue_runs = venue_runs.sort_values(
    ascending=False
).head(10)

fig5 = px.bar(
    x=venue_runs.values,
    y=venue_runs.index,
    orientation="h",
    labels={"x": "Runs", "y": "Venue"}
)

total_matches_team = pd.concat([
    matches["team1"],
    matches["team2"]
]).value_counts()

total_wins = matches["winner"].value_counts()

win_percentage = (
    (total_wins / total_matches_team) * 100
).dropna()

win_percentage = win_percentage.sort_values(
    ascending=False
).head(10)

fig6 = px.bar(
    x=win_percentage.index,
    y=win_percentage.values,
    title="Top Teams by Win Percentage"
)

fig6.update_layout(
    xaxis_title="Team",
    yaxis_title="Win Percentage (%)",
    height=400
)

season_runs = merged.groupby("season")["total_runs"].sum().reset_index()

fig7 = px.line(
    season_runs,
    x="season",
    y="total_runs",
    markers=True,
    title="Total Runs Scored per Season"
)

# Total runs scored in each match
match_scores = (
    merged.groupby(["season", "match_id"])["total_runs"]
    .sum()
    .reset_index()
)

# Average match score for each season
avg_match_score = (
    match_scores.groupby("season")["total_runs"]
    .mean()
    .reset_index()
)

fig8 = px.line(
    avg_match_score,
    x="season",
    y="total_runs",
    markers=True,
    title="Average Runs per Match by Season"
)

fig8.update_layout(
    xaxis_title="Season",
    yaxis_title="Average Match Score",
    height=400
)

season_runs = merged.groupby(
    ["season", "batsman"]
)["batsman_runs"].sum().reset_index()

orange_winners = season_runs.loc[
    season_runs.groupby("season")["batsman_runs"].idxmax()
]

fig9 = px.bar(
    orange_winners,
    x="season",
    y="batsman_runs",
    color="batsman",
    title="Orange Cap Winners by Season"
)

season_wickets = (
    merged[merged["player_dismissed"].notna()]
    .groupby(["season", "bowler"])
    .size()
    .reset_index(name="wickets")
)

purple_winners = season_wickets.loc[
    season_wickets.groupby("season")["wickets"].idxmax()
]

fig10 = px.bar(
    purple_winners,
    x="season",
    y="wickets",
    color="bowler",
    title="Purple Cap Winners by Season"
)

fig1.update_layout(height=380)
fig2.update_layout(height=380)
fig3.update_layout(height=380)
fig4.update_layout(height=380)
fig5.update_layout(height=380)
fig6.update_layout(height=380)
fig7.update_layout(height=400)
fig8.update_layout(height=400)
fig9.update_layout(height=380)
fig10.update_layout(height=380)

# =========================
# ROW 2
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Most Successful Teams")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🎯 Toss Impact")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# =========================
# ROW 3
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏏 Top Run Scorers")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🎯 Top Wicket Takers")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# =========================
# ROW 4
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏟️ Highest Scoring IPL Venues")
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader("🏆 Team Win Percentage")
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# =========================
# ROW 5
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Season-wise Total Runs")
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    st.subheader("🏏 Average Runs per Match")
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

# =========================
# ROW 6
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🟠 Orange Cap Winners")
    st.plotly_chart(fig9, use_container_width=True)

with col2:
    st.subheader("🟣 Purple Cap Winners")
    st.plotly_chart(fig10, use_container_width=True)
