# Web-Scraping
It is used to scrape the news from ndtv and provide summary and perform sentiment analysis.
It uses BeautifulSoup4 and flask.Intially we scrape the data from ndtv/latest website and store it in .csv file along with title sentiment using nltk, summary using openai gpt-4o-mini model and the link where the actual news present.
The flask file will collect the data from .csv file and display the title,summary,sentiment and link.
