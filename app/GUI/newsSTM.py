import yfinance as yf
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def calc_sentiment_score(text):
    return analyser.polarity_scores(text)['compound']

def get_sentiments(stock):
    stock = yf.Ticker(stock)
    news = stock.news
    v = [x['title'] for x in news]
    r = [calc_sentiment_score(i['title']) for i in news]
    score = list(zip(r, v))

    return score

def picked_headlines(stocks, target_score=0.4):
    stocks = stocks.split(' ')
    e = []
    for stock in stocks:
        try:
            news = [s for s in get_sentiments(stock) ]
            for i in news:
                e.append(i)
        except:
            continue
    p = [title for score, title in e if score >= target_score]

    return p

if __name__ == "__main__":
    # for i in picked_headlines("AAPL AMZN GOOGL"):
    #     print(i)
    print(get_sentiments("AAPL"))