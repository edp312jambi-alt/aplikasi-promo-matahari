import streamlit as st
import pandas as pd
from supabase import create_client, Client

# 1. Mengatur Tampilan Halaman Web
st.set_page_config(layout="wide", page_title="Database Promo Matahari")
 
st.title("📊 Portal Data Promosi Matahari")
st.write("Akses publik cepat untuk melihat ratusan ribu data langsung dari cloud database baru.")

# 2. Konfigurasi Endpoint Proyek Supabase Baru Anda
SUPABASE_URL = "https://smiepesiidolrcztrboq.supabase.co"
SUPABASE_KEY = "smiepesiidolrcztrboq"  # <-- Ganti dengan anon key baru Anda

# 3. Fungsi Pengambil Data Otomatis (Pagination)
@st.cache_data(ttl=600)
def muat_data_dari_supabase():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    semua_data = []
    baris_mulai = 0
    ukuran_halaman = 1000  
    
    with st.spinner("Sedang menarik data dari cloud database baru..."):
        while True:
            respons = supabase.table("Matahari 312 Promotion") \
                              .select("ACARA, FORM DATE, TO DATE, DEPT, WORLD") \
                              .range(baris_mulai, baris_mulai + ukuran_halaman - 1) \
                              .execute()
            
            data_halaman = respons.data
            if not data_halaman:
                break
                
            semua_data.extend(data_halaman)
            baris_mulai += ukuran_halaman
            
            # Pengaman memori (Dapat dinaikkan sesuai kebutuhan)
            if len(semua_data) >= 50000:  
                break

    df = pd.DataFrame(semua_data)
    return df

# 4. Tampilan Menu dan Fitur Pencarian
try:
    data_mentah = muat_data_dari_supabase()
    data = data_mentah.fillna('').astype(str)
    
    pencarian = st.text_input("🔍 Cari berdasarkan Acara, Departemen, atau Kata Kunci Lain:")
    if pencarian:
        mask = data.apply(lambda x: x.str.contains(pencarian, case=False)).any(axis=1)
        data_disaring = data[mask]
    else:
        data_disaring = data
 
    st.metric(label="Total Data Ditemukan", value=f"{len(data_disaring):,}")
    st.dataframe(data_disaring, use_container_width=True)
 
except Exception as e:
    st.error(f"Gagal memuat data dari cloud database baru: {e}")
