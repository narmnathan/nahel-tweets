import pandas as pd
from deep_translator import GoogleTranslator
import concurrent.futures
import time

translator = GoogleTranslator(source='auto', target='english')
tweets = []

def translate_tweet(str):
    time.sleep(1)
    print('Translating: ' + str)
    translated = translator.translate(text=str)
    tweets.append(translated)

def main():
    df = pd.read_csv('tweet_text.csv')
    tweets = df['tweet_text']
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor: # setting to five workers since api request maxes out at 5
        executor.map(translate_tweet, tweets)
        
    df_translated = pd.DataFrame(tweets, columns=[['translated']])
    
    df_translated.to_csv('translated.csv', index=False)
    
if __name__ == "__main__":
    main()