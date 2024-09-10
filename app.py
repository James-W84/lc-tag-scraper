import argparse
import csv
from query import tags_from_lc_url
import json

import threading
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(
                    prog='Leetcode Tag Scraper',
                    description='Given a CSV of leetcode questions associated with a company, generate a list of question tags sorted by frequency',)

parser.add_argument('filename')

args = parser.parse_args()
filename = args.filename

tag_dict = {}
cnf = []

locks = {}
cnf_lock = threading.Lock()

def process_row(url):
    try:
        tags = tags_from_lc_url(url)
        for tag in tags:
            slug = tag['slug']
            if slug in tag_dict:
                with locks[slug]:
                    tag_dict[slug] += 1
            else:
                locks[slug] = threading.Lock()
                with locks[slug]:
                    tag_dict[slug] = 1
    except:
        with cnf_lock:
            print(url)
            cnf.append(url)

with open(f'src/{filename}.csv', 'r') as file:
    csvreader = csv.reader(file)
    fields = next(csvreader)

    with ThreadPoolExecutor(max_workers=8) as executor:

        for row in csvreader:
            url = row[-1]
            executor.submit(process_row, url)
                

sorted_dict = dict(sorted(tag_dict.items(), key=lambda item: item[1], reverse=True))

print(json.dumps(sorted_dict, indent=4))

if len(cnf) > 0:
    print("Could not find tags for these questions:")
    print(cnf)  