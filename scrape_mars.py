# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # start a dictionary to store all the scraped data
    mars_dict = {}

    ### Scrape the 1st news article about nasa mars missions.
    # URL of 1st page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')
    # The first news title and article text
    news_title = news_soup.find('div', class_='content_title').a.text.strip()
    news_text = news_soup.find('div', class_="rollover_description_inner").text.strip()
    mars_dict = {
        'title': news_title,
        'article': news_text
        }

    ### Scrape the current featured JPL Mars image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')
    featured_image_url = 'https:' + img_soup.find_all('div', class_="download_tiff")[1].p.a['href']
    mars_dict['image_url'] = featured_image_url

    ###Scrape the latest Mars weather tweet
    # URL of 1st page to be scraped
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    weather_response = requests.get(weather_url)
    # Create BeautifulSoup object
    weather_soup = BeautifulSoup(weather_response.text)
    mars_weather = weather_soup.find('p', class_='tweet-text').contents[0]
    mars_dict['mars_weather'] = mars_weather

    ### Scrape Mars Facts using PANDAS
    facts_url = 'https://space-facts.com/mars/'
    table_df = pd.read_html(facts_url, index_col=0)[0]
    html_table = table_df.to_html(header=False)
    mars_dict['html_table'] = html_table

    ### scrape links to the 4 full hemisphere images of Mars
    maps_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(maps_url)
    hemisphere_links = browser.find_link_by_partial_text('Hemisphere')
    hemisphere_image_urls = []
    for link in range(len(hemisphere_links)):
        browser.find_link_by_partial_text('Hemisphere')[link].click()
        img_url=browser.find_link_by_partial_text('Sample')['href']
        title = browser.find_by_tag('h2').text
        hemisphere_image_urls.append(
            {'title': title,
            'img_url': img_url
        })
        browser.back()
    browser.quit()
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict

