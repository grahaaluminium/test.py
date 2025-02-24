import streamlit as st
import yfinance as yf
import pandas as pd

# Fungsi untuk mengambil data saham dari Yahoo Finance
def get_stock_data(tickers, start_date, end_date):
    data = {}
    # Menyimpan tanggal pertama data tersedia untuk setiap ticker
    ticker_first_dates = {}

    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        # Menyimpan tanggal pertama kali data tersedia untuk ticker
        if not df.empty:
            ticker_first_dates[ticker] = df.index.min()
            # Hanya ambil data Close
            data[ticker] = df[['Close']].reset_index()
    
    return data, ticker_first_dates

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
data, ticker_first_dates = get_stock_data(tickers, start_date, end_date)

# Menyesuaikan start_date berdasarkan tanggal pertama data yang tersedia
adjusted_start_date = max(start_date, min(ticker_first_dates.values()))

# Menampilkan informasi tentang penyesuaian tanggal
st.write(f"Tanggal mulai yang digunakan adalah {adjusted_start_date.strftime('%Y-%m-%d')}")

# Gabungkan semua data menjadi satu DataFrame
combined_data = pd.concat(data.values(), keys=data.keys(), names=['Ticker', 'Tanggal'])

# Tampilkan tabel dengan data yang telah diurutkan
st.write("Data Saham - Harga Penutupan")
st.dataframe(combined_data.loc[combined_data.index.get_level_values('Tanggal') >= adjusted_start_date]
             .sort_values(by=['Tanggal'], ascending=True))
