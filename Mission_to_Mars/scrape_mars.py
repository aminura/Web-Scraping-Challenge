#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time

def scrape ():

    # to control browser
    browser = Browser("chrome", headless=False)

    # visit the NASA Mars News site and scrape headlines
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # give page time to load
    time.sleep(3)

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")

    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Para: {news_paragraph}")

    # visit the JPL website and scrape the featured image
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(url_image)
    time.sleep(1)

    #Getting the base url
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
    print(base_url)

    # Design an xpath selector to grab the image
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    #Use splinter to click on the mars featured image
    #to bring the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url = base_url + img_url
    print(full_img_url)
    # give page time to load
    time.sleep(3)

    # visit the mars weather report twitter and scrape the latest tweet
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    #temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)
    #temp

    # visit space facts and scrap the mars facts table
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[1]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])

    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_html_table

    # give page time to load
    time.sleep(1)

    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    #Getting the base url
    hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
    print(hemisphere_base_url)
   
    # give page time to load
    time.sleep(3)

    # scrape images of Mars' hemispheres from the USGS sitemars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []
    
    for i in range(1,9,2):
        hemi_dict = {}
        
        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hemispheres_html = browser.html
        hemispheres_soup = bs(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
        
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hemi_img_soup = bs(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        hemi_dict['title'] = hemi_name.strip()       
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)

        mars_info["hemisphere_img_urls"]= hemi_dicts

        # make dictionary out of all collected data for later use in flask app
        mars_info={"news_title":news_title,
           "news_paragraph":news_paragraph,
           "featured_image_url":full_img_url,
           "tweet_url":base_url,
           "mars_weather":mars_weather,
           "mars_facts":url_facts,
           "hemisphere_image_urls":hemi_dicts  
          }
    print(mars_info)

    browser.quit()

    return mars_info