import requests
from time import sleep 
import re
import pandas as pd
import json
import os
from bs4 import BeautifulSoup

class GoogleScholarScraper:
    def __init__(self,
                 headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}
                 ):
        self.headers = headers  ## define header to access google scholar website
        self.df = {
            "paper_title": [],
            "cite_count": [],
            "years": [],
            "publication": [],
            "authors": []
        }
        self.labels_dict = {}
        self.num_examples = 0

    ## Main
    def run(self, topics, num_paper_per_topic=10, wait=40, output_dir="data/"):
        for topic in topics:
            topic_str = "+".join(topic.lower().split())
            self.labels_dict[topic] = [_ for _ in range(self.num_examples, self.num_examples+num_paper_per_topic)]
            print("Working on topic: ", topic_str)
            for i in range(0,num_paper_per_topic,10):
                url = f"https://scholar.google.com/scholar?start={i}&q={topic_str}&hl=en&as_sdt=0,5"
                doc = self.get_paperinfo(url)
                paper_tag,cite_tag,author_tag = self.get_tags(doc)
                self.get_papertitle(paper_tag)
                self.get_citecount(cite_tag)
                self.get_author_year_publi_info(author_tag)
                self.num_examples += 10
                sleep(wait)
        ## Save data
        df = pd.DataFrame(self.df)
        df.to_csv(os.path.join(output_dir,"raw_data.csv"), index=False)
        with open(os.path.join(output_dir,"labels_dict.json"), 'w') as f:
            json.dump(self.labels_dict, f)

    
    ## Getting inforamtion of the web page
    def get_paperinfo(self, url):
        response = requests.get(url,headers=self.headers) # download the page
        if response.status_code != 200: # check successful response
            print('Status code:', response.status_code)
            raise Exception('Failed to fetch web page ')
        #parse using beautiful soup
        doc = BeautifulSoup(response.text,'html.parser')
        return doc
    
    ## Extracting information of the tags
    def get_tags(self, doc):
        paper_tag = doc.select('[data-lid]')
        cite_tag = doc.select('a:-soup-contains("Cited by")')
        author_tag = doc.find_all("div", {"class": "gs_a"})
        return paper_tag,cite_tag,author_tag
    
    ## Title of the paper
    def get_papertitle(self, paper_tag):
        for tag in paper_tag:
            self.df["paper_title"].append(tag.select('h3')[0].get_text())

    ## Number of citation of the paper
    def get_citecount(self, cite_tag):
        for i in cite_tag:
            cite = i.text
            if i is None or cite is None:  # if paper has no citatation then consider 0
                self.df["cite_count"].append(0)
            else:
                tmp = re.search(r'\d+', cite) # return only integer value
                if tmp is None :
                    self.df["cite_count"].append(0)
                else :
                    self.df["cite_count"].append(int(tmp.group()))

    # function for the getting autho , year and publication information
    def get_author_year_publi_info(self, authors_tag):
        for i in range(len(authors_tag)):
            authortag_text = (authors_tag[i].text).split()
            year = int(re.search(r'\d+', authors_tag[i].text).group())
            self.df["years"].append(year)
            self.df["publication"].append(authortag_text[-1])
            author = authortag_text[0] + ' ' + re.sub(',','', authortag_text[1])
            self.df["authors"].append(author)
    
if __name__ == '__main__':
    scraper = GoogleScholarScraper()
    demo_topics = ["object detection", "face recognition", "biological vision", "face anti spoofing", "object recognition",
                   "name entity recognition", "sentiment analysis", "text summarization", "machine translation", "topic modelling"]
    scraper.run(topics=demo_topics, num_paper_per_topic=30, wait=60, output_dir="data/")
    print(scraper.df)