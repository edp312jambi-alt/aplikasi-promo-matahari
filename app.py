import streamlit as st
import pandas as pd
import requests

# Mengatur tampilan halaman web agar melebar otomatis
st.set_page_config(layout="wide", page_title="Database Promo Matahari")
 
st.title("📊 Portal Data Promosi Matahari")
st.write("Akses publik cepat untuk melihat ratusan ribu data langsung dari cloud database baru.")

# Menggunakan endpoint REST API REST Supabase (Lebih aman dari error driver database)
API_URL = "https://supabase.co"

# PENTING: Gunakan Publishable Key (sb_publishable_...) yang Anda salin dari dashboard sebelumnya
API_KEY = "sb_publishable_1cMUgWrzNj9EULAerQDiA_dZdGi" # <-- Pastikan teks ini sesuai dengan key Anda

@st.cache_data(ttl=600)  # Mengunci cache selama 10 menit
def muat_data_api():
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Meminta data mentah format JSON langsung lewat jaringan HTTP web
    respons = requests.get(API_URL, headers=headers)
    
    if respons.status_code == 200:
        json_data = respons.json()
        df = pd.DataFrame(json_data)
        
        # Buang kolom 'id' bawaan jika ada agar tidak mengganggu tampilan
        if 'id' in df.columns:
            df = df.drop(columns=['id'])
            
        return df
    else:
        raise Exception(f"Error API Supabase: {respons.status_code} - {respons.text}")

try:
    # Memuat data murni tanpa melibatkan engine SQL sama sekali
    data_mentah = muat_data_api()
    data = data_mentah.fillna('').astype(str)
    
    # Membuat kotak pencarian interaktif untuk publik
    pencarian = st.text_input("🔍 Cari berdasarkan Acara, Departemen, atau Kata Kunci Lain:")
    if pencarian:
        mask = data.apply(lambda x: x.str.contains(pencarian, case=False)).any(axis=1)
        data_disaring = data[mask]
    else:
        data_disaring = data
 
    # Menampilkan ringkasan jumlah data
    st.metric(label="Total Data Ditemukan", value=f"{len(data_disaring):,}")
    
    # Menampilkan tabel data utama
    st.dataframe(data_disaring, use_container_width=True)
 
except Exception as e:
    st.error(f"Gagal memuat data dari cloud database baru: {e}")
