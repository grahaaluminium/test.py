import streamlit as st
import yfinance as yf
import pandas as pd

#add data stock
portfolioTicker = []
portfolioData = []
while len(portfolioTicker) < 30:
  st.write("Portfolio anda masih kurang",30-len(portfolioTicker),"ticker. Mohon isi ticker pilihan anda")
  tickerSelect = list(map(str, input().split(",")))
  for i in range(30-len(portfolioTicker)):
    tickerSelect_data = yf.Ticker(tickerSelect[i]).history(period="max")#INI BISA PAKAI SUMBER DATA MANAPUN TIDAK HARUS YFINANCE
    tickerSelect_data.index = pd.to_datetime(tickerSelect_data.index).date
    if len(tickerSelect_data) > 1000:
      portfolioTicker.append(tickerSelect[i])
      portfolioData.append(tickerSelect_data)

#cleaning and rekonstruk test data
testStartdate = dt.datetime(1900, 1, 1).date()
testEnddate = dt.datetime.now().date()
for i in range(len(portfolioData)):
   testStartdate = max(testStartdate,portfolioData[i].index.min())
   testEnddate = min(testEnddate,portfolioData[i].index.max())

for i in range(len(portfolioData)):
   while not testStartdate in portfolioData[i].index:#INI DI UJI LAGI, CODING INI SDH BENER ATAU TDK
    testStartdate += datetime.timedelta(days=1)

testDate = testStartdate
date = []
data = []
while testDate < testEnddate:
  data_array = []
  for i in range(len(portfolioData)):
    if testDate in portfolioData[i].index:#INI DI CEK DAN PASTIKAN LAGI
      data_array.append(portfolioData[i]["Close"].loc[testDate])
    else:
      data_array.append(data[len(data)-1][i])
  date.append(testDate)
  data.append(data_array)

  testDate += datetime.timedelta(days=1)

test_data = pd.DataFrame(data,index=date)
dataHarga = test_data.to_numpy()
tanggal = test_data.index.to_numpy()
st.write("Your Portfolio Ticker:",portfolioTicker)
st.write("Your Portfolio Data:\n",test_data)
