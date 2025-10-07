import yfinance as yf
import pandas as pd
import plotly.express as px
import numpy as np

tickersdict = {
    "AAPL": 82,
    "ADBE": 48,
    "ADP": 148,
    "ALL": 30,
    "AMZN": 200,
    "BRK-B": 108,
    "CAT": 99,
    "COST": 67,
    "CRH": 250,
    "DG": 161,
    "DHR": 165,
    "DIS": 20,
    "GOOG": 292,
    "HD": 70,
    "HON": 114,
    "JNJ": 134,
    "LMT": 35,
    "MA": 98,
    "MSFT": 112,
    "NEE": 322,
    "NKE": 89,
    "ON": 200,
    "SNOW": 145,
    "SPY": 537,
    "STLA": 1000,
    "TTWO": 65,
    "VLTO": 55,
    "WMT": 558,
    "WEAV": 1079
}


# Download the ticker prices and save them into the 'prices' list
# Find a way to make this more efficient, grab all the prices at once? 
# Also remove the progress log from the ouput (***100%***)
prices = []
for ticker in tickersdict:
    data = yf.download(ticker, period='1d', auto_adjust=False)
    last_close = data["Close"].iloc[-1].round(2).item() #Grabs the item on the last row of the Close column, rounds it to 2 decimal places
    prices.append(last_close)
# print(prices)


# Establishing the column order based on tickersdict, sanity checking lengths
cols = list(tickersdict.keys())
assert len(prices) == len(cols)


# Making a series for closing prices and shares owned
price_s = pd.Series(prices, index=cols, name="Closing Price")
shares_s = pd.Series(tickersdict, name="Shares Owned").reindex(cols).astype(int)


# Computing the total value (closing price * shares owned)
total_s = price_s.mul(shares_s).round(2)
total_s.name = "Total Value"


# Assembling the final DataFrame
final_df = pd.concat([price_s, shares_s, total_s], axis=1).reset_index()
final_df = final_df.rename(columns={"index": "Ticker"})

#print(final_df)

# Ensuring correct dtypes, eliminating potential factors causing hoverdata bug
final_df["Closing Price"] = final_df["Closing Price"].astype(float)
final_df["Shares Owned"] = final_df["Shares Owned"].astype(int)


pf_donut_chart = px.pie(
    final_df,
    names = "Ticker",
    values = "Total Value",
    custom_data=['Closing Price', 'Shares Owned'],
    hole = 0.5,
)

pf_donut_chart.update_traces(
    textinfo = 'label+percent',
    hovertemplate= (
        "<b>%{label}</b><br>"
        "Total Value: %{value}<br>" #fix formatting later to show trailing 0 for cents
        "Closing Price: %{customdata[0][0]:,.2f}<br>" #double indexing because PX wraps trace data inside a list
        "Shares Owned: %{customdata[0][1]:,d}<br>"
        "<extra></extra>"
    )
)

pf_donut_chart.update_layout(autosize=False, width=900, height=900, showlegend=False)
pf_donut_chart.show()

#print(pf_donut_chart.data[0].customdata[:5])




































# from datetime import datetime, timedelta

# tickers = ['AAPL', 'ADBE' ,'ADP', 'ALL', 'AMZN', 'BRK-B', 'CAT', 'COST', 'CRH', 'DG', 'DHR', 'DIS', 'GOOG', 'HD', 'HON', 'JNJ', 'LMT', 'MA', 'MSFT', 'NEE', 'NKE', 'ON', 'SNOW', 'SPY', 'STLA', 'TTWO', 'VLTO', 'WMT', 'WEAV']


# close_price = pd.Series(prices, index=tickersdict.keys())

    # print("Start of Last Close")
    # print(last_close)
    # print("End of Last Close")


    # print("Start of Data")
    # print(data)
    # print("End of Data")




# Setting start and end points for historical prices:
# end_date = datetime.today()
# print(end_date)

# start_date = end_date - timedelta(days = 365)
# print(start_date)



# close_df = pd.DataFrame(index=row_names)
# for ticker in tickersdict:
#     data = yf.download(ticker, period='1d', auto_adjust=False)
#     close_df[ticker] = data["Close"].round(2)
