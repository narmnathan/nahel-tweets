from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import concurrent.futures

# from selenium-twitter-scraper, refer to guide if necessary

tweets = []
errors = [] # for scraping errors
columns = ['username', 'tweet_date', 'tweet_text', 'tweet_link', 'media_exists']

def scrape(link):
    # replacing twitter link with nitter to make scraping easier
    nitter_link = link.replace("https://twitter.com", "http://nitter.luvvglobal.com", 1) # my public nitter instance
    
    # selenium web driver
    options = webdriver.FirefoxOptions() 
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get(nitter_link)
    
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

def main():
    df = pd.read_csv('emeutes.csv') # replace with csv name!
    links = df['tweets']
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor: # change max_workers as needed
        executor.map(load, links)
    
    df_tweets = pd.DataFrame(tweets, columns=columns)
    df_errors = pd.DataFrame(errors, columns=[['tweets']])
    
    df_tweets.to_csv('csv/emeutes-tweets.csv', index=False) # replace as needed
    df_errors.to_csv('csv/emeutes-errors.csv', index=False)

if __name__ == "__main__":
    main()