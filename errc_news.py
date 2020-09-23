#importing libraries
import requests
from bs4 import  BeautifulSoup
import pandas as pd


def get_errc_data(num_pages = 1):
    #creating urls
    t=[]


    for i in range(1,num_pages+1):

        base_url = "http://www.errc.org/media/news"+"?page="+str(i)
        url_to_con = "http://www.errc.org"
        response = requests.get(base_url)
        print(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text)
            #the titles are not finished there so I just get the links and navigate there
            # the css selector should be "post h3 a", BUT FOR NOW IT WORKS
            links = soup.select(".post h3")
            
            
            #empty dict after which will be data frame,its faster(https://stackoverflow.com/questions/10715965/add-one-row-to-pandas-dataframe/10716007)
            di = {"link":[],
            "title":[],
            "date":[],
            "author":[],
            "text":[]}
            
            for link in links:
                article = link.select("a")[0]['href']
                article = url_to_con+article
                resp = requests.get(article)
                s = BeautifulSoup(resp.text)
                link = article
                title = s.select("h1")[0].text
                
                date = s.select("p.date")[0].text
                
                author = s.select("strong")[0].text
                
                text = s.select("p:nth-of-type(n+4)")
                temp = []
                #for now I will loop through the text and get the text like this
                for paragraph in text:
                    temp.append(paragraph.text)
                text = ' '.join([str(elem) for elem in temp]) 

                
                di['link'].append(link)
                di['title'].append(title)
                di['date'].append(date)
                di['author'].append(author)
                di['text'].append(text)
        t.append(pd.DataFrame(di))

    return t
