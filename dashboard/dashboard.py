import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Mengatur gaya Seaborn
sns.set(style='dark')

# Fungsi untuk memuat dan mempersiapkan data
def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['month'] = df['dteday'].dt.month
    df['season'] = df['month'].map({
        1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring',
        5: 'Spring', 6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall', 12: 'Winter'
    })
    return df

# Fungsi untuk menghitung total penyewaan per bulan dan per musim
def calculate_rentals(df):
    monthly_rentals = df.groupby('month')['cnt'].sum()
    seasonal_rentals = df.groupby('season')['cnt'].sum()
    return monthly_rentals, seasonal_rentals

# Fungsi untuk menghitung total pengunjung harian dan per jam
def calculate_total_visitors(df):
    day_df = df.groupby('dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    }).reset_index()
    
    total_visitor_day = day_df["casual"].sum() + day_df["registered"].sum()
    
    return total_visitor_day, day_df

# Fungsi untuk analisis penyewaan berdasarkan suhu
def analyze_rentals_by_temp(df):
    hour_analysis = df.groupby('temp')['cnt'].agg(['mean', 'sum']).reset_index()
    hour_analysis.columns = ['temp', 'Average Rentals', 'Total Rentals']
    return hour_analysis

# Fungsi untuk visualisasi hubungan antara suhu dan jumlah penyewaan
def plot_temp_vs_rentals(all_df):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(x='temp', y='cnt', data=all_df, alpha=0.6)
    plt.title('Hubungan antara Suhu dan Jumlah Sewa Sepeda')
    plt.xlabel('Suhu (temp)')
    plt.ylabel('Jumlah Sewa Sepeda (cnt)')
    plt.grid()
    return fig

# Fungsi untuk visualisasi hubungan antara musim dan jumlah penyewaan
def plot_seasonal_rentals(all_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='season', y='cnt', data=all_df)
    plt.title('Box Plot Jumlah Sewa Sepeda Berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Sewa Sepeda (cnt)')
    plt.grid()
    return fig

# Fungsi untuk visualisasi tren penyewaan sepanjang tahun
def plot_yearly_trend(all_df, monthly_rentals):
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(all_df['dteday'], all_df['cnt'], label='Jumlah Penyewaan', color='blue')
    plt.title('Tren Penyewaan Sepeda Selama Setahun')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penyewaan')
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()

    plt.subplot(1, 2, 2)
    monthly_rentals.plot(kind='bar', color='lightgreen')
    plt.title('Jumlah Penyewaan Sepeda per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')
    plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    plt.grid(axis='y')
    
    plt.tight_layout()
    return fig

# Load cleaned data
all_df = load_and_prepare_data("all_data.csv")

# Menentukan nilai minimum dan maksimum tanggal
min_date = all_df['dteday'].min()
max_date = all_df['dteday'].max()

# Sidebar untuk input tanggal
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Menyaring DataFrame berdasarkan rentang tanggal
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                  (all_df["dteday"] <= str(end_date))]

# Menghitung total penyewaan dan pengunjung untuk data yang telah disaring
monthly_rentals, seasonal_rentals = calculate_rentals(main_df)
total_visitor_day, day_df = calculate_total_visitors(main_df)

# Analisis penyewaan berdasarkan suhu
hour_analysis = analyze_rentals_by_temp(main_df)  # Menggunakan main_df yang telah disaring

# Streamlit Dashboard
st.header('Analisis Penyewaan Sepeda :sparkles:')
st.subheader('Total Pengunjung')

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Pengunjung Harian", value=total_visitor_day)

# Visualisasi hubungan antara suhu dan jumlah penyewaan
st.subheader('Hubungan antara Suhu dan Jumlah Sewa Sepeda')
st.pyplot(plot_temp_vs_rentals(main_df))

# Visualisasi hubungan antara musim dan jumlah penyewaan
st.subheader('Jumlah Sewa Sepeda Berdasarkan Musim')
st.pyplot(plot_seasonal_rentals(main_df))

# Visualisasi tren penyewaan sepanjang tahun
st.subheader('Tren Penyewaan Sepeda Selama Setahun')
st.pyplot(plot_yearly_trend(main_df, monthly_rentals))

st.caption('Copyright © Dicoding 2024')