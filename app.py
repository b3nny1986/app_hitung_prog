import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi format ke Rupiah
def format_rupiah(angka):
    return "Rp. {:,}".format(int(angka)).replace(",", ".")

# Data bobot kendaraan
bobot_kendaraan = {
    "Sedan": 1.025,
    "Jeep": 1.05,
    "Minibus": 1.05,
    "Mikrobus": 1.085,
    "Pickup": 1.085,
    "Truck": 1.3,
    "Sepeda Motor": 1
}

# Judul Aplikasi
st.title("🚗 Aplikasi Penghitung Pajak Kendaraan Bermotor (PKB) Progresif")
st.markdown("Hitung PKB progresif berdasarkan **NJKB** dan **Jenis Kendaraan**")

# Input user
njkb = st.number_input("Masukkan Nilai Jual Kendaraan Bermotor (NJKB):", min_value=0, step=1000000)
jenis = st.selectbox("Pilih Jenis Kendaraan:", list(bobot_kendaraan.keys()))

# Tombol hitung
if st.button("Hitung PKB"):
    bobot = bobot_kendaraan[jenis]
    pkb_list = {}

    # Hitung PKB progresif untuk kepemilikan 1-5
    for i, persen in enumerate([0.008, 0.009, 0.010, 0.011, 0.012], start=1):
        pkb = (njkb * bobot * persen) + (0.66 * (njkb * bobot * persen))
        pkb_list[f"Milik ke-{i}"] = pkb

    # Buat DataFrame untuk ditampilkan (dengan format Rupiah)
    df_pkb = pd.DataFrame(
        [(kepemilikan, format_rupiah(pkb)) for kepemilikan, pkb in pkb_list.items()],
        columns=["Kepemilikan", "PKB"]
    )

    # Hitung selisih PKB Milik 1 dengan lainnya
    selisih = {}
    for i in range(2, 6):
        diff = pkb_list[f"Milik ke-{i}"] - pkb_list["Milik ke-1"]
        selisih[f"Selisih Milik 1 - Milik {i}"] = diff

    df_selisih = pd.DataFrame(
        [(k, format_rupiah(v)) for k, v in selisih.items()],
        columns=["Perbandingan", "Selisih"]
    )

    # Tampilkan hasil
    st.subheader("📊 Hasil Perhitungan PKB Progresif")
    st.table(df_pkb)

    st.subheader("🔍 Selisih PKB Progresif")
    st.table(df_selisih)

    # Visualisasi grafik
    st.subheader("📈 Visualisasi PKB Progresif")
    fig, ax = plt.subplots()
    ax.bar(df_pkb["Kepemilikan"], [pkb for pkb in pkb_list.values()], color="skyblue", edgecolor="black")
    ax.set_ylabel("PKB (Rp)")
    ax.set_title("Grafik PKB Progresif")
    st.pyplot(fig)
