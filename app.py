import streamlit as st
import pandas as pd

# =========================================
# 📝 BAGIAN INI WAJIB DIGANTI NAMA KAMU
# =========================================
DEVELOPER_NAME = "Nayla R" 
# Ganti teks di dalam tanda kutip dengan namamu (misal: "Budi Santoso")
# =========================================

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title=f"B-ENC by {DEVELOPER_NAME}",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOGIKA KRIPTOGRAFI ---

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

def generate_barcode_html(binary_key):
    """Visualisasi Kunci (0/1) menjadi Barcode Hitam Putih."""
    html = '<div style="display: flex; gap: 3px; align-items: center; background: #f0f2f6; padding: 10px; border-radius: 5px; width: fit-content;">'
    for bit in binary_key:
        color = "#000000" if bit == '1' else "#ffffff"
        border = "1px solid #000"
        label = "+3" if bit == '1' else "-1"
        
        html += f'''
        <div style="text-align: center;">
            <div style="width: 25px; height: 50px; background-color: {color}; border: {border}; margin-bottom: 5px;"></div>
            <span style="font-size: 10px; font-weight: bold; font-family: monospace;">{bit}<br>{label}</span>
        </div>
        '''
    html += '</div>'
    return html

def generate_cipher_visualization(cipher_numbers):
    """
    Visualisasi HASIL ENKRIPSI.
    Mengubah angka menjadi batang visual.
    - Tinggi batang = Nilai angka.
    - Warna Hitam = Positif.
    - Warna Merah = Negatif/Nol (Indikator unik).
    """
    html = '<div style="display: flex; gap: 4px; align-items: flex-end; height: 100px; padding: 10px; background: #ffffff; border: 1px solid #ddd; border-radius: 8px; overflow-x: auto;">'
    
    for num in cipher_numbers:
        # Tentukan tinggi batang (maksimal 80px biar rapi)
        height = abs(num) * 3 
        if height > 80: height = 80
        if height < 5: height = 5
        
        # Tentukan warna
        if num > 0:
            color = "#333" # Hitam/Abu tua
        else:
            color = "#ff4b4b" # Merah (untuk angka negatif/nol)
            
        html += f'''
        <div style="text-align: center; min-width: 20px;">
            <div style="width: 15px; height: {height}px; background-color: {color}; margin: 0 auto;" title="Nilai: {num}"></div>
            <span style="font-size: 9px; color: #555;">{num}</span>
        </div>
        '''
    html += '</div>'
    return html

def encrypt_b_enc(plaintext, key):
    chars, numbers = text_to_numbers(plaintext)
    cipher_numbers = []
    details = []
    key_len = len(key)
    
    if not numbers: return [], pd.DataFrame()

    for i, num in enumerate(numbers):
        key_bit = key[i % key_len]
        original_num = num
        change = 3 if key_bit == '1' else -1
        new_num = original_num + change
        
        cipher_numbers.append(new_num)
        details.append({
            "Karakter": chars[i],
            "Angka Awal": original_num,
            "Bit Kunci": key_bit,
            "Operasi": f"{'+3' if change == 3 else '-1'}",
            "Hasil Cipher": new_num
        })
        
    return cipher_numbers, pd.DataFrame(details)

def decrypt_b_enc(cipher_str, key):
    cipher_str = " ".join(cipher_str.split())
    try:
        cipher_list = [int(x) for x in cipher_str.split(' ')]
    except ValueError:
        return None, None, "Error: Input hanya boleh angka dan spasi."

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

        details.append({
            "Cipher": cipher_val,
            "Bit Kunci": key_bit,
            "Operasi Balik": f"{'-3' if change == -3 else '+1'}",
            "Hasil Angka": final_num,
            "Hasil Huruf": char_res
        })
        
    return numbers_to_text(plain_numbers), pd.DataFrame(details), None

# --- 3. SESSION STATE ---
if 'last_ciphertext' not in st.session_state: st.session_state['last_ciphertext'] = ""
if 'last_plaintext' not in st.session_state: st.session_state['last_plaintext'] = ""

# --- 4. SIDEBAR & NAVIGASI ---
with st.sidebar:
    st.header("🔐 B-ENC Navigasi")
    
    selected_menu = st.selectbox(
        "Pilih Halaman:",
        ["🏠 Beranda", "📖 Teori Kriptografi", "🔒 Enkripsi (Encrypt)", "🔓 Dekripsi (Decrypt)", "👀 Visualisasi Kunci", "ℹ️ Tentang"]
    )
    
    st.markdown("---")
    st.markdown("### 🔑 Konfigurasi Kunci")
    global_key = st.text_input("Pola Barcode (Biner):", value="101011")
    
    if not all(c in '01' for c in global_key) or len(global_key) == 0:
        st.error("Kunci tidak valid! Gunakan 0 dan 1.")
        st.stop()
    
    st.caption("Visualisasi Kunci Aktif:")
    st.markdown(generate_barcode_html(global_key), unsafe_allow_html=True)
    
    # --- IDENTITAS DI SIDEBAR ---
    st.markdown("---")
    st.markdown(f"**Developed by:**\n### {DEVELOPER_NAME}")
    st.caption("© 2024 B-ENC Project")

# --- 5. KONTEN HALAMAN ---

# === HALAMAN BERANDA ===
if selected_menu == "🏠 Beranda":
    st.title(f"Selamat Datang, {DEVELOPER_NAME}!")
    st.subheader("Sistem Demonstrasi Kriptografi B-ENC")
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2462/2462829.png", width=200)
    with col2:
        st.markdown("""
        **B-ENC (Barcode-Based Encryption Cipher)** adalah metode kriptografi sederhana.
        Website ini dibuat khusus untuk memenuhi tugas dan demonstrasi edukasi.
        
        **Fitur Unggulan:**
        1.  **Visualisasi Barcode:** Melihat bagaimana biner diubah jadi grafik.
        2.  **Visualisasi Ciphertext:** Hasil enkripsi ditampilkan dalam bentuk grafik batang.
        3.  **Matematika Cermin:** Menjamin pesan bisa dikembalikan 100% akurat.
        """)
        
    st.success(f"⚡ Sistem siap digunakan. Dibuat dengan bangga oleh **{DEVELOPER_NAME}**.")

# === HALAMAN TEORI ===
elif selected_menu == "📖 Teori Kriptografi":
    st.title("📖 Teori Dasar")
    st.write("Memahami logika di balik B-ENC.")
    st.divider()
    st.markdown("""
    ### Logika Warna & Angka
    Metode ini menggunakan pergeseran angka (Shift Cipher) yang dinamis berdasarkan pola barcode.
    
    | Bit | Visual | Enkripsi (Maju) | Dekripsi (Mundur) |
    | :---: | :---: | :---: | :---: |
    | **1** | ⬛ | **+3** | **-3** |
    | **0** | ⬜ | **-1** | **+1** |
    """)

# === HALAMAN ENKRIPSI ===
elif selected_menu == "🔒 Enkripsi (Encrypt)":
    st.title("🔒 Enkripsi Pesan")
    st.divider()
    
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.subheader("1. Input Teks")
        plaintext_input = st.text_area("Plaintext:", height=150, placeholder="Ketik pesan rahasia di sini...")
        
        if st.button("🚀 Proses Enkripsi", type="primary"):
            if plaintext_input:
                cipher_nums, df_enc = encrypt_b_enc(plaintext_input, global_key)
                cipher_str = " ".join(map(str, cipher_nums))
                
                st.session_state['last_ciphertext'] = cipher_str
                st.session_state['last_plaintext'] = plaintext_input
                st.success("Enkripsi Selesai!")
            else:
                st.warning("Masukkan teks dulu.")

    with col_result:
        st.subheader("2. Hasil Enkripsi")
        if 'last_ciphertext' in st.session_state and st.session_state['last_ciphertext']:
            # Tampilan Angka
            st.info("Ciphertext (Angka):")
            st.code(st.session_state['last_ciphertext'], language="text")
            
            # --- FITUR BARU: VISUALISASI HASIL ---
            st.write("### 📊 Visualisasi Hasil")
            st.caption("Grafik representasi nilai ciphertext (Hitam=Positif, Merah=Negatif/Nol)")
            
            # Ambil angka dari string untuk divisualisasikan
            c_nums = [int(x) for x in st.session_state['last_ciphertext'].split()]
            st.markdown(generate_cipher_visualization(c_nums), unsafe_allow_html=True)
            # -------------------------------------
            
            if plaintext_input == st.session_state.get('last_plaintext', ''):
                 _, df_show = encrypt_b_enc(plaintext_input, global_key)
                 with st.expander("Lihat Detail Perhitungan"):
                     st.dataframe(df_show, use_container_width=True)

# === HALAMAN DEKRIPSI ===
elif selected_menu == "🔓 Dekripsi (Decrypt)":
    st.title("🔓 Dekripsi Pesan")
    st.divider()

    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.subheader("Input Ciphertext")
        default_val = st.session_state.get('last_ciphertext', "")
        cipher_input = st.text_area("Deret Angka:", value=default_val, height=150)
        
        if st.button("🔍 Balikkan ke Teks", type="primary"):
            if cipher_input:
                res_text, df_dec, err = decrypt_b_enc(cipher_input, global_key)
                if err:
                    st.error(err)
                else:
                    st.session_state['result_text'] = res_text
                    st.session_state['result_df'] = df_dec
                    st.success("Dekripsi Berhasil!")

    with col_result:
        st.subheader("Hasil Plaintext")
        if 'result_text' in st.session_state:
            st.markdown(f"## {st.session_state['result_text']}")
            if 'result_df' in st.session_state:
                with st.expander("Lihat Detail"):
                     st.dataframe(st.session_state['result_df'], use_container_width=True)

# === HALAMAN LAIN ===
elif selected_menu == "👀 Visualisasi Kunci":
    st.title("Visualisasi Kunci")
    st.write(f"Kunci saat ini: `{global_key}`")
    st.markdown(generate_barcode_html(global_key), unsafe_allow_html=True)

elif selected_menu == "ℹ️ Tentang":
    st.title("Tentang")
    st.write("Aplikasi ini dibuat oleh:")
    st.header(DEVELOPER_NAME)
    st.write("Mahasiswa Teknik Informatika / Ilmu Komputer")
    st.write("Tujuan: Edukasi Kriptografi Simetris.")

# --- FOOTER GLOBAL ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: gray;'>Created with ❤️ by <b>{DEVELOPER_NAME}</b> | Powered by Python Streamlit</div>", unsafe_allow_html=True)
