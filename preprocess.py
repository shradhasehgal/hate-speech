import json
from tqdm import tqdm
from twarc import Twarc
from pathlib import Path
import os
import csv
import re 

# Twarc used to hydrate tweets based on tweet IDs
twarc = Twarc()

# Input dataset
data_dir = "dataset"
input_dataset = os.path.join(data_dir, "input_category.csv")
# Final dataset with processed tweet text
final_dataset = os.path.join(data_dir, "tweets_data.csv")
# Frontend datasets - tweets count and hashtags
frontend_dir = "frontend/src"
hashtags_dataset = os.path.join(frontend_dir, "hashtags_data.csv")
counts_dataset = os.path.join(frontend_dir, "counts_data.csv")

category_map = {}
category_count = {"racism": 0, "sexism": 0, "none": 0}
hashtags_count = {"racism": {}, "sexism": {}, "none": {}}

def main():
    # Mapping tweet IDs to hate class
    with open(input_dataset, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            category_map[row[0]] = row[1]

    # Hydrating each tweet ID
    for path in Path(data_dir).iterdir():
        if path.name.endswith('input.csv'):
            hydrate(path)
    
    # Write hashtags to file
    hashtags_write(hashtags_dataset)
    # Write tweet counts of each class to file
    counts_write(counts_dataset)

def hydrate(id_file):
    with open(final_dataset, 'w') as output:
        linewriter = csv.writer(output, delimiter=',', quotechar="\"")
        linewriter.writerow(["tweet", "hate"])

        for tweet in twarc.hydrate(id_file.open()):
            category = category_map[tweet['id_str']]
            category_count[category] += 1
            
            # Iterate over all hashtags in a tweet and increment hashtag count for that class
            if "hashtags" in tweet["entities"]:
                hashtags_list = tweet["entities"]["hashtags"]
                for hashtag in hashtags_list:
                    hashtagText = hashtag["text"].lower()
                    if hashtagText in hashtags_count[category]:
                        hashtags_count[category][hashtagText] += 1
                    else:
                        hashtags_count[category][hashtagText] = 1
            
            # Lowercasing text
            text = tweet['full_text'].lower()
            
            # Removing punctuation
            text = re.sub(r'[^\w\s]', '', text)
            if category == "racism" or category == "sexism":
                # Hateful = 1
                linewriter.writerow([text, 1]) 
            else:
                # Non-hateful = 0
                linewriter.writerow([text, 0]) 

# Function to write hashtags to file
def hashtags_write(id_file):
    for category in hashtags_count.keys():
        hashtags_count[category] = {k: v for k, v in sorted(hashtags_count[category].items(), key=lambda item: -item[1])}

    with open(hashtags_dataset, 'w') as output:
        linewriter = csv.writer(output, delimiter=',', quotechar="\"")
        linewriter.writerow(["hashtag", "count", "category"])
        for category,hashtags in hashtags_count.items():
            for hashtag,count in hashtags.items():
                linewriter.writerow([hashtag, count, category]) 

# Function to write tweets count for each class 
def counts_write(id_file):
    with open(counts_dataset, 'w') as output:
        linewriter = csv.writer(output, delimiter=',', quotechar="\"")
        linewriter.writerow(["category", "count"])
        for category,count in category_count.items():
            linewriter.writerow([category, count]) 

if __name__ == "__main__":
    main()