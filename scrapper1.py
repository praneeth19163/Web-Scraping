import requests
import pandas as pd
from bs4 import BeautifulSoup
import schedule
import time
import openai
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

import os
from openai import OpenAI
os.environ['OPENAI_API_KEY']="your api key(for security reasons i have removed)"
os.getenv('OPENAI_API_KEY')

URL = "https://www.ndtv.com/latest"

def get_sentiment(text):
    score = sia.polarity_scores(text)["compound"]
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

def summarize_text(text):
    try:
        client=OpenAI()
        response=client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Summarize the given news article."},
                      {"role": "user", "content": text}],
            max_tokens=200
        )
        print("summary is .........")
        return response.choices[0].message.content 
    except Exception as e:
        print(f"Error in summarization: {e}")
        return "Summarization failed."

def get_article_content(article_url):
    try:
        response = requests.get(article_url)
        if response.status_code != 200:
            return "Failed to fetch article."

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.get_text() for p in paragraphs])

        return article_text if article_text else "No content found."
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return "Error fetching content."

def scrape_news():
    print("\nStarting Scraping...")
    
    try:
        response = requests.get(URL)
        print(f"Response Status Code: {response.status_code}")

        if response.status_code != 200:
            print("Failed to fetch the website. Exiting scraping...")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("h2", class_="NwsLstPg_ttl")

        news_list = []
        for article in articles:
            link_tag = article.find("a")
            
            if link_tag:
                title = link_tag.text.strip()
                link = link_tag["href"]
                full_text = get_article_content(link)
                print("summary is done...........")
                summary = summarize_text(full_text)
                sentiment = get_sentiment(title)
                
                news_list.append({
                    "Title": title,
                    "Link": link,
                    "Summary": summary,
                    "Sentiment": sentiment
                })

        if not news_list:
            print("No news articles found. Check the website structure.")
            return
        
        df = pd.DataFrame(news_list)
        df.to_csv("news_summarized.csv", index=False)

        print(f"Scraped and summarized {len(news_list)} articles. Saved to news_summarized.csv")

    except Exception as e:
        print(f"Error during scraping: {e}")

scrape_news()

schedule.every(30).minutes.do(scrape_news)

print("Scheduler started. Scraping every 30 minutes...")
while True:
    schedule.run_pending()
    time.sleep(1)
