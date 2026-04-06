import pandas as pd
import matplotlib.pyplot as plt
import os

"""Task 1"""
# Task 3 Result CSV File
trends_analysed_csv = f"data/trends_analysed.csv"
df = pd.read_csv(trends_analysed_csv)

os.makedirs("outputs", exist_ok=True)

"""Task 2 — Chart 1: Top 10 Stories by Score"""
top10_stories = df.sort_values(by="score", ascending=False).head(10)

# Shortening title if length is more than 50
short_titles = []

for title in top10_stories["title"]:
    if len(title) > 50:
        short_titles.append(title[:50] + "...")
    else:
        short_titles.append(title)

top10_stories["short_title"] = short_titles

plt.figure(figsize=(8,6))
# Horizontal Bar Graph
plt.barh(top10_stories["short_title"], top10_stories["score"])

# Labels
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Title")

# Sorting in Descending order
plt.gca().invert_yaxis()

# Saving chart
plt.savefig("outputs/chart1_top_stories.png")
plt.close()


"""Task 3 — Chart 2: Stories per Category"""
category_counts = df["category"].value_counts()

plt.figure(figsize=(8,6))
# Bar chart
plt.bar(category_counts.index, category_counts.values, color=["blue", "red", "green", "purple", "orange"])

# Labels
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.savefig("outputs/chart2_categories.png")
plt.close()

"""Taks 4 — Chart 3: Score vs Comments"""
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(8,6))

# Scatter Plot 1
plt.scatter(popular["score"], popular["num_comments"], label="Popular")

# Scatter Plot 2
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

# Labels
plt.title("Score Vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.close()

"""BONUS - Dashboard"""
fig, axes = plt.subplots(1, 3, figsize=(18,5))

# Chart 1 - Horizontal Bar Graph
axes[0].barh(top10_stories["short_title"], top10_stories["score"])
axes[0].set_title("Top Stories")
axes[0].invert_yaxis()

# Chart 2 - Bar Graph
axes[1].bar(category_counts.index, category_counts.values, color=["blue", "red", "green", "purple", "orange"])
axes[1].set_title("Stories per Category")

# Chart 3 - Scatter Plot
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score Vs Comments")

# Main Title
fig.suptitle("TrendPulse Dashboard")

# Saving The Graphs
plt.savefig("outputs/dashboard.png")    
plt.close()