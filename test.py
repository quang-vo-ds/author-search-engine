import requests
from time import sleep 
import re
import pandas as pd
from bs4 import BeautifulSoup

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
url = "https://scholar.google.com/scholar?start=10&q=object+detection+in+aerial+image+&hl=en&as_sdt=0,5"

def get_paperinfo(url):

  #download the page
  response=requests.get(url)

  # check successful response
  if response.status_code != 200:
    print('Status code:', response.status_code)
    raise Exception('Failed to fetch web page ')

  #parse using beautiful soup
  paper_doc = BeautifulSoup(response.text,'html.parser')

  return paper_doc

def get_tags(doc):
  paper_tag = doc.select('[data-lid]')
  cite_tag = doc.select('[title=Cite] + a')
  link_tag = doc.find_all('h3',{"class" : "gs_rt"})
  author_tag = doc.find_all("div", {"class": "gs_a"})

  return paper_tag,cite_tag,link_tag,author_tag

# paper title from each page
def get_papertitle(paper_tag):
  paper_names = []
  for tag in paper_tag:
    paper_names.append(tag.select('h3')[0].get_text())
  return paper_names

doc = get_paperinfo(url)
paper_tag,cite_tag,link_tag,author_tag = get_tags(doc)
print(doc)
print(get_papertitle(author_tag))