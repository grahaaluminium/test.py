import streamlit as st
import pandas as pd
import datetime as dt
import random
import urllib.request
import urllib.error

# Judul aplikasi
st.title("CREATE TEST DATA")

# Load data
data_stooq_ticker = pd.read_csv('https://raw.githubusercontent.com/guangyoung/dataStock/refs/heads/main/stooq_tickers.csv')
data_yfinance_ticker = pd.read_csv('https://raw.githubusercontent.com/guangyoung/dataStock/refs/heads/main/stooq_tickers.csv')

# Dropdown untuk memilih sumber data
data_source = st.selectbox("Data Source:", options=['stooq', 'yahooFinance', 'local'], index=0)

# Dropdown untuk memilih exchange
if data_source == 'stooq':
    exchange_options = data_stooq_ticker.columns.tolist()
elif data_source == 'yahooFinance':
    exchange_options = data_yfinance_ticker.columns.tolist()
else:
    exchange_options = []

exchange = st.selectbox("Exchange:", options=exchange_options, index=0 if exchange_options else None)

# Dropdown untuk memilih tahun mulai
start_year = st.selectbox("Start Year:", options=[str(year) for year in range(1991, 2015)], index=0)

# Dropdown untuk memilih mode seleksi
select_mode = st.selectbox("Select Mode:", options=['Manual Select', 'Random Select'], index=0)

# Dropdown untuk memilih saham
if data_source in ['stooq', 'yahooFinance']:
    ticker_data = data_stooq_ticker if data_source == 'stooq' else data_yfinance_ticker
    saham_options = [stock for stock in ticker_data[exchange].dropna().tolist() if dt.datetime.strptime(stock.split(',')[1], '%Y%m%d').year < int(start_year)]
else:
    saham_options = []

saham = st.multiselect("Select Stock:", options=saham_options)
st.write(saham)
st.write(len(saham))

# Tombol untuk menambahkan ke portofolio
if st.button("Add to Portfolio"):
    if len(saham) < 5:
        st.warning(f"Portfolio anda masih kurang {30 - len(saham)} ticker. Mohon isi ticker dengan total sejumlah 30.")
    else:
        portfolio_data, portfolio_ticker = [], []
        if data_source == 'stooq':
            st.write("masuk stooq")
            for ticker in saham:
                st.write(ticker)
                ticker_split = ticker.split(',')[0]
                st.write(ticker_split)
                ticker_data = pd.read_csv(f'https://stooq.com/q/d/l/?s={'aa.us'}&i=d')
                st.write("berhasil tarik data")
                st.write(ticker_data)
                if len(ticker_data) > 100 and ticker not in portfolio_ticker:
                    ticker_data.set_index(pd.to_datetime(ticker_data['Date']), inplace=True)
                    portfolio_data.append(ticker_data['Close'])
                    portfolio_ticker.append(ticker)
                    st.write(ticker_data)
                else:
                    st.write(ticker)
        elif data_source == 'local':
            uploaded_files = st.file_uploader("Upload File From Local Computer:", type=['csv'], accept_multiple_files=True)
            for uploaded_file in uploaded_files:
                ticker_data = pd.read_csv(uploaded_file)
                ticker_data.set_index(pd.to_datetime(ticker_data['Date']), inplace=True)
                ticker = uploaded_file.name.rsplit('.', 1)[0]
                if len(ticker_data) > 0 and ticker not in portfolio_ticker:
                    portfolio_data.append(ticker_data['Close'])
                    portfolio_ticker.append(ticker)
        st.write(portfolio_data)
        if len(portfolio_data) >= 5:
            test_start_date = max([data.index.min() for data in portfolio_data])
            st.write(test_start_date)
            test_end_date = min([data.index.max() for data in portfolio_data])
            st.write(test_end_date)
            date_range = pd.date_range(test_start_date, test_end_date)
            date_range = date_range[~date_range.weekday.isin([5, 6])]
            test_data = pd.DataFrame([
                [data.loc[test_date] if test_date in data.index else data.loc[:test_date].iloc[-1] for data in portfolio_data]
                for test_date in date_range
            ], index=date_range.date)
            st.write(test_data)
