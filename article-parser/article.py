import requests
import json
import sys

from bs4 import BeautifulSoup

url = sys.argv[1]

response = requests.get(url)

article = {}
# à remplacer à la main
article['id'] = 000
article['url'] = url
# à remplacer à la main
article['personality'] = ''

soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")

article_title = soup.find("h1", {"class": "article__title"}).text
article_heading = soup.find("p", {"class": "article__desc"}).text
article_publication = soup.find("span", {"class": "meta__date"}).text

article_nodes = soup.find_all(["p", "h2"], {"class": ["article__paragraph", "article__sub-title"]})

nodes = []

publicationNode = {}
publicationNode['type'] = 'publication'
publicationNode['content'] = article_publication
nodes.append(publicationNode)

titleNode = {}
titleNode['type'] = 'title'
titleNode['content'] = article_title
nodes.append(titleNode)

headingNode = {}
headingNode['type'] = 'heading'
headingNode['content'] = article_heading
nodes.append(headingNode)

for node in article_nodes:
  if node.has_attr('class'):
    newNode = {}
    if node['class'][0] == 'article__paragraph':
      newNode['type'] = 'paragraph'
      newNode['content'] = node.text
    if node['class'][0] == 'article__sub-title':
      newNode['type'] = 'subtitle'
      newNode['content'] = node.text
    nodes.append(newNode)

article['nodes'] = nodes

with open('article.json', 'w', encoding='utf8') as json_file:
    json.dump(article, json_file, ensure_ascii=False)
