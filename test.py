
import pandas as pd
import numpy as np
import requests
import time
from bs4 import BeautifulSoup

article_info = []

# range(first_page, last_page)
for i in range(0, 20, 10):
    page = requests.get("https://scholar.google.com/scholar?start=" + str(i) + "&q=mitochondrial+synthesis&hl=en&as_sdt=0,5&as_ylo=2020&as_yhi=2022&as_rr=1")
    # sleep between requests
    time.sleep(60)
     
    soup = BeautifulSoup(page.text, 'html.parser')
    article_names = soup.findAll('div', attrs={'class':'gs_r gs_or gs_scl'})
    for store in article_names:
        title = store.h3.a.text
        url = store.h3.a
        article_info.append([title, url['href']])

article_list = pd.DataFrame(article_info)

# write to CSV
print(article_list)
article_list.to_csv('data/raw_data.csv', index=False)