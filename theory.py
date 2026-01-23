import streamlit as st

def show_theory():
    st.header("📘 Teori Dasar Kriptografi")

    st.markdown("""
### 🔐 Apa itu Kriptografi?
Kriptografi adalah teknik untuk mengamankan informasi dengan mengubah pesan asli (plaintext)
menjadi pesan tersandi (ciphertext).

### 🔁 Kriptografi Simetris
Menggunakan **kunci yang sama** untuk proses enkripsi dan dekripsi.

### 🧾 Barcode & Sistem Biner
Barcode 1D terdiri dari garis hitam dan putih:
- Hitam = 1
- Putih = 0

Pada metode **B-ENC**, barcode digunakan sebagai pola kunci untuk menentukan operasi enkripsi.
""")
