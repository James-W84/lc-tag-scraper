import re
import requests
import json

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

def tags_from_lc_url(url):
    match = re.search(url_pattern, url)
    if match:
        try:
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
            return tags
        except:
            raise AttributeError("No tag data found") 
