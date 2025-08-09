import streamlit as st
import pandas as pd
import pickle

# Load model
with open('model_lr.pkl', 'rb') as f:
    model = pickle.load(f)

# Sidebar untuk navigasi
st.sidebar.title("Menu Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", ["Dashboard", "Prediksi", "Catatan Sablon"])

# --- HALAMAN DASHBOARD ---
if menu == "Dashboard":
    st.title("Dashboard Kualitas Sablon")
    st.markdown("""
    Selamat datang di dashboard deteksi kualitas sablon konveksi.  
    Di sini Anda bisa melihat ringkasan kualitas produksi sablon, catatan penting, dan status terbaru.
    """)
    
    # Contoh ringkasan statis (bisa kamu ganti dengan data asli)
    total_produksi = 1200
    produk_cacat = 45
    produk_bagus = total_produksi - produk_cacat
    persentase_cacat = produk_cacat / total_produksi * 100

    st.metric("Total Produksi Sablon", total_produksi)
    st.metric("Produk Cacat", produk_cacat, delta=f"{persentase_cacat:.2f}% dari total")
    st.metric("Produk Tidak Cacat", produk_bagus)

    # Bisa tambah grafik misal pie chart
    import matplotlib.pyplot as plt

    labels = ['Produk Bagus', 'Produk Cacat']
    sizes = [produk_bagus, produk_cacat]
    colors = ['#4CAF50', '#F44336']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax1.axis('equal')
    st.pyplot(fig1)

# --- HALAMAN PREDIKSI ---
elif menu == "Prediksi":
    st.title("Prediksi Cacat Sablon - Konveksi")
    st.markdown("Masukkan data sablon untuk prediksi apakah produk cacat atau tidak.")

    jenis_kain = st.number_input("Jenis Kain (kode angka)", min_value=0, value=0)
    jenis_sablon = st.number_input("Jenis Sablon (kode angka)", min_value=0, value=0)
    suhu_mesin = st.number_input("Suhu Mesin (°C)", min_value=150.0, max_value=200.0, value=175.0)
    kecepatan_cetak = st.number_input("Kecepatan Cetak (m/s)", min_value=1.0, max_value=5.0, value=3.0)
    operator = st.number_input("Operator (kode angka)", min_value=0, value=0)

    if st.button("Prediksi"):
        input_df = pd.DataFrame({
            'Jenis_Kain': [jenis_kain],
            'Jenis_Sablon': [jenis_sablon],
            'Suhu_Mesin': [suhu_mesin],
            'Kecepatan_Cetak': [kecepatan_cetak],
            'Operator': [operator]
        })

        pred = model.predict(input_df)[0]

        if pred == 1:
            st.error("Produk diprediksi: **Cacat** ❌")
        else:
            st.success("Produk diprediksi: **Tidak Cacat** ✅")

# --- HALAMAN CATATAN SABLON ---
elif menu == "Catatan Sablon":
    st.title("Catatan dan Tips Kualitas Sablon")
    st.markdown("""
    Berikut adalah beberapa tips dan catatan penting untuk menjaga kualitas sablon:  
    - Pastikan suhu mesin stabil antara 170°C - 180°C  
    - Jangan terlalu cepat dalam kecepatan cetak, optimal 2.5 - 3.5 m/s  
    - Pilih jenis kain yang sesuai dengan jenis sablon yang digunakan  
    - Lakukan maintenance rutin pada mesin sablon  
    - Operator harus terlatih untuk menghindari cacat produk  
    """)

    st.markdown("### Contoh Masalah dan Solusi")
    st.write("""
    - **Masalah:** Hasil sablon tidak rata  
      **Solusi:** Periksa tekanan mesin dan kecepatan cetak.  
    - **Masalah:** Warna pudar setelah dicuci  
      **Solusi:** Gunakan tinta sablon yang berkualitas dan suhu pengeringan sesuai standar.  
    - **Masalah:** Cacat sablon muncul setelah proses finishing  
      **Solusi:** Pastikan proses finishing tidak merusak sablon, lakukan kontrol kualitas.  
    """)

