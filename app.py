import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw

# =========================================
# 🕵️ KONFIGURASI RAHASIA (HANYA KITA YANG TAU)
# =========================================
DEVELOPER_NAME = "Nayla R" 

# INI ADALAH KUNCI RAHASIA (HARDCODED)
# Pengguna tidak bisa mengubah ini lewat website.
# Kamu bisa ganti pola ini sesuka hati di sini (0 = Putih, 1 = Hitam)
SECRET_KEY = "101011" 
# =========================================

st.set_page_config(
    page_title=f"B-ENC by {DEVELOPER_NAME}",
    page_icon="🛡️",
    layout="wide"
)

# --- FUNGSI GENERATOR GAMBAR (IMAGE PROCESSING) ---
def generate_real_barcode_image(binary_key):
    """
    Fungsi ini BENAR-BENAR MENGGAMBAR gambar digital.
    Bukan sekadar HTML, tapi image object.
    """
    # Konfigurasi Ukuran
    bar_width = 30
    height = 100
    width = len(binary_key) * bar_width
    
    # Buat Kanvas Putih Baru
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Mulai Menggambar Batang
    for i, bit in enumerate(binary_key):
        x_start = i * bar_width
        x_end = x_start + bar_width
        
        if bit == '1':
            # Gambar Kotak Hitam (Full Black)
            draw.rectangle([x_start, 0, x_end, height], fill="black")
        else:
            # Gambar Kotak Putih (Tapi dikasih garis tipis biar kelihatan batasnya)
            draw.rectangle([x_start, 0, x_end, height], fill="white", outline=None)
            
    return img

# --- LOGIKA KRIPTOGRAFI UTAMA ---
def text_to_numbers(text):
    text = text.upper()
    numbers = []
    chars = []
    for char in text:
        if 'A' <= char <= 'Z':
            num = ord(char) - 64
            numbers.append(num)
            chars.append(char)
        elif char == ' ':
            numbers.append(0)
            chars.append('(Spasi)')
    return chars, numbers

def numbers_to_text(numbers):
    text = ""
    for num in numbers:
        try:
            val = int(num)
            if 1 <= val <= 26:
                text += chr(val + 64)
            elif val == 0:
                text += " "
            else:
                text += "?"
        except ValueError:
            pass
    return text

def encrypt_b_enc(plaintext, key):
    chars, numbers = text_to_numbers(plaintext)
    cipher_numbers = []
    details = []
    key_len = len(key)
    
    if not numbers: return [], pd.DataFrame()

    for i, num in enumerate(numbers):
        key_bit = key[i % key_len]
        original_num = num
        
        # Logika: 1 -> +3, 0 -> -1
        change = 3 if key_bit == '1' else -1
        new_num = original_num + change
        
        cipher_numbers.append(new_num)
        
        # Di tabel detail, kita sembunyikan bit kuncinya agar misterius
        # Kita ganti dengan simbol visual saja
        visual_bit = "⬛ (Black)" if key_bit == '1' else "⬜ (White)"
        
        details.append({
            "Karakter": chars[i],
            "Angka Awal": original_num,
            "Pola Barcode": visual_bit, # Kunci biner disembunyikan
            "Operasi": f"{'+3' if change == 3 else '-1'}",
            "Hasil Cipher": new_num
        })
        
    return cipher_numbers, pd.DataFrame(details)

def decrypt_b_enc(cipher_str, key):
    cipher_str = " ".join(cipher_str.split())
    try:
        cipher_list = [int(x) for x in cipher_str.split(' ')]
    except ValueError:
        return None, None, "Error: Input harus angka."

    plain_numbers = []
    details = []
    key_len = len(key)
    
    for i, cipher_val in enumerate(cipher_list):
        key_bit = key[i % key_len]
        change = -3 if key_bit == '1' else 1
        final_num = cipher_val + change
        plain_numbers.append(final_num)
        
        if 1 <= final_num <= 26: char_res = chr(final_num + 64)
        elif final_num == 0: char_res = "(Spasi)"
        else: char_res = "?"

        visual_bit = "⬛" if key_bit == '1' else "⬜"

        details.append({
            "Cipher": cipher_val,
            "Pola Barcode": visual_bit,
            "Operasi Balik": f"{'-3' if change == -3 else '+1'}",
            "Hasil Angka": final_num,
            "Hasil Huruf": char_res
        })
        
    return numbers_to_text(plain_numbers), pd.DataFrame(details), None

# --- STATE MANAGEMENT ---
if 'last_ciphertext' not in st.session_state: st.session_state['last_ciphertext'] = ""
if 'last_plaintext' not in st.session_state: st.session_state['last_plaintext'] = ""

# --- SIDEBAR ---
with st.sidebar:
    st.header("B-ENC System")
    st.write(f"Dev: **{DEVELOPER_NAME}**")
    st.markdown("---")
    
    menu = st.radio("Menu Utama", 
        ["Beranda", "Enkripsi", "Dekripsi", "Tentang"])
    
    st.markdown("---")
    st.info("ℹ️ **Info Keamanan:**\nKunci enkripsi ditanam di dalam sistem (Hidden Key). Pengguna hanya perlu memasukkan pesan.")

# --- HALAMAN BERANDA ---
if menu == "Beranda":
    st.title("🛡️ Secure Barcode Encryption")
    st.write("Selamat datang di sistem demonstrasi B-ENC.")
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Menampilkan Barcode Kunci sebagai GAMBAR ASLI
        st.write("**Pola Kunci Sistem:**")
        barcode_img = generate_real_barcode_image(SECRET_KEY)
        st.image(barcode_img, caption="System Master Key", use_container_width=True)
        
    with col2:
        st.markdown("""
        ### Cara Kerja Sistem
        Sistem ini menggunakan **Master Key** berbentuk barcode di sebelah kiri.
        
        1.  Kamu tidak perlu tahu angka binernya.
        2.  Cukup lihat pola **Hitam** dan **Putih**.
        3.  Sistem otomatis menghitung sandi berdasarkan gambar tersebut.
        
        Silakan masuk ke menu **Enkripsi** untuk mencoba.
        """)

# --- HALAMAN ENKRIPSI ---
elif menu == "Enkripsi":
    st.title("🔒 Enkripsi Data")
    st.write("Sistem akan mengenkripsi pesanmu menggunakan kunci barcode rahasia.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        plaintext = st.text_area("Masukkan Pesan:", height=150)
        if st.button("🔒 Kunci Pesan Sekarang", type="primary"):
            if plaintext:
                cipher_nums, df_enc = encrypt_b_enc(plaintext, SECRET_KEY)
                st.session_state['last_ciphertext'] = " ".join(map(str, cipher_nums))
                st.session_state['last_plaintext'] = plaintext
                st.success("Berhasil diamankan!")
            else:
                st.warning("Isi pesan dulu.")
                
    with col2:
        if st.session_state['last_ciphertext']:
            st.subheader("Hasil Ciphertext")
            st.code(st.session_state['last_ciphertext'])
            
            st.write("Visualisasi Barcode Kunci yang digunakan:")
            # Generate gambar on-the-fly
            img = generate_real_barcode_image(SECRET_KEY)
            st.image(img, width=300)
            
            with st.expander("Lihat Logika Sistem"):
                # Hitung ulang untuk display tabel
                _, df_show = encrypt_b_enc(st.session_state['last_plaintext'], SECRET_KEY)
                st.dataframe(df_show, use_container_width=True)

# --- HALAMAN DEKRIPSI ---
elif menu == "Dekripsi":
    st.title("🔓 Dekripsi Data")
    
    col1, col2 = st.columns(2)
    with col1:
        cipher_in = st.text_area("Masukkan Ciphertext (Angka):", value=st.session_state['last_ciphertext'], height=150)
        if st.button("🔓 Buka Pesan"):
            if cipher_in:
                res, df_dec, err = decrypt_b_enc(cipher_in, SECRET_KEY)
                if err:
                    st.error(err)
                else:
                    st.session_state['res_dec'] = res
                    st.session_state['df_dec'] = df_dec
                    st.success("Pesan terbuka!")

    with col2:
        if 'res_dec' in st.session_state:
            st.subheader("Pesan Asli:")
            st.markdown(f"## {st.session_state['res_dec']}")
            
            with st.expander("Lihat Proses Pembalikan"):
                st.dataframe(st.session_state['df_dec'], use_container_width=True)

# --- HALAMAN TENTANG ---
elif menu == "Tentang":
    st.title(f"Tentang {DEVELOPER_NAME}")
    st.write("Website ini dibuat untuk tujuan edukasi keamanan data.")
    st.image(generate_real_barcode_image("111111"), width=200, caption="Developers Signature")
    st.markdown("---")
    st.caption(f"Copyright © 2024 {DEVELOPER_NAME}")
