import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Mengatur tampilan halaman web agar melebar otomatis
st.set_page_config(layout="wide", page_title="Database Promo Matahari")
 
st.title("📊 Portal Data Promosi Matahari")
st.write("Akses publik cepat untuk melihat ratusan ribu data langsung dari cloud database.")
 
DB_URI = "postgresql://postgres.pfesinwsletypxslrjhc:Jambi312345@://supabase.com"
 
# Cache dimatikan sementara agar error lama terbuang
def muat_data():
    engine = create_engine(DB_URI)
    query = text('SELECT * FROM "Matahari 312 Promotion";')
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df
 
try:
    # Memuat data segar langsung dari cloud database
    data_mentah = muat_data()
    
    # Konversi seluruh isi kolom menjadi teks biasa demi keamanan tipe data
    data = data_mentah.copy()
    for col in data.columns:
        data[col] = data[col].astype(str).str.strip().replace({"": None, "nan": None, "None": None})
    
    # Kotak pencarian interaktif
    pencarian = st.text_input("🔍 Cari berdasarkan Acara, Departemen, atau Kata Kunci Lain:")
    if pencarian:
        mask = data.astype(str).fillna('').apply(lambda x: x.str.contains(pencarian, case=False)).any(axis=1)
        data_disaring = data[mask]
    else:
        data_disaring = data
 
    # Tampilkan jumlah data dan tabel
    st.metric(label="Total Data Ditemukan", value=f"{len(data_disaring):,}")
    st.dataframe(data_disaring, use_container_width=True)
 
except Exception as e:
    st.error(f"Gagal memuat data dari cloud database: {e}")
