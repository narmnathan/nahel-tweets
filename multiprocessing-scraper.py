from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import multiprocessing

# from selenium-twitter-scraper, refer to guide if necessary

tweets = []
errors = [] # for scraping errors
columns = ['username', 'tweet_date', 'tweet_text', 'tweet_link', 'media_exists']

df_emeutes = pd.read_csv('emeutes.csv')
df_france = pd.read_csv('france.csv')
df_franceriots = pd.read_csv('franceriots.csv')
df_nael = pd.read_csv('nael.csv')
df_nahel = pd.read_csv('nahel.csv')
df_nanterre = pd.read_csv('nanterre.csv')

def scrape(link):
    # replacing twitter link with nitter to make scraping easier
    nitter_link = link.replace("twitter.com", "nitter.net", 1)
    
    # selenium web driver
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (compatible; MSIE 11.0; Windows NT 6.3; Trident/7.0)")
    options = webdriver.FirefoxOptions() 
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get(nitter_link)
    
    # waiting for elements to load
    time.sleep(1)
    
    # getting variables
    username = driver.find_element(By.XPATH, "//a[@class='username']").text
    tweet_date = driver.find_element(By.XPATH, "//span[@class='tweet-date']/a[@title]").get_attribute("title")
    tweet_text = driver.find_element(By.XPATH, "//div[@class='tweet-content media-body']").text
    
    try:
        tweet_media = driver.find_element(By.XPATH, "//div[@class='attachments card']")
    except:
        media_exists = False
    else:
        media_exists = True
        
    # adding to list
    row = [username, tweet_date, tweet_text, link, media_exists]
    tweets.append(row)
    
    # suspending driver
    driver.quit()
    
def add(list):
    while True:
        prompt = input("Enter a tweet, or 'exit' to exit. Count: " + str(len(list)))
        if prompt == 'exit':
            break
        else:
            list.append(prompt)
            
def load(link):
        try:
            print('Scraping link: ' + link)
            scrape(link)
        except:
            print('Error!')
            errors.append(link)

def process(list):
    list['tweets'].apply(load)

if __name__ == "__main__":
    processes = 6
    
    pool = multiprocessing.Pool(processes)
    
    lists = [df_emeutes, df_france, df_franceriots, df_nael, df_nahel, df_nanterre]
    
    pool.map(process, lists)
    
    pool.close()
    pool.join()
    
    df_tweets = pd.DataFrame(tweets, columns=columns)
    df_tweets.to_csv('tweets.csv', index=False)

    df_errors = pd.DataFrame(errors, columns=[['tweets']])
    df_errors.to_csv('errors.csv', index=False)

# find a way to minimize memory usage
# and prevent ip from being blocked

