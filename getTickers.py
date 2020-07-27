import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import string
letters = string.ascii_uppercase
tickers = []
exchanges = ['NYSE', 'NASDAQ']
for ex in exchanges:
    for letter in letters:
        try:
            res = requests.get("http://eoddata.com/stocklist/%s/%s.htm" % (ex,letter))
            soup = BeautifulSoup(res.content,"html.parser")
            table = soup.find_all('table')[5] 
            tickers = tickers + pd.read_html(str(table))[0]['Code'].to_list()
        except:
            pass
print(tickers[:10])
import pickle
from tqdm import tqdm
tickDict = {}
for tick in tqdm(tickers[:10]):

    try:
        ticker = yf.Ticker(tick)
        recommend = ticker.get_recommendations()
        
        market_data = ticker.history(period='5y')
        market_data['delta'] = market_data['Close'].diff()/market_data['Close']
        market_data['spread'] = market_data['High']-market_data['Low']/((market_data['High']+market_data['Low'])/2)
        market_data['norm_vol'] = (market_data['Volume']-market_data['Volume'].min())/(market_data['Volume'].max()-market_data['Volume'].min())
        rec_mat = recommend[['To Grade']].pivot_table(index=recommend.index.date, columns=['To Grade'], aggfunc=len, fill_value=0)
        mrkt_rec = market_data.join(rec_mat).fillna(0)
        tickDict[tick] = mrkt_rec
        
    except:
        pass
        
outfile = open('stock.pkl','wb')
pickle.dump(tickDict,outfile)
outfile.close()