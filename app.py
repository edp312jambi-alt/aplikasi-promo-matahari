import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Mengatur tampilan halaman web agar melebar otomatis
st.set_page_config(layout="wide", page_title="Database Promo Matahari")
 
st.title("📊 Portal Data Promosi Matahari")
st.write("Akses publik cepat untuk melihat ratusan ribu data langsung dari cloud database baru.")
 
# KONEKSI MENGGUNAKAN HOST PROYEK SUPABASE BARU ANDA (Aman & Stabil)
DB_URI = "postgresql://postgres.smiepesiidolrcztrboq:Jambi312345@://supabase.com"
 
@st.cache_data(ttl=600)  # Mengunci cache selama 10 menit
def muat_data():
    engine = create_engine(DB_URI)
    query = text('SELECT * FROM "Matahari 312 Promotion";')
    with engine.connect() as conn:
        # Memaksa semua kolom dibaca sebagai text/string untuk mencegah error angka/int()
        df = pd.read_sql(query, conn, dtype=str)
    return df
 
try:
    # Memuat data aman
    data = muat_data()
    data = data.fillna('')
    
    # Membuat kotak pencarian interaktif untuk publik
    pencarian = st.text_input("🔍 Cari berdasarkan Acara, Departemen, atau Kata Kunci Lain:")
    if pencarian:
        mask = data.astype(str).apply(lambda x: x.str.contains(pencarian, case=False)).any(axis=1)
        data_disaring = data[mask]
    else:
        data_disaring = data
 
    # Menampilkan ringkasan jumlah data
    st.metric(label="Total Data Ditemukan", value=f"{len(data_disaring):,}")
    
    # Menampilkan tabel data utama
    st.dataframe(data_disaring, use_container_width=True)
 
except Exception as e:
    st.error(f"Gagal memuat data dari cloud database baru: {e}")
