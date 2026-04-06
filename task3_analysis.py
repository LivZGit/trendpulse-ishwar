import pandas as pd
import numpy as np

# Path of The cleaned CSV file
cleanedCsvPath = f"data/trends_clean.csv"

"""Task 1"""
# Loading cleaned CSV into Pandas DataFrame
df = pd.read_csv(cleanedCsvPath)

print(f"\nLoaded data: {df.shape}")

# Printing first 5 rows of the DataFrame
print(f"\nFirst 5 rows: \n{df.head(5)}")

# Average of score
avg_score = np.mean(df["score"])
print(f"\nAverage score   : {avg_score:.2f}")

# Average of comments
avg_num_comments = np.mean(df["num_comments"])
print(f"\nAverage comments: {avg_num_comments:.2f}")

"""Task 2"""
print("\n--- NumPy Stats ---")

scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

# Average score
print(f"Mean score   : {np.mean(scores):.2f}")

# Median score
print(f"Median score : {np.median(scores):.2f}")

# Standard deviation of score
print(f"Std deviation: {np.std(scores):.2f}")

# Maximum score
print(f"Max score    : {np.max(scores)}")

# Minimum score
print(f"Min score    : {np.min(scores)}")

# Categories with the most stories
category_counts = df["category"].value_counts()

top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with most comments
most_commented = df.loc[df["num_comments"].idxmax()]

print(f"\nMost commented story: \"{most_commented['title']}\" — {most_commented['num_comments']} comments")

"""Task 3"""
# New Columns

# engagement column
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular column
df["is_popular"] = df["score"] > avg_score

"""Task 4"""
# Saving the result
output_path = f"data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")