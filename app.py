import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
 
# Mengatur tampilan halaman web agar melebar otomatis
st.set_page_config(layout="wide", page_title="Database Promo Matahari")
 
st.title("📊 Portal Data Promosi Matahari")
st.write("Akses publik cepat untuk melihat ratusan ribu data langsung dari cloud database.")
# GANTI STRING DI BAWAH INI DENGAN CONNECTION STRING DARI DASHBOARD SUPABASE ANDA
# Format yang benar biasanya: postgresql://postgres.[ID_PROYEK]:[PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
DB_URI = "postgresql://postgres.pfesinwsletypxslrjhc:Jambi312345@://supabase.com"
 
@st.cache_data(ttl=600)  # Mengunci cache selama 10 menit agar loading data publik sangat cepat
def muat_data():
    engine = create_engine(DB_URI)
    # Menarik data dari tabel Supabase Anda
    query = 'SELECT * FROM "Matahari 312 Promotion";'
    df = pd.read_sql(query, engine)
    return df
 
try:
    data = muat_data()
    
    # Membuat kotak pencarian interaktif untuk publik
    pencarian = st.text_input("🔍 Cari berdasarkan Acara, Departemen, atau Kata Kunci Lain:")
    if pencarian:
        mask = data.astype(str).apply(lambda x: x.str.contains(pencarian, case=False)).any(axis=1)
        data_disaring = data[mask]
    else:
        data_disaring = data
 
    # Menampilkan ringkasan jumlah data
    st.metric(label="Total Data Ditemukan", value=f"{len(data_disaring):,}")
    
    # Menampilkan tabel data utama yang bisa di-scroll dan disortir oleh publik
    st.dataframe(data_disaring, use_container_width=True)
 
except Exception as e:
    st.error(f"Gagal memuat data dari cloud database: {e}")

