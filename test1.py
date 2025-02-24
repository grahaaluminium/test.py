import streamlit as st
import yfinance as yf
import pandas as pd

# Judul aplikasi
st.title('Aplikasi Data Saham dari Stooq (via Yahoo Finance)')

# Input untuk kode saham
ticker = st.text_input('Masukkan kode saham (misalnya: AAPL, TSLA, GOOG)', 'AAPL')

# Pilih rentang waktu
start_date = st.date_input('Tanggal Mulai', pd.to_datetime('2020-01-01'))
end_date = st.date_input('Tanggal Selesai', pd.to_datetime('2023-01-01'))

# Tombol untuk menarik data
if st.button('Tarik Data'):
    # Mengambil data saham dari Yahoo Finance (melalui kode saham)
    st.write(f'Tarik data untuk {ticker} dari {start_date} hingga {end_date}...')
    
    # Ambil data
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Menampilkan data dalam bentuk tabel
    st.write('Data Saham:', data)

    # Plot grafik harga saham
    st.line_chart(data['Close'])

# Menyediakan penjelasan tentang aplikasi
st.sidebar.write("""
Aplikasi ini memungkinkan Anda untuk menarik data saham dari Yahoo Finance yang juga mencakup data dari Stooq.
Masukkan kode saham, pilih rentang waktu, dan klik tombol 'Tarik Data' untuk melihat informasi dan grafik harga saham.
""")
