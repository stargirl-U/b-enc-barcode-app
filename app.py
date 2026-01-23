import streamlit as st
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="B-ENC Cryptography",
    page_icon="🔐",
    layout="wide"
)

# --- FUNGSI LOGIKA B-ENC (PRESISI) ---

def text_to_numbers(text):
    """
    Mengubah teks menjadi angka.
    A=1, B=2 ... Z=26
    Spasi = 0
    Karakter lain diabaikan untuk menjaga konsistensi.
    """
    text = text.upper()
    numbers = []
    chars = []
    
    for char in text:
        if 'A' <= char <= 'Z':
            num = ord(char) - 64 # A (65) jadi 1
            numbers.append(num)
            chars.append(char)
        elif char == ' ':
            numbers.append(0)
            chars.append('(Spasi)')
            
    return chars, numbers

def numbers_to_text(numbers):
    """
    Mengubah angka kembali menjadi teks.
    Hanya menerima angka yang valid hasil dekripsi.
    """
    text = ""
    for num in numbers:
        try:
            val = int(num)
            if 1 <= val <= 26:
                text += chr(val + 64) # 1 jadi A (65)
            elif val == 0:
                text += " "
            else:
                text += "?" # Jika kunci salah, hasil bisa di luar jangkauan
        except ValueError:
            pass
    return text

def generate_barcode_html(binary_key):
    """Visualisasi Barcode HTML."""
    html = '<div style="display: flex; gap: 4px; align-items: center;">'
    for bit in binary_key:
        color = "#000000" if bit == '1' else "#ffffff"
        border = "1px solid #000" # Tambah border agar warna putih terlihat
        label = "+3" if bit == '1' else "-1"
        
        html += f'''
        <div style="text-align: center;">
            <div style="width: 20px; height: 50px; background-color: {color}; border: {border}; margin-bottom: 5px;"></div>
            <span style="font-size: 10px; font-weight: bold;">{label}</span>
        </div>
        '''
    html += '</div>'
    return html

def encrypt_b_enc(plaintext, key):
    chars, numbers = text_to_numbers(plaintext)
    cipher_numbers = []
    details = []
    key_len = len(key)
    
    # Jika plaintext kosong/simbol semua
    if not numbers:
        return [], pd.DataFrame()

    for i, num in enumerate(numbers):
        key_bit = key[i % key_len]
        original_num = num
        
        # RUMUS ENKRIPSI
        # Bit 1 -> Ditambah 3
        # Bit 0 -> Dikurang 1
        if key_bit == '1':
            change = 3
        else:
            change = -1
            
        new_num = original_num + change
        cipher_numbers.append(new_num)
        
        details.append({
            "Huruf": chars[i],
            "Angka Asli": original_num,
            "Bit Kunci": key_bit,
            "Rumus": f"{original_num} {'+' if change > 0 else ''}{change}",
            "Cipher (Angka)": new_num
        })
        
    return cipher_numbers, pd.DataFrame(details)

def decrypt_b_enc(cipher_str, key):
    # Membersihkan input (hapus spasi ganda/enter)
    cipher_str = " ".join(cipher_str.split())
    
    try:
        cipher_list = [int(x) for x in cipher_str.split(' ')]
    except ValueError:
        return None, None, "Format Error: Pastikan input hanya angka dan spasi."

    plain_numbers = []
    details = []
    key_len = len(key)
    
    for i, cipher_val in enumerate(cipher_list):
        key_bit = key[i % key_len]
        
        # RUMUS DEKRIPSI (KEBALIKAN TOTAL)
        # Bit 1 (tadi +3) -> Sekarang DIKURANG 3
        # Bit 0 (tadi -1) -> Sekarang DITAMBAH 1
        if key_bit == '1':
            change = -3
            rumus_str = "- 3"
        else:
            change = 1
            rumus_str = "+ 1"
            
        final_num = cipher_val + change
        plain_numbers.append(final_num)
        
        # Mapping hasil angka ke huruf untuk tabel
        char_res = ""
        if 1 <= final_num <= 26:
            char_res = chr(final_num + 64)
        elif final_num == 0:
            char_res = "(Spasi)"
        else:
            char_res = "?" # Indikator kunci salah

        details.append({
            "Cipher (Angka)": cipher_val,
            "Bit Kunci": key_bit,
            "Rumus Balik": f"{cipher_val} {rumus_str}",
            "Hasil Angka": final_num,
            "Hasil Huruf": char_res
        })
        
    final_text = numbers_to_text(plain_numbers)
    return final_text, pd.DataFrame(details), None

# --- UI UTAMA ---

st.sidebar.title("Navigasi B-ENC")
menu = st.sidebar.radio("Menu", ["Beranda", "Enkripsi & Dekripsi", "Tentang"])

if menu == "Beranda":
    st.title("🔐 B-ENC Simulator")
    st.write("Selamat datang di simulasi kriptografi berbasis Barcode.")
    st.info("Pilih menu **Enkripsi & Dekripsi** di sebelah kiri untuk memulai percobaan.")
    
    st.markdown("""
    ### Prinsip Reversibility (Keterbalikan)
    Agar pesan bisa kembali seperti semula, kita menggunakan matematika sederhana:
    * Jika Enkripsi **menambah 3**, maka Dekripsi **mengurangi 3**.
    * Jika Enkripsi **mengurangi 1**, maka Dekripsi **menambah 1**.
    """)

elif menu == "Enkripsi & Dekripsi":
    st.title("⚙️ Laboratorium B-ENC")
    
    # Input Kunci Global
    st.sidebar.markdown("### Pengaturan Kunci")
    key = st.sidebar.text_input("Masukkan Kunci (Biner):", value="101011")
    
    # Validasi Kunci
    if not all(c in '01' for c in key) or len(key) == 0:
        st.error("Kunci harus berupa kombinasi 0 dan 1!")
        st.stop()
        
    st.sidebar.markdown("Visualisasi Kunci:")
    st.sidebar.markdown(generate_barcode_html(key), unsafe_allow_html=True)

    # --- TAB ENKRIPSI ---
    st.subheader("1. Proses Enkripsi")
    plaintext = st.text_area("Masukkan Pesan Anda:", "JANGAN LUPA MAKAN", height=100)
    
    if plaintext:
        cipher_nums, df_enc = encrypt_b_enc(plaintext, key)
        
        # Tampilkan Hasil Ciphertext dalam format string yang mudah dicopy
        cipher_str = " ".join(map(str, cipher_nums))
        
        st.success("👇 Ini adalah Ciphertext (Angka Terenkripsi)")
        st.code(cipher_str, language="text")
        
        with st.expander("Lihat Detail Perhitungan Enkripsi"):
            st.dataframe(df_enc, use_container_width=True)
            
    st.markdown("---")
    
    # --- TAB DEKRIPSI ---
    st.subheader("2. Proses Dekripsi")
    st.write("Masukkan angka ciphertext di atas untuk mengembalikannya menjadi teks.")
    
    # Fitur otomatis copy dari hasil enkripsi (opsional untuk user)
    default_decrypt_val = cipher_str if plaintext else ""
    cipher_input = st.text_area("Masukkan Ciphertext (Angka):", value=default_decrypt_val, height=100)
    
    if st.button("Dekripsi Pesan"):
        if cipher_input.strip():
            res_text, df_dec, err = decrypt_b_enc(cipher_input, key)
            
            if err:
                st.error(err)
            else:
                st.success("✅ Hasil Dekripsi (Plaintext Akhir)")
                st.markdown(f"## {res_text}")
                
                # VERIFIKASI OTOMATIS
                # Kita bandingkan teks hasil dekripsi dengan input plaintext awal (jika ada)
                if plaintext:
                    # Normalisasi untuk perbandingan (upper case)
                    p_awal = text_to_numbers(plaintext)[0] # Ambil chars saja
                    p_akhir = text_to_numbers(res_text)[0]
                    
                    if p_awal == p_akhir:
                        st.toast("Validasi Sukses! Pesan kembali sempurna.", icon="✅")
                        st.info("🎯 **Status Validasi:** Sempurna. Plaintext Awal sama persis dengan Hasil Akhir.")
                    else:
                        st.warning("⚠️ Hasil berbeda. Pastikan kunci yang dipakai sama.")
                
                with st.expander("Lihat Detail Perhitungan Dekripsi"):
                    st.dataframe(df_dec, use_container_width=True)
        else:
            st.warning("Masukkan ciphertext terlebih dahulu.")

elif menu == "Tentang":
    st.title("Tentang")
    st.write("Dibuat untuk tujuan edukasi kriptografi B-ENC.")
