import requests
from time import sleep 
import re
import pandas as pd
from bs4 import BeautifulSoup

class GoogleScholarScraper:
    def __init__(self,
                 headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
                 ):
        self.headers = headers  ## define header to access google scholar website
        self.paper_title = []
        self.cite_count = []
        self.years = []
        self.publication = []
        self.authors = []

    ## Main
    def run(self, topics, num_paper_per_topic=10, wait=40):
        for topic in topics:
            topic_str = "+".join(topic.lower().split())
            for i in range(0,num_paper_per_topic,10):
                url = f"https://scholar.google.com/scholar?start={i}&q={topic_str}&hl=en&as_sdt=0,5"
                doc = self.get_paperinfo(url)
                paper_tag,cite_tag,author_tag = self.get_tags(doc)
                self.get_papertitle(paper_tag)
                self.get_citecount(cite_tag)
                self.get_author_year_publi_info(author_tag)
                sleep(wait)
        ## Save as csv
        df = pd.DataFrame({
                    'Paper Title' : self.paper_title,
                    'Year' : self.years,
                    'Author' : self.authors,
                    'Citation' : self.cite_count,
                    'Publication' : self.publication
                    })
        df.to_csv('data/raw_data.csv', index=False)

    
    ## Getting inforamtion of the web page
    def get_paperinfo(self, url):
        response = requests.get(url,headers=self.headers, proxies=self.proxies) # download the page
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
            self.paper_title.append(tag.select('h3')[0].get_text())

    ## Number of citation of the paper
    def get_citecount(self, cite_tag):
        for i in cite_tag:
            cite = i.text
            if i is None or cite is None:  # if paper has no citatation then consider 0
                self.cite_count.append(0)
            else:
                tmp = re.search(r'\d+', cite) # return only integer value
                if tmp is None :
                    self.cite_count.append(0)
                else :
                    self.cite_count.append(int(tmp.group()))

    # function for the getting link information
    def get_link(self, link_tag):
        for i in range(len(link_tag)):
            self.links.append(link_tag[i].a['href'])

    # function for the getting autho , year and publication information
    def get_author_year_publi_info(self, authors_tag):
        for i in range(len(authors_tag)):
            authortag_text = (authors_tag[i].text).split()
            year = int(re.search(r'\d+', authors_tag[i].text).group())
            self.years.append(year)
            self.publication.append(authortag_text[-1])
            author = authortag_text[0] + ' ' + re.sub(',','', authortag_text[1])
            self.authors.append(author)
    
if __name__ == '__main__':
    scraper = GoogleScholarScraper()
    demo_topics = ["object detection", "face recognition", "biological vision"]
    scraper.run(topics=demo_topics, num_paper_per_topic=10, wait=45)
    print(scraper.authors)