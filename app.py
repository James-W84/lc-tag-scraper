import argparse
import re
import requests
import csv
import json


parser = argparse.ArgumentParser(
                    prog='Leetcode Tag Scraper',
                    description='Given a CSV of leetcode questions associated with a company, generate a list of question tags sorted by frequency',)

parser.add_argument('filename')

args = parser.parse_args()
filename = args.filename

url_pattern = r'https://leetcode\.com/problems/([^/]+)'
api_endpoint = 'https://leetcode.com/graphql/'
headers = {
    'Content-Type': 'application/json',
    'Host': 'leetcode.com',
    'Cookies': '',
    'x-csrftoken': '',

}

query = """
query singleQuestionTopicTags($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    topicTags {
      name
      slug
    }
  }
}
"""

tag_dict = {}


with open(f'src/{filename}.csv', 'r') as file:
    csvreader = csv.reader(file)
    fields = next(csvreader)

    for row in csvreader:
        url = row[-1]
        match = re.search(url_pattern, url)
        if match:
            title_slug = match[1]
            response = requests.post(
                url=api_endpoint,
                headers=headers,
                data=json.dumps({
                    'query': query,
                    'variables': {
                        'titleSlug': title_slug
                    }
                })
            )
            data = response.json()
            tags = data['data']['question']['topicTags']
            for tag in tags:
                slug = tag['slug']
                if slug in tag_dict:
                    tag_dict[slug] += 1
                else:
                    tag_dict[slug] = 1

print(tag_dict)