from bs4 import BeautifulSoup
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from webdriver_manager.core.utils import ChromeType
import json
from sys import argv


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=OFF')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--enable-low-end-device-mode")
chrome_options.add_argument("--renderer-process-limit=2")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--disable-extensions")


rows = []
url = f'{argv[1]}'
here = os.path.dirname(os.path.abspath(__file__))
s = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
browser = webdriver.Chrome(service=s, options=chrome_options )




def get_page_info():    
    browser.get(url)
    time.sleep(5)
    browser.find_element(By.XPATH, '//button[@aria-label="REVIEWS tab, 2 of 3"]').click()
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    reviews_names = soup.find_all('div', {'class': 'ReviewCards-module__reviewUserName___3m-MD'})
    names = []
    for name in reviews_names:
        name_text = name.text
        names.append(name_text)
    
    reviews_dates = soup.find_all('p', {'class': 'ReviewCards-module__reviewDateNoUserActions___3WgJL'})
    dates = []
    for date in reviews_dates:
        date_text = date.text
        dates.append(date_text)
        
    reviews_platforms = soup.find_all('div', {'class': 'commonStyles-module__basicContainer___ZmTki FeaturesList-module__item___19NYe typography-module__xdsTag3___dtX8u'})
    platforms = []
    for plat in reviews_platforms:
        plat_text = plat.text
        platforms.append(plat_text)
        
    reviews_titles = soup.find_all('div', {'class': 'Row-module__row___1VeVT typography-module__xdsH6___RhUR_ ReviewCards-module__reviewTitle___3zHNM'})
    titles = []
    for title in reviews_titles:
        title_text = title.text
        titles.append(title_text)
    reviews_list = soup.find_all('p', {'class': "ReviewCards-module__shadowCloneText___1kUNE"})
    texts = []
    for review in reviews_list:
        review_text = review.text
        texts.append(review_text)
        
    for i in range(len(titles)):
        full_review = {'name': names[i],
                       'date': dates[i],
                       'platform': platforms[i],
                       'title': titles[i],
                       'text': texts[i]}
        review_json = json.dumps(full_review)
        rows.append(review_json)
        
    browser.close()
    return rows


if __name__ == '__main__':
    print(get_page_info())
    