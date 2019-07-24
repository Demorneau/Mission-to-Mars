from bs4 import BeautifulSoup
from splinter import Browser
import time
import requests
import pandas as pd
from selenium.common.exceptions import ElementNotVisibleException
import pprint
import json

def init_browser():
    executable_path= {'executable_path':"chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=True)


def mars_nasa():
    marsComplete_data = {}

    # Obtaining Nasa Mars' information
    news_title = requests.get('https://mars.nasa.gov/news/', timeout=3)
    mars_news = BeautifulSoup(news_title.text,'html.parser')
    mars_title = mars_news.find('div', class_='content_title').text
    mars_paragraph = mars_news.find('div', class_='rollover_description_inner').text
    return mars_title, mars_paragraph

    # Obtaining JPL Mars' information
def mars_jpl():
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path = {'executable_path':"chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(featured_image_url)
    html= browser.html
    soup = BeautifulSoup(html, 'html.parser')
    marsian_pic = soup.find('img', class_= 'thumb')['src']
    featured_mars_pic = 'https://www.jpl.nasa.gov' + marsian_pic
    time.sleep(3)
    return browser.visit(featured_mars_pic)
 

    # Obtaining Teewter Mars' Weather information
def mars_allWeather(browser):
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    tweetnews_title = requests.get(mars_weather_url)
    time.sleep(3)
    tweet_weather= BeautifulSoup(tweetnews_title.text, 'html.parser')
    tweetmars_weather = tweet_weather.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    return tweetmars_weather
 
    #Mars' Facts from space-Facts
def mars_facts():
    mars_tableurl = 'https://space-facts.com/mars/'
    mars_tablestring = pd.read_html(mars_tableurl)[0]
    mars_df = pd.DataFrame(mars_tablestring).rename(columns={0:'Mars Facts', 1:'Dimensions'}).set_index('Mars Facts')
    mars_df
    return mars_df.to_html(classes = 'table')

    #Obtaining pics from Mars' Hemispheres
def mars_hemis(browser):
    mars_hemisphere_imgurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path = {'executable_path':"chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(mars_hemisphere_imgurl)
    html= browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_titles = []
    titles = soup.find_all('h3')
    for title in titles:
        hemisphere_titles.append(title.text)
    mars_hemisphere_img_url = []
    #pic_hemisphere_dict = {'title photo':[], 'img_url':[]}
    for pic in range(4):
        browser.find_by_tag('h3')[pic].click()
        html= browser.html
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('h2', class_='title').text
        titles = title.replace('Enhanced','')
        pic_partial_url = soup.find('img',class_='wide-image')['src']
        pic_url = 'https://astrogeology.usgs.gov' + pic_partial_url
        pic_hemisphere_dict = {'title photo': titles, 'img_url':pic_url}
        mars_hemisphere_img_url.append(pic_hemisphere_dict)
        browser.back()
    return hemisphere_titles, mars_hemisphere_img_url

    #Dictionary to accumulate the scraped data

    marsComplete_data = {
        "title": mars_title,
        "paragraph": mars_paragraph,
        "jpl_image": mars_jpl,
        "tweet_weather": tweetmars_weather,
        "facts": mars_table(),
        "hemisphere_img": mars_images
    }

def scrape():
    marsComplete_data = {}

    # Obtaining Nasa Mars' information
    news_title = requests.get('https://mars.nasa.gov/news/', timeout=3)
    mars_news = BeautifulSoup(news_title.text,'html.parser')
    mars_title = mars_news.find('div', class_='content_title').text
    mars_paragraph = mars_news.find('div', class_='rollover_description_inner').text
    marsComplete_data["mars_title"] = mars_title
    marsComplete_data["mars_paragraph"] = mars_paragraph
    print(marsComplete_data)

    # Obtaining JPL Mars' information
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path = {'executable_path':"chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(featured_image_url)
    html= browser.html
    soup = BeautifulSoup(html, 'html.parser')
    marsian_pic = soup.find('img', class_= 'thumb')['src']
    featured_mars_pic = 'https://www.jpl.nasa.gov' + marsian_pic
    time.sleep(3)
    browser.visit(featured_mars_pic)
    time.sleep(3)
    
    #try:
     #   expand = browser.find_by_href('src')
     #   browser.visit(expand)
     #   time.sleep(3)

      #  html= browser.html
      #  soup = BeautifulSoup(html, 'html.parser')
      #  marsian_pic = soup.find('img', class_= 'fancybox-image')['src']  
      #  marsComplete_data["featureMarsPic"] = featured_mars_pic
    #except ElementNotVisibleException as err:
      #  featured_mars_pic = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA17761_ip.jpg'
    marsComplete_data["featureMarsPic"] = featured_mars_pic

    # Obtaining Teewter Mars' Weather information
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    tweetnews_title = requests.get(mars_weather_url)
    time.sleep(3)
    tweet_weather= BeautifulSoup(tweetnews_title.text, 'html.parser')
    tweetmars_weather = tweet_weather.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    marsComplete_data["tweetmars_allweather"] = tweetmars_weather
    pprint.pprint(marsComplete_data)


    #Mars' Facts from space-Facts
    mars_tableurl = 'https://space-facts.com/mars/'
    mars_tablestring = pd.read_html(mars_tableurl)[0]
    mars_df = pd.DataFrame(mars_tablestring).rename(columns={0:'Mars Facts', 1:'Dimensions'}).set_index('Mars Facts')
    mars_df
    mars_table = mars_df.to_html(classes = 'table')
    marsComplete_data["table"] = mars_table

    #Obtaining pics from Mars' Hemispheres
    mars_hemisphere_imgurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path = {'executable_path':"chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(mars_hemisphere_imgurl)
    html= browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('h3')
    mars_hemisphere_img_url = []
    #pic_hemisphere_dict = {'title photo':[], 'img_url':[]}
    for pic in range(4):
        browser.find_by_tag('h3')[pic].click()
        html= browser.html
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('h2', class_='title').text
        titles = title.replace('Enhanced','')
        pic_partial_url = soup.find('img',class_='wide-image')['src']
        pic_url = 'https://astrogeology.usgs.gov' + pic_partial_url
        pic_hemisphere_dict = {'title photo': titles, 'img_url':pic_url}
        mars_hemisphere_img_url.append(pic_hemisphere_dict)
        browser.back()
    marsComplete_data["hemisphere_pics"] = mars_hemisphere_img_url

    return scrape
    browser.quit()
    return marsComplete_data