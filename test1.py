import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Judul aplikasi Streamlit
st.title("Aplikasi Tarik Data Saham dari Stooq")

# Input simbol saham (misalnya: AAPL, TSLA)
symbol = st.text_input("Masukkan simbol saham (misal: AAPL, TSLA)", "AAPL")

# Pilihan rentang tanggal
start_date = st.date_input("Tanggal Mulai", pd.to_datetime("2020-01-01"))
end_date = st.date_input("Tanggal Selesai", pd.to_datetime("2025-01-01"))

# Mengkonversi tanggal ke format yang dibutuhkan oleh Stooq (yyyy-mm-dd)
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

# URL API Stooq untuk mengunduh data saham dalam format CSV
url = f"https://stooq.com/q/d/l/?s={symbol}&d1={start_str.replace('-', '')}&d2={end_str.replace('-', '')}&c=1"

# Tombol untuk menarik data
if st.button("Tarik Data Saham"):
    try:
        # Mengambil data CSV dari Stooq
        response = requests.get(url)

        if response.status_code == 200:
        st.write(StringIO(response.text))    
            # Membaca data CSV ke dalam DataFrame
            data = pd.read_csv(StringIO(response.text))
            st.write(data)
            data['Date'] = pd.to_datetime(data['Date'])

            # Menampilkan data dalam bentuk tabel
            st.write(f"Data saham {symbol} dari {start_date} hingga {end_date}:")
            st.dataframe(data)

            # Menampilkan grafik harga saham
            st.line_chart(data.set_index('Date')['Close'])
        else:
            st.error("Gagal mengambil data dari Stooq, pastikan simbol saham benar.")
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
