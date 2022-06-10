#!/usr/bin/env python
# coding: utf-8

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


slide_elem.find('div', class_='content_title')


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title



# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

#mars facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser = Browser('chrome', **executable_path, headless=False)
browser2 = Browser('chrome', **executable_path, headless=False)
browser.visit(url)



# 2. Create a list to hold the images and titles.
img_urls = []
titles = []


# 3. Write code to retrieve the image urls and titles for each hemisphere.
#tag = browser.find_by_tag("a")
html = browser.html
img_soup = soup(html, 'html.parser')
#print(img_soup.prettify())
item = img_soup.find_all("div", class_ = "item")
for i in item:
    tag = (i.find("a", class_ = "itemLink product-item")).get("href")
    browser2.visit(url + tag)
    html = browser2.html
    img_soup = soup(html, 'html.parser')
    title=img_soup.find("h2", class_ = "title").get_text()
    titles.append(title)
    print(title)
    link = img_soup.find("div", class_ = "downloads")
    link2 = link.find_all("li")[0]
    img_url = (link2.find("a")).get("href")
    img_urls.append(url+img_url)
    print(url+img_url)


hemisphere_image_urls = [{'img_url': img_urls, 'title': titles } for (img_urls, titles) in zip(img_urls, titles)] 

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()






