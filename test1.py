import requests
import pandas as pd
import io
import streamlit as st

ticker_split = 'AAPL'  # Replace with the ticker from user input

try:
    url = f'https://stooq.com/q/d/l/?s={ticker_split}&i=d'
    response = requests.get(url)
    response.raise_for_status()  # Check if request was successful
    
    # Check if the response contains CSV data
    if response.headers['Content-Type'] == 'text/csv':
        ticker_data = pd.read_csv(io.StringIO(response.text))
        st.write(ticker_data)
    else:
        st.error(f"Unexpected content type: {response.headers['Content-Type']}")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")
