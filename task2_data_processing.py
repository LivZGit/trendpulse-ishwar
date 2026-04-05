import pandas as pd
import os

# Load JSON data into a DataFrame
filePath = "data/trends_20260405.json"
df = pd.read_json(filePath)

print(f"\nLoaded {len(df)} stories from {filePath}")

# Remove duplicate stories using post_id
df = df.drop_duplicates(subset="post_id")
print(f"\nAfter removing duplicates: {len(df)}")

# Remove rows where "post_id", "title", "score" are missing
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Converting "score", "num_comments" to integer data type
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Filtering low-qualtiy strories
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Removing extra white-space from "title"
df["title"] = df["title"].str.strip()

output_path = "data/trends_clean.csv"

# Save cleaned data to CSV
df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")

print(f"\nStories per category:")
print(df["category"].value_counts())