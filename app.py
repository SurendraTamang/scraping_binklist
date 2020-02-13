import requests
from lxml import html
import json
import pandas as pd
response = requests.get('https://www.blinkist.com/en/sitemap')
page = html.fromstring(response.content)
tree = page.xpath('//div[@class="sitemap-section"]//ul[@class="sitemap-links"]/li/a/@href')
books = [i for i in tree if "https://www.blinkist.com/en/books" in i]

files = dict()
count = 0
for url in books:
    res = requests.get(url)
    page = html.fromstring(res.content)
    title = '//h2[@class="book-sample-info__title"]/text()'
    sub_title = '//h4[@class="book-sample-info__subtitle"]/text()'
    author =  '//div[@class="book-sample-info__author"]/text()'
    synopsis = '//div[@class="book-sample-info__about-text"]/p//text()'
#joini
    keyideas = '//span[@class="book-sample-reader__chapters-label"]'
    abract = '//div[@class="book-sample-reader__text reader-text"]/h2/text()'
    summary = '//div[@class="book-sample-reader__text reader-text"]/p'
    try:
        title = page.xpath(title)[0].strip()
    except:
        title = "DELETE"
    ftitle = title.replace("#",'').replace('"','')
    title = title.replace('"','')
    try:
        sub_title = page.xpath(sub_title)[0].strip()
    except:
        sub_title = False
    try:
        author = page.xpath(author)[0].replace('By','').strip()
    except:
        author = 'DELETE'
    syp = page.xpath(synopsis)
    synopsis = ' '.join(syp).replace('#','')
    key_ideas = page.xpath(keyideas)
    try:
        key_ideas = [i.xpath('.//text()')[0].strip() for i in key_ideas]
    except:
        key_ideas = 'DELETE'
    abstract = page.xpath(abract)
    try:
        abstract = abstract[0].strip()
    except:
        abstract = 'DELETE'
    sumar = page.xpath(summary)
    try:
        summary = [i.xpath('.//text()')[0].strip() for i in sumar]
    except KeyError:
        summary = False
    if sub_title:
        files[ftitle] = {"title":title,"subtitle":sub_title,"author":author,"synopsis":synopsis,"abstract":abstract,"summary":summary,"key_ideas":key_ideas}
    else:
        files[ftitle] = {"title":title,"author":author,"synopsis":synopsis,"abstract":abstract,"summary":summary,"key_ideas":key_ideas}
    print(count)
    count = count + 1
    
ff = pd.DataFrame.from_dict(files)
    
ff.to_json('whole_data.json')
    
        
