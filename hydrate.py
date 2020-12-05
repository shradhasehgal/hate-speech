import json
from tqdm import tqdm
from twarc import Twarc
from pathlib import Path
import os
from csv import reader

twarc = Twarc()
data_dir = "dataset"
input_dataset = os.path.join(data_dir, "input_category.csv")
final_dataset = os.path.join(data_dir, "final_data.json")
category_map = {}

def main():
    with open(input_dataset, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            category_map[row[0]] = row[1]

    for path in Path(data_dir).iterdir():
        if path.name.endswith('input.csv'):
            hydrate(path)

def hydrate(id_file):
    with open(final_dataset, 'w') as output:
        for tweet in twarc.hydrate(id_file.open()):
            category = category_map[tweet['id_str']]
            tweet['category'] = category
            output.write(json.dumps(tweet))
            output.write('\n')

if __name__ == "__main__":
    main()