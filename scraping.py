# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "Hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    print(data["featured_image"])
    print(data["Hemispheres"])

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com/' #'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    print(full_image_elem)
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        print(img_url_rel)
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    mars_hemispheres = []

# # 3. Write code to retrieve the image urls and titles for each hemisphere.
    tag = browser.find_by_tag("a")
    html = browser.html
    img_soup = soup(html, 'html.parser')
# #print(img_soup.prettify())
    item = img_soup.find_all("div", class_ = "item")
    for i in item:
        dic = {}
        tag = (i.find("a", class_ = "itemLink product-item")).get("href")
        browser.visit(url + tag)
        html = browser.html
        img_soup = soup(html, 'html.parser')
        title=img_soup.find("h2", class_ = "title").get_text()
        dic["title"] = title
        link = img_soup.find("div", class_ = "downloads")
        link2 = link.find_all("li")[0]
        img_url = (link2.find("a")).get("href")
        dic["img_url"] = (url+img_url)
        mars_hemispheres.append(dic)
        browser.back() 
    return mars_hemispheres






# def hemispheres(browser):
#     url = 'https://marshemispheres.com/'
#     browser.visit(url)

#     html = browser.html
#     img_soup = soup(html, 'html.parser')

#     hemi_urls = []
#     hemi_titles = []

#     item = img_soup.find_all("div", class_ = "item")
#     for i in item:
#         tag = (i.find("a", class_ = "itemLink product-item")).get("href")
#         browser.visit(url + tag)

#         html = browser.html
#         img_soup = soup(html, 'html.parser')
#     try:
#         title=img_soup.find("h2", class_ = "title").get_text()
#         hemi_titles.append(title)
#         #print(title)
#         link = img_soup.find("div", class_ = "downloads")
#         link2 = link.find_all("li")[0]
#         img_url = (link2.find("a")).get("href")
#         hemi_urls.append(url+img_url)
#     except AttributeError:
#         return None
#         #print(url+img_url)
#     browser.back()
#     hemispheres_ = [{'img_url': hemi_urls, 'title': hemi_titles } for (hemi_urls, hemi_titles) in zip(hemi_urls, hemi_titles)] 
#     return hemi_urls, hemi_titles


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())