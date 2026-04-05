"""
Fetch trending stories from HackerNews and group them into categories based on keywords, 
then save the result as a JSON file
"""

import requests
import time
import json
import datetime as dt
import os

top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"
headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    
    "worldnews": [
        "war", "government", "country", "president", "election", "climate",
        "attack", "global", "policy", "law", "minister", "news",
        "china", "india", "russia", "uk", "us", "eu",
        "regulation", "sanction", "court", "bill", "vote"
    ],
    
    "sports": [
        "nfl", "nba", "fifa", "sport", "game", "team", "player",
        "league", "championship", "match", "tournament", "score",
        "goal", "win", "final", "coach", "season",
        "cricket", "football", "soccer", "tennis"
    ],

    "science": [
        "research", "study", "space", "physics", "biology", "discovery",
        "nasa", "genome", "scientist", "experiment", "lab",
        "quantum", "astronomy", "neuroscience", "medicine",
        "drug", "health", "disease", "cell", "energy"
    ],
    
    "entertainment": [
        "movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming", 
        "tv", "series", "video"
    ]
}

# Decide category by checking keywords in the title
def assign_category(title):
    title = title.lower()
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title:
                return category
            
    return None

# Get top story IDs (limiting to 500 to keep things manageable)
try:
    response = requests.get(top_stories_url, headers=headers)
    response.raise_for_status()
    
    story_ids = response.json()
    story_ids = story_ids[:500]
    
    print("Fetched Top Story IDs")
    
except Exception as e:
    print(f"Error Fetching Top Stories : {e}")
    story_ids = []
    
collected_stories = []

category_count = {
    "technology" : 0,
    "worldnews" : 0,
    "sports" : 0,
    "science" : 0,
    "entertainment" : 0
}

# Go through each category and collect up to 25 matching stories
for category in categories:
    print(f"\nCollecting Stories For : {category}")
    for story_id in story_ids:
        if category_count[category] >= 25:
            break
        
        # Fetch story details
        try:
            response = requests.get(item_url.format(story_id), headers=headers)
            response.raise_for_status()
            
            story = response.json()
            
        
        except Exception as e:
            print(f"Error Fetching Story {story_id} : {e}")
            continue

        title = story.get("title")
        
        # Skip if no title or doesn't match this category
        if not title:
            continue
        
        assigned_category = assign_category(title)
        
        if assigned_category != category:
            continue
        
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        collected_stories.append(story_data)
        category_count[category] += 1
        
    time.sleep(2)
    
if not os.path.exists("data"):
    os.makedirs("data")

date_str = dt.datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{date_str}.json"

# Save results to JSON file inside data folder
with open(filename, "w") as f:
    json.dump(collected_stories, f, indent=4)
    
print(f"\nCollected {len(collected_stories)} Stories. Saved To {filename}")