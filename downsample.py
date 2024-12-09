import pandas as pd
from tqdm import tqdm
import json
import os

# List of JSON files
json_files = ["review_split_0.json", "review_split_1.json", "review_split_2.json"]

# Initialize lists to hold data
user_ids, business_ids, stars, dates, texts = [], [], [], [], []

# Process each JSON file
for json_file in json_files:
    print(f"Processing {json_file}...")
    # Count the number of lines in the current file
    with open(json_file, "r") as file:
        line_count = sum(1 for _ in file)
    
    # Read the JSON file line by line
    with open(json_file, "r") as file:
        for line in tqdm(file, total=line_count, desc=f"Reading {json_file}"):
            blob = json.loads(line)
            user_ids.append(blob["user_id"])
            business_ids.append(blob["business_id"])
            stars.append(blob["stars"])
            dates.append(blob["date"])
            texts.append(blob["text"])

# Create a DataFrame
ratings_ = pd.DataFrame(
    {
        "user_id": user_ids,
        "business_id": business_ids,
        "rating": stars,
        "date": dates,
        "text": texts,
    }
)

# Count the number of reviews per user
user_counts = ratings_["user_id"].value_counts()

# Get users with 5 or more reviews
active_users = user_counts.loc[user_counts >= 5].index.tolist()

# Filter ratings to include only active users
ratings_ = ratings_.loc[ratings_.user_id.isin(active_users)]

# Optional: print the first few rows to verify
print(ratings_.head())

active_users = user_counts.loc[user_counts >= 5].index.tolist()
ratings_ = ratings_.loc[ratings_.user_id.isin(active_users)]

SAMPLING_RATE = 1/5
user_id_unique = ratings_.user_id.unique()
user_id_sample = pd.DataFrame(user_id_unique, columns=['unique_user_id']) \
                    .sample(frac= SAMPLING_RATE, replace=False, random_state=1)
ratings_sample = ratings_.merge(user_id_sample, left_on='user_id', right_on='unique_user_id') \
                    .drop(['unique_user_id'], axis=1)

# Step 1: Load the user dataset (yelp_academic_dataset_user.json)
user_data = []
with open('yelp_academic_dataset_user.json', 'r') as f:
    for line in f:
        user_data.append(json.loads(line))

# Step 2: Convert the user data into a DataFrame and keep only the relevant columns
user_df = pd.DataFrame(user_data)
user_df = user_df[['user_id', 'review_count', 'yelping_since', 'fans', 'average_stars']]

# Step 3: Filter ratings_sample to keep only users with a matching user_id from user_df
ratings_sample = ratings_sample[ratings_sample['user_id'].isin(user_df['user_id'])]

# Step 4: Merge ratings_sample with user data
merged_df = pd.merge(ratings_sample, user_df, on='user_id', how='inner')

# Step 5: Load the business dataset (yelp_academic_dataset_business.json)
business_data = []
with open('yelp_academic_dataset_business.json', 'r') as f:
    for line in f:
        business_data.append(json.loads(line))

# Step 6: Convert the business data into a DataFrame
business_df = pd.DataFrame(business_data)

import pandas as pd
import json

# Step 1: Load the business data
business_data = []
with open('yelp_academic_dataset_business.json', 'r') as f:
    for line in f:
        business_data.append(json.loads(line))

# Step 2: Convert the business data into a DataFrame
business_df = pd.DataFrame(business_data)

# Step 3: Select relevant columns and expand nested fields
# Extract the columns you want
business_df = business_df[
    ['business_id', 'city', 'state', 'latitude', 'longitude', 'stars', 
     'review_count', 'is_open', 'attributes', 'categories', 'hours']
]

# Step 4: Flatten the `attributes` and `hours` columns
# Attributes are JSON-like, so convert them to individual columns
attributes_df = business_df['attributes'].apply(pd.Series)
hours_df = business_df['hours'].apply(pd.Series)

# Step 5: Merge the expanded columns back into the main DataFrame
business_df = pd.concat([business_df, attributes_df, hours_df], axis=1).drop(['attributes', 'hours'], axis=1)

# Step 6: Merge the business data with the previously merged user data
final_df = pd.merge(merged_df, business_df, on='business_id', how='inner')

# Step 7: Save the final merged data to a CSV
final_df.to_csv('sample.csv', index=False)

