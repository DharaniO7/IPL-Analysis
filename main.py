
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# LOAD DATASETS
# =========================

matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

# =========================
# DATA UNDERSTANDING
# =========================

print("MATCHES DATASET")
print(matches.head())

print("\nDELIVERIES DATASET")
print(deliveries.head())

# =========================
# DATA CLEANING
# =========================

# Drop useless column
matches.drop(columns=['umpire3'], inplace=True)

# Convert date column
matches['date'] = pd.to_datetime(matches['date'])

# Fill missing city values
matches['city'].fillna('Unknown', inplace=True)

# Fill missing umpire names
matches['umpire1'].fillna('Unknown', inplace=True)
matches['umpire2'].fillna('Unknown', inplace=True)

# Fix inconsistent team names
matches.replace(
    'Rising Pune Supergiants',
    'Rising Pune Supergiant',
    inplace=True
)

deliveries.replace(
    'Rising Pune Supergiants',
    'Rising Pune Supergiant',
    inplace=True
)

# =========================
# CHECK MISSING VALUES
# =========================

print("\nMissing Values in Matches")
print(matches.isnull().sum())

print("\nMissing Values in Deliveries")
print(deliveries.isnull().sum())

# =========================
# FIRST IPL ANALYSIS
# =========================

most_wins = matches['winner'].value_counts()

print("\nMost Successful IPL Teams")
print(most_wins.head(10))

# =========================
# VISUALIZATION
# =========================

plt.figure(figsize=(10,5))

sns.countplot(
    y='winner',
    data=matches,
    order=matches['winner'].value_counts().index
)

plt.title("Most Successful IPL Teams")
plt.xlabel("Number of Wins")
plt.ylabel("Teams")

plt.show()

toss_win_match_win = (matches['toss_winner'] == matches['winner']).mean() * 100

print(f"Toss winner also won the match: {toss_win_match_win:.2f}%")
labels = ['Won Match', 'Lost Match']

values = [
    (matches['toss_winner'] == matches['winner']).sum(),
    (matches['toss_winner'] != matches['winner']).sum()
]

plt.figure(figsize=(6,6))

plt.pie(
    values,
    labels=labels,
    autopct='%1.1f%%'
)

plt.title("Impact of Toss on Match Result")

plt.show()
merged_data = deliveries.merge(
    matches[['id', 'venue']],
    left_on='match_id',
    right_on='id'
)

print(merged_data.head())
venue_scores = merged_data.groupby('venue')['total_runs'].sum()

venue_scores = venue_scores.sort_values(ascending=False)

print(venue_scores.head(10))
plt.figure(figsize=(10,5))

sns.barplot(
    x=venue_scores.head(10).values,
    y=venue_scores.head(10).index
)

plt.title("Top 10 Highest Scoring IPL Venues")
plt.xlabel("Total Runs")
plt.ylabel("Venue")

plt.show()

top_batsmen = deliveries.groupby('batsman')['batsman_runs'].sum()

top_batsmen = top_batsmen.sort_values(ascending=False)

print(top_batsmen.head(10))
plt.figure(figsize=(10,5))

sns.barplot(
    x=top_batsmen.head(10).values,
    y=top_batsmen.head(10).index
)

plt.title("Top 10 IPL Run Scorers")
plt.xlabel("Runs")
plt.ylabel("Batsmen")

plt.tight_layout()
plt.show()

runs = deliveries.groupby('batsman')['batsman_runs'].sum()
balls = deliveries.groupby('batsman')['ball'].count()
strike_rate_df = pd.DataFrame({
    'Runs': runs,
    'Balls': balls
})
strike_rate_df['Strike Rate'] = (
    strike_rate_df['Runs'] / strike_rate_df['Balls']
) * 100
strike_rate_df = strike_rate_df[
    strike_rate_df['Runs'] > 2000
]
strike_rate_df = strike_rate_df.sort_values(
    by='Strike Rate',
    ascending=False
)

print(strike_rate_df.head(10))
plt.figure(figsize=(10,5))

sns.barplot(
    x=strike_rate_df.head(10)['Strike Rate'],
    y=strike_rate_df.head(10).index
)

plt.title("Best IPL Strike Rates")
plt.xlabel("Strike Rate")
plt.ylabel("Batsmen")

plt.tight_layout()
plt.show()

wickets_data = deliveries[
    deliveries['dismissal_kind'] != 'run out'
]
top_bowlers = wickets_data.groupby('bowler')[
    'player_dismissed'
].count()
top_bowlers = top_bowlers.sort_values(
    ascending=False
)

print(top_bowlers.head(10))
plt.figure(figsize=(10,5))

sns.barplot(
    x=top_bowlers.head(10).values,
    y=top_bowlers.head(10).index
)

plt.title("Top IPL Wicket Takers")
plt.xlabel("Wickets")
plt.ylabel("Bowlers")

plt.tight_layout()
plt.show()