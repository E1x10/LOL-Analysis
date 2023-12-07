#data sorting
import numpy as np
import pandas as pd
#visualization
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns
import plotly as py
import plotly.graph_objs as go

#read data
df = pd.read_csv(r'C:\CSC21700\LOL\games.csv')
df.head()
df.shape
champs = pd.read_csv(r'C:\CSC21700\LOL\champs.csv')

# Calculate win rate
win_rate_counts = df['winner'].value_counts()
labels = win_rate_counts.index
values = win_rate_counts.values

# Identifying columns that contain champion IDs
champion_columns = [col for col in df.columns if 'champ' in col and 'id' in col]

# Counting the occurrences of each champion ID in these columns
champion_counts = df[champion_columns].apply(pd.Series.value_counts).sum(axis=1).sort_values(ascending=False)

# Plot Pie Chart
labels = ['Team 1' if label == 1 else 'Team 2' for label in labels]
plt.figure(figsize=(8, 8))

# Use seaborn to create the pie chart
sns.set_palette(['#3498db', '#e74c3c'])
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)

plt.title('Winrate of Matches')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()


#First Blood Winrate
# Calculate First Blood Winrate
first_blood_counts = df.groupby('firstBlood')['winner'].value_counts(normalize=True).unstack().fillna(0)
first_blood_winrate = first_blood_counts[1] * 100  # Convert to percentage

# Plot Horizontal Bar Graph
plt.figure(figsize=(10, 6))
first_blood_winrate.plot(kind='barh', color=['blue', 'red'], alpha=0.7)

plt.title('First Blood Winrate')
plt.xlabel('Winrate (%)')
plt.ylabel('First Blood and Win (Team)')
plt.xlim(0, 100)  # Set x-axis limit to represent percentages

# Display winrate values on the bars
for index, value in enumerate(first_blood_winrate):
    plt.text(value, index, f'{value:.1f}%', va='center')

plt.show()

#Bar graph
def plot_bar_horizontal(input_col, target_col, title_name):
    # Calculate winrate based on the specified input column
    winrate_counts = df.groupby(input_col)[target_col].value_counts(normalize=True).unstack().fillna(0)
    
    # If 0 is present in the index, it means no team got the specified objective
    if 0 in winrate_counts.index:
        winrate_counts = winrate_counts.drop(0)

    winrate = winrate_counts[1] * 100  # Assuming 1 represents the winning team

    # Plot Horizontal Bar Graph
    plt.figure(figsize=(10, 6))
    winrate.plot(kind='barh', color=['blue', 'red'], alpha=0.7)

    plt.title(title_name)
    plt.xlabel('Winrate (%)')
    plt.ylabel(title_name)  # Use title_name for both title and ylabel
    plt.xlim(0, 100)  # Set x-axis limit to represent percentages

    # Display winrate values on the bars
    for index, value in enumerate(winrate):
        plt.text(value, index, f'{value:.1f}%', va='center')

    plt.show()
# Usage
# First Tower    
plot_bar_horizontal(input_col='firstTower', target_col='winner', title_name='First Tower on Winning')
# First Inhibitor
plot_bar_horizontal(input_col='firstInhibitor', target_col='winner', title_name='Destroying First Inhibitor on Winning')
# First Baron
plot_bar_horizontal(input_col='firstBaron', target_col='winner', title_name='Killing First Baron on Winning')
# First Dragon
plot_bar_horizontal(input_col='firstDragon', target_col='winner', title_name='Killing First Dragon on Winning')
# First Herald
plot_bar_horizontal(input_col='firstRiftHerald', target_col='winner', title_name='Impact of Killing First Herald on Winning')


# initialize winning list
t1_win_rates = []
t2_win_rates = []

# Calculate win rate of every team in different numbers of drags
for dragons in range(7):  # from 0 to 6 drag
    # win rate for first team
    t1_games_with_dragons = df[(df['t1_dragonKills'] == dragons)]
    t1_wins_with_dragons = t1_games_with_dragons[t1_games_with_dragons['winner'] == 1]
    t1_win_rate = len(t1_wins_with_dragons) / len(t1_games_with_dragons) if len(t1_games_with_dragons) > 0 else 0
    t1_win_rates.append(t1_win_rate)
    
    # win rate for second team
    t2_games_with_dragons = df[(df['t2_dragonKills'] == dragons)]
    t2_wins_with_dragons = t2_games_with_dragons[t2_games_with_dragons['winner'] == 2]
    t2_win_rate = len(t2_wins_with_dragons) / len(t2_games_with_dragons) if len(t2_games_with_dragons) > 0 else 0
    t2_win_rates.append(t2_win_rate)

# setting up the bar graph
index = np.arange(7)
bar_width = 0.35
offset = bar_width / 2  # to not have overlap

fig, ax = plt.subplots()

# set up bar graph distinguished by team
bar1 = ax.bar(index - offset, t1_win_rates, bar_width, label='Team 1', color='b')
bar2 = ax.bar(index + offset, t2_win_rates, bar_width, label='Team 2', color='r')

# add chart column
ax.legend()

# label x and y
ax.set_xlabel('Number of Dragons')
ax.set_ylabel('Win Rate (%)')
ax.set_title('Win Rate by Number of Dragons')
ax.set_xticks(index)
ax.set_xticklabels(range(7))
ax.set_yticks([i/10 for i in range(11)])  # set y from 0%-100%
ax.set_yticklabels([f'{i*10}%' for i in range(11)])

# show
plt.show()