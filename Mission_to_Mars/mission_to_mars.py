#!/usr/bin/env python
# coding: utf-8

# In[268]:


# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo

def scrape():
    # Define splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit website and store html code as soup
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Extract and store latest news_title and information
    news_title = soup.find_all('div',class_='content_title')[0].text
    news_p= soup.find_all('div',class_='article_teaser_body')[0].text
    print(news_title)
    print("---------------")
    print(news_p)
    print("---------------")

    # Visit website, click on feature image and extract html as soup
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    browser.links.find_by_partial_text('FULL IMAGE').click()
    soup = BeautifulSoup(html, 'html.parser')

    # Extract url of featured image
    b=soup.find_all('img')[1]['src']
    featured_image_url = url +b
    print(featured_image_url)
    print("---------------")

    # Visit New website and extract tables with pandas
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    tables = pd.read_html(url)

    # Select table required and rename column header
    df = tables[0]

    # Transform Table into html code
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    table_header = [df[0][0],df[1][0],df[2][0]]
    table_data=[[df[0][x+1],df[1][x+1],df[2][x+1]] for x in range(len(df[0])-1)]
    print(table_header)
    print("---------------")
    print(table_data)
    print("---------------")

    # Visit new website and store html code as soup
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find Url of individual hemisphere website
    x=soup.find_all('div',class_="description")
    url_list=[]
    for a in x:
        b=a.find('a', class_="itemLink")['href']
        url_list.append(url+b)

    # Visit individual website and append information into a list
    hemisphere_image_urls = []
    for x in url_list:
        url_x = x
        browser.visit(url_x)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2').text.replace(' Enhanced', '')
        img_url = url + soup.find_all('li')[0].find('a')['href']
        hemisphere_image_urls.append({"title": title, "img_url":img_url})
    print (hemisphere_image_urls)
    print("---------------")

    # Create connection variable
    conn = 'mongodb://localhost:27017'

    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = client.Mars_db

    # Drops collection if available to remove duplicates
    db.details.drop()

    # Creates a collection in the database and inserts two documents
    db.details.insert_one(
            {
                'news_title': news_title,
                'news_p': news_p,
                'featured_image_url':featured_image_url,
                'html_table':html_table,
                'hemisphere_image_urls':hemisphere_image_urls,
                'table_header':table_header,
                'table_data':table_data
            }
    )

    # Close splinter window
    browser.quit()