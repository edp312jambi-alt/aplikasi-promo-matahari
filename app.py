import streamlit as st
import pandas as pd
import requests

# Mengatur tampilan halaman web agar melebar otomatis
st.set_page_config(layout="wide", page_title="Database Promo Matahari")
 
st.title("📊 Portal Data Promosi Matahari")
st.write("Akses publik cepat untuk melihat ratusan ribu data langsung dari cloud database baru.")

# PERBAIKAN 1: Mengubah nama tabel dengan encoding spasi URL (%20) yang benar
API_URL = "https://supabase.co"

# PERBAIKAN 2: Gunakan Publishable Key (sb_publishable_...) yang Anda salin secara utuh dan lengkap
API_KEY = "sb_publishable_1cMUgWrzNj9EULAerQDiA_dZdGi" # <-- Pastikan kode panjang Anda tertempel utuh di sini

@st.cache_data(ttl=600)
def muat_data_api():
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}"
    }
    
    respons = requests.get(API_URL, headers=headers)
    
    # PERBAIKAN 3: Jika berhasil (Status 200), langsung parsing JSON
    if respons.status_code == 200:
        return pd.DataFrame(respons.json())
    else:
        # Jika gagal, tampilkan pesan asli dari Supabase agar mudah dilacak
        st.error(f"⚠️ Kode Respons Server: {respons.status_code}")
        st.error(f"💬 Detail Masalah: {respons.text}")
        st.stop()

try:
    data_mentah = muat_data_api()
    
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
