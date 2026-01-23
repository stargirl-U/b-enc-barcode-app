import streamlit as st
import pandas as pd

from benc_cipher import encrypt_benc, decrypt_benc
from barcode_utils import draw_barcode
from theory import show_theory

KEY = "101011"

st.set_page_config(page_title="B-ENC Cipher", layout="wide")

menu = st.sidebar.selectbox(
    "Navigasi",
    ["Home", "Teori Kriptografi", "Enkripsi", "Dekripsi", "Visualisasi Barcode", "About"]
)

# ---------------- HOME ----------------
if menu == "Home":
    st.title("🔐 B-ENC : Barcode-Based Encryption Cipher")
    st.write("""
    Website edukasi kriptografi yang mendemonstrasikan proses
    enkripsi dan dekripsi menggunakan **pola barcode biner**.
    """)
    st.info("Website ini bersifat edukatif dan tidak ditujukan untuk keamanan data nyata.")

# ---------------- TEORI ----------------
elif menu == "Teori Kriptografi":
    show_theory()

# ---------------- ENKRIPSI ----------------
elif menu == "Enkripsi":
    st.header("🔐 Enkripsi B-ENC")

    plaintext = st.text_input("Masukkan Plaintext")
    st.text(f"Kunci Barcode (Fixed): {KEY}")

    if st.button("Enkripsi"):
        cipher, table = encrypt_benc(plaintext)

        st.success("Ciphertext berhasil dibuat")
        st.write("**Ciphertext:**", cipher)

        st.subheader("Tabel Proses Enkripsi")
        st.dataframe(pd.DataFrame(table))

        st.subheader("Visualisasi Barcode Kunci")
        fig = draw_barcode(KEY)
        st.pyplot(fig)

# ---------------- DEKRIPSI ----------------
elif menu == "Dekripsi":
    st.header("🔓 Dekripsi B-ENC")

    cipher_input = st.text_input("Masukkan Ciphertext (pisahkan dengan koma, contoh: 11,12,5)")
    st.text(f"Kunci Barcode (Fixed): {KEY}")

    if st.button("Dekripsi"):
        try:
            cipher_nums = [int(x.strip()) for x in cipher_input.split(",")]
            plaintext, table = decrypt_benc(cipher_nums)

            st.success("Plaintext berhasil dikembalikan")
            st.write("**Plaintext:**", plaintext)

            st.subheader("Tabel Proses Dekripsi")
            st.dataframe(pd.DataFrame(table))
        except:
            st.error("Format ciphertext salah!")

# ---------------- BARCODE ----------------
elif menu == "Visualisasi Barcode":
    st.header("🧾 Visualisasi Barcode Kunci")

    st.markdown("""
    **Hitam = 1**  
    **Putih = 0**
    """)

    fig = draw_barcode(KEY)
    st.pyplot(fig)

# ---------------- ABOUT ----------------
elif menu == "About":
    st.header("ℹ️ Tentang B-ENC")
    st.write("""
    Proyek B-ENC dikembangkan sebagai media pembelajaran kriptografi
    simetris berbasis barcode untuk mahasiswa informatika.
    """)
