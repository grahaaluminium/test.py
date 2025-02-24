import streamlit as st
import yfinance as yf
import pandas as pd

# Fungsi untuk mengambil data saham dari Yahoo Finance
def get_stock_data(tickers, start_date, end_date):
    # Mengambil data untuk setiap ticker
    data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        # Hanya ambil data Close
        data[ticker] = df[['Close']].reset_index()
    return data

# Daftar ticker saham yang ingin diambil
tickers = [
    'AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'NFLX', 'BA', 'V',
    'WMT', 'DIS', 'INTC', 'NKE', 'IBM', 'PYPL', 'GS', 'KO', 'PEP', 'MCD',
    'CAT', 'AMD', 'SNAP', 'SPY', 'QQQ', 'BABA', 'UBER', 'GM', 'RBLX', 'BA', 'SQ'
]

# Interface Streamlit untuk input tanggal
st.title("Data Saham Yahoo Finance")
start_date = st.date_input("Tanggal Mulai", pd.to_datetime("2020-01-01"))
end_date = st.date_input("Tanggal Akhir", pd.to_datetime("2025-01-01"))

# Ambil data saham dari Yahoo Finance
data = get_stock_data(tickers, start_date, end_date)

# Gabungkan semua data menjadi satu DataFrame
combined_data = pd.concat(data.values(), keys=data.keys(), names=['Ticker', 'Tanggal'])

# Tampilkan tabel dengan data yang telah diurutkan
st.write("Data Saham - Harga Penutupan")
st.dataframe(combined_data.sort_values(by=['Tanggal'], ascending=True))
