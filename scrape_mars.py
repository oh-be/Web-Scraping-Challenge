from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    list_text = soup.find_all('div', class_='list_text')
    try:
        content_title = list_text[0].find('div', class_ = 'content_title')
        news_title = content_title.text.strip()
        article_teaser_body = list_text[0].find('div', class_ = 'article_teaser_body')
        news_p = article_teaser_body.text.strip()
    except AttributeError:
        return None, None
    return news_title, news_p

def featured_image(browser):
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = url + soup.find('img', class_='headerimage fade-in')['src']
    return featured_image_url

def mars_facts(browser):
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    mars_facts = pd.read_html(url)
    mars_facts = mars_facts[0]
    mars_facts.columns = ['Comparison', 'Mars', 'Earth']
    mars_facts = mars_facts.drop(index=0)
    mars_facts.set_index('Comparison', inplace=True)
    return mars_facts.to_html(classes="table table-striped")

def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    sidebar = soup.find('div', class_='collapsible')

    categories = sidebar.find_all('h3')
    hemisphere_img_urls = []

    for item in range(len(categories)):
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[item].click()
        
        sample_img = browser.links.find_by_text("Sample").first
        
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere["img_url"] = sample_img["href"]     
        
        hemisphere_img_urls.append(hemisphere)
        
        browser.back()
    return hemisphere_img_urls

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    featured_image_url = featured_image(browser)
    facts = mars_facts(browser)
    hemisphere_image_urls = hemispheres(browser)

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
    }

    browser.quit()
    return mars_data

if __name__ == "__main__":
    data = scrape_all()
    print(data)