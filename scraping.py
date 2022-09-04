
# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():

    # Initiate headless driver for deployment 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Set news title and paragraph variables from mars_news function return output
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()


    return data

# ### NASA - Mars News

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div,list_text', wait_time=1)

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

# ### JPL Space Images Featured

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ### Mars Facts

def mars_facts():

    # Add try/except for error handling
    try:

        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped table-hover")

# ### Hemispheres

def hemispheres(browser):

    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles
    hemisphere_image_urls = []

    # Create for loop to iterate through each full image elem... click on every other html link found to iterate
    # over a range from 1-7, incrementing by 2 in order to click each of the 4 full image elem links
    for i in range(1, 8, 2):
        # Initialize empy dictionary variable to add 'image link: title' key-value pair from scraping results
        hemispheres = {}
        
        # Search for the full image elem link by partial href value and click on the element
        full_image_elem = browser.links.find_by_partial_href('.html')
        full_image_elem[i].click()
        
        # Parse the html from the web page
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        try:

            # Search for the 'a' tag containg the href full image link within the div container with the class 'downloads',
            # and scrape the href value (the relative url). Then concatenate the relative url with the base url
            img_url_rel = img_soup.find('div', class_='downloads').find('a').get('href')
            img_url = f'{url}{img_url_rel}'
                    
            # Search for the image title in the 'h2' header tag with the 'title' class
            title = img_soup.find('h2', class_='title').get_text()
                    
        except AttributeError:
            
            return None

        # Add full image url and title key-value pairs to hemispheres dictionary.
        # Then append the hemispheres dictionary to the hemisphere image urls list.
        hemispheres.update({'img_url': img_url, 'title': title})
        hemisphere_image_urls.append(hemispheres)
        
        # Use the browser to click 'back' to allow next loop iteration to click on the next full image elem link.
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
