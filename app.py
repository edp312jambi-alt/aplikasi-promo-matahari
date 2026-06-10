import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Mengatur tampilan halaman web agar melebar otomatis
st.set_page_config(layout="wide", page_title="Database Promo Matahari")
 
st.title("📊 Portal Data Promosi Matahari")
st.write("Akses publik cepat untuk melihat ratusan ribu data langsung dari cloud database baru.")
 
DB_URI = "postgresql://postgres.smiepesiidolrcztrboq:Matahari3123450@://supabase.com"
 
@st.cache_data(ttl=600)  # Mengunci cache selama 10 menit
def muat_data():
    engine = create_engine(DB_URI)
    query = text('SELECT "ACARA", "FORM DATE", "TO DATE", "DEPT", "WORLD" FROM "Matahari 312 Promotion";')
    
    with engine.connect() as conn:
        # Eksekusi kueri secara manual tanpa melibatkan automap dari Pandas
        result = conn.execute(query)
        
        # Iterasi manual baris demi baris dan memaksa semua nilai diubah menjadi text/string biasa
        baris_bersih = []
        for row in result:
            baris_bersih.append([str(item).strip() if item is not None else "" for item in row])
            
        # Bentuk tabel DataFrame secara manual menggunakan data mentah string
        kolom = ["ACARA", "FORM DATE", "TO DATE", "DEPT", "WORLD"]
        df = pd.DataFrame(baris_bersih, columns=kolom)
    return df
 
try:
    # Memuat data yang sudah bersih total dari tipe data numerik
    data = muat_data()
    
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
