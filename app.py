import streamlit as st
import pandas as pd
import requests

# Mengatur tampilan halaman web agar melebar otomatis
st.set_page_config(layout="wide", page_title="Database Promo Matahari")
 
st.title("📊 Portal Data Promosi Matahari")
st.write("Akses publik cepat untuk melihat ratusan ribu data langsung dari cloud database baru.")

# Menggunakan endpoint REST API REST Supabase
API_URL = "https://supabase.co"

# Pastikan untuk menempelkan Publishable Key asli Anda yang sangat panjang di sini
API_KEY = "sb_publishable_1cMUgWrzNj9EULAerQDiA_dZdGi" 

# NAMA FUNGSI DIUBAH MENJADI 'ambil_data_terbaru' UNTUK MEMAKSA CACHE TERBUANG
@st.cache_data(ttl=600)
def ambil_data_terbaru():
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Menambahkan parameter select=* secara eksplisit agar Supabase memberikan response data yang valid
    params = {"select": "*"}
    
    respons = requests.get(API_URL, headers=headers, params=params)
    
    if respons.status_code == 200:
        return pd.DataFrame(respons.json())
    else:
        st.error(f"⚠️ Kode HTTP Server: {respons.status_code}")
        st.error(f"💬 Detail Masalah: {respons.text}")
        st.stop()

try:
    # Memanggil fungsi baru pembongkar cache
    data_mentah = ambil_data_terbaru()
    
    if not data_mentah.empty:
        if 'id' in data_mentah.columns:
            data_mentah = data_mentah.drop(columns=['id'])
            
        data = data_mentah.fillna('').astype(str)
        
        pencarian = st.text_input("🔍 Cari berdasarkan Acara, Departemen, atau Kata Kunci Lain:")
        if pencarian:
            mask = data.apply(lambda x: x.str.contains(pencarian, case=False)).any(axis=1)
            data_disaring = data[mask]
        else:
            data_disaring = data
     
        st.metric(label="Total Data Ditemukan", value=f"{len(data_disaring):,}")
        st.dataframe(data_disaring, use_container_width=True)
    else:
        st.warning("Tabel database kosong atau tidak memiliki baris data.")
 
except Exception as e:
    st.error(f"Gagal memuat data dari cloud database baru: {e}")
