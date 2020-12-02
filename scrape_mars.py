# Import Dendencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

# Init Splinter Browser
def init_browser():
    # MAC
    # executable_path = { 'executable_path': '/usr/local/bin/chromedriver' }
    
    # WINDOWS
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # Init Splinter Browser
    browser = init_browser()

    news_title = ""
    news_p = ""
    featured_image_url = ""
    mars_fact_html_string = ""
    hemisphere_image_urls = []

    try:
        
        #################################################
        # Scrape - NASA Mars News
        #################################################
        
        # URL of page to be scraped
        url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

        # Open webpage
        browser.visit(url1)
        
        # Wait 3 seconds for the page to load before scraping
        time.sleep(3)

        # Retrieve HTML webpage source
        html1 = browser.html

        # Parse HTML webpage source using BeautifulSoup
        soup1 = BeautifulSoup(html1, 'html.parser')

        # Scrape the latest news title and paragraph
        result1 = soup1.find('div', class_='list_text')
        news_title = result1.find('div', class_='content_title').text
        news_p = result1.find("div", class_="article_teaser_body").text
        
        #################################################
        # Scrape - JPL Mars Space Images - Featured Image
        #################################################

        # URL of page to be scraped
        url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

        # Open webpage
        browser.visit(url2)

        # Retrieve HTML webpage source
        html2 = browser.html

        # Parse HTML webpage source using BeautifulSoup
        soup2 = BeautifulSoup(html2, 'html.parser')

        # Scrape the Featured Image URL
        divs = soup2.find_all('div', class_='carousel_items')
        for div in divs:
            article = div.find('article', class_='carousel_item')
            featured_img = article['style'].split("url('")[1].split("');")[0]
            featured_image_url = f'https://www.jpl.nasa.gov{featured_img}'

        #################################################
        # Scrape - Mars Facts
        #################################################

        # URL of page to be scraped
        url3 = 'https://space-facts.com/mars/'

        # Use Pandas to scrape the tables from the URL
        dfs = pd.read_html(url3)

        # Mars fact Dataframe 
        mars_fact_df = dfs[0]
        mars_fact_df = mars_fact_df.rename(columns={0:'Description',
                                                    1:'Mars'})

        # Convert the data to a HTML table string
        mars_fact_html_string = mars_fact_df.to_html(index=False, classes=['table','table-striped'], border=0, justify='left')

        #################################################
        # Scrape - Mars Hemispheres
        #################################################

        # URL of page to be scraped
        url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        # Open webpage
        browser.visit(url4)

        # Retrieve HTML webpage source
        html3 = browser.html

        # Parse HTML webpage source using BeautifulSoup
        soup3 = BeautifulSoup(html3, 'html.parser')

        # Scrape the Mars Hemisphere Titles
        h3s = soup3.find_all('h3')
        hemisphere_links = [h3.text for h3 in h3s]

        # Variable to hold the list of Mars Hemisphere dictionary
        hemisphere_image_urls = []

        # Loop through the Mars Hemisphere Titles
        for hemisphere_link in hemisphere_links:
            
            # Find the link with the title and click on the link
            browser.links.find_by_partial_text(hemisphere_link).click()
            
            # Retrieve HTML webpage source
            html4 = browser.html
            
            # Parse HTML webpage source using BeautifulSoup
            soup4 = BeautifulSoup(html4, 'html.parser')

            # Scrape the image url string for the full resolution hemisphere image
            original_imgs = soup4.find_all('a', href=True, text='Sample')
            for original_img in original_imgs:
                original_img_url = original_img['href']

            # Scrape the Hemisphere title containing the hemisphere name
            title_tag = soup4.find('h2', class_='title')
            title = title_tag.text

            # Add the Mars Hemisphere dictionary to the list
            hemisphere_image_urls.append({'title': title, 'img_url':original_img_url})

            # Go back to previous page
            browser.visit(url4)
    except:
        print('Error scraping')
    
    scrape_mars_list = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_fact_html_string': mars_fact_html_string,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    browser.quit()

    return scrape_mars_list
