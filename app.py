import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Mengatur tampilan halaman web agar melebar otomatis
st.set_page_config(layout="wide", page_title="Database Promo Matahari")
 
st.title("📊 Portal Data Promosi Matahari")
st.write("Akses publik cepat untuk melihat ratusan ribu data langsung dari cloud database.")
 
DB_URI = "postgresql://postgres.pfesinwsletypxslrjhc:Jambi312345@://supabase.com"
 
@st.cache_data(ttl=600)  # Mengunci cache selama 10 menit
def muat_data():
    engine = create_engine(DB_URI)
    
    # PERBAIKAN: Membaca data menggunakan object text() dari SQLAlchemy
    query = text('SELECT * FROM "Matahari 312 Promotion";')
    
    # Menggunakan connection context manager agar pengambilan data lebih stabil
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df
 
try:
    # Memuat data asli dari database
    data_mentah = muat_data()
    
    # PERBAIKAN TOTAL: Bersihkan semua string kosong ("") atau spasi di dataframe menjadi None/NaN
    data = data_mentah.copy()
    for col in data.columns:
        if data[col].dtype == 'object':
            data[col] = data[col].astype(str).str.strip().replace({"": None, "nan": None, "None": None})
    
    # Membuat kotak pencarian interaktif untuk publik
    pencarian = st.text_input("🔍 Cari berdasarkan Acara, Departemen, atau Kata Kunci Lain:")
    if pencarian:
        # Memastikan pencarian aman dari data kosong
        mask = data.astype(str).fillna('').apply(lambda x: x.str.contains(pencarian, case=False)).any(axis=1)
        data_disaring = data[mask]
    else:
        data_disaring = data
 
    # Menampilkan ringkasan jumlah data
    st.metric(label="Total Data Ditemukan", value=f"{len(data_disaring):,}")
    
    # Menampilkan tabel data utama yang bisa di-scroll dan disortir oleh publik
    st.dataframe(data_disaring, use_container_width=True)
 
except Exception as e:
    st.error(f"Gagal memuat data dari cloud database: {e}")
