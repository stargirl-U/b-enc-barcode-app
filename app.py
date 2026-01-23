import streamlit as st
import pandas as pd

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="B-ENC System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOGIKA KRIPTOGRAFI (CORE) ---

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
    html = '<div style="display: flex; gap: 3px; align-items: center; background: #f0f2f6; padding: 10px; border-radius: 5px;">'
    for bit in binary_key:
        color = "#000000" if bit == '1' else "#ffffff"
        border = "1px solid #000"
        label = "+3" if bit == '1' else "-1"
        
        html += f'''
        <div style="text-align: center;">
            <div style="width: 25px; height: 60px; background-color: {color}; border: {border}; margin-bottom: 5px;"></div>
            <span style="font-size: 10px; font-weight: bold; font-family: monospace;">{bit}<br>{label}</span>
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
        
        # Logika: 1 -> +3, 0 -> -1
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
    # Membersihkan input dari spasi berlebih
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
        
        # Logika Balik: 1 -> -3, 0 -> +1
        change = -3 if key_bit == '1' else 1
        final_num = cipher_val + change
        plain_numbers.append(final_num)
        
        # Mapping huruf
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

# --- 3. SESSION STATE (Simpan Data Antar Halaman) ---
if 'last_ciphertext' not in st.session_state:
    st.session_state['last_ciphertext'] = ""
if 'last_plaintext' not in st.session_state:
    st.session_state['last_plaintext'] = ""

# --- 4. SIDEBAR & NAVIGASI ---
with st.sidebar:
    st.header("🔐 B-ENC Navigasi")
    
    # Menu Utama dengan Ikon
    selected_menu = st.selectbox(
        "Pilih Halaman:",
        [
            "🏠 Beranda",
            "📖 Teori Kriptografi",
            "🔒 Enkripsi (Encrypt)",
            "🔓 Dekripsi (Decrypt)",
            "👀 Visualisasi Kunci",
            "ℹ️ Tentang"
        ]
    )
    
    st.markdown("---")
    st.markdown("### 🔑 Konfigurasi Kunci")
    st.info("Kunci ini berlaku untuk semua halaman.")
    
    # Global Key Input
    global_key = st.text_input("Pola Barcode (Biner):", value="101011")
    
    if not all(c in '01' for c in global_key) or len(global_key) == 0:
        st.error("Kunci tidak valid! Gunakan 0 dan 1.")
        st.stop()
    
    # Mini Visualisasi di Sidebar
    st.caption("Visualisasi Kunci Aktif:")
    st.markdown(generate_barcode_html(global_key), unsafe_allow_html=True)

# --- 5. KONTEN HALAMAN ---

# === HALAMAN BERANDA ===
if selected_menu == "🏠 Beranda":
    st.title("Selamat Datang di B-ENC System")
    st.subheader("Media Pembelajaran Kriptografi Berbasis Barcode")
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2462/2462829.png", width=200)
    with col2:
        st.markdown("""
        **B-ENC (Barcode-Based Encryption Cipher)** adalah metode kriptografi sederhana untuk tujuan edukasi.
        Aplikasi ini membantu kamu memahami bagaimana komputer mengamankan pesan menggunakan logika matematika dan pola biner.
        
        **Apa yang bisa kamu lakukan di sini?**
        1.  Mempelajari teori dasar enkripsi.
        2.  Mengubah pesan rahasia menjadi kode angka.
        3.  Mengembalikan kode angka menjadi pesan asli.
        4.  Melihat bagaimana kunci biner divisualisasikan menjadi barcode.
        """)
        
    st.info("👈 Silakan pilih menu **Teori** atau **Enkripsi** di sidebar sebelah kiri untuk memulai.")

# === HALAMAN TEORI ===
elif selected_menu == "📖 Teori Kriptografi":
    st.title("📖 Teori Dasar B-ENC")
    st.divider()
    
    st.markdown("""
    ### 1. Apa itu Plaintext & Ciphertext?
    * **Plaintext:** Pesan asli yang bisa dibaca (Contoh: "AKU MAHASISWA").
    * **Ciphertext:** Pesan acak yang sudah disandikan (Contoh: "4 14 24 ...").
    
    ### 2. Bagaimana B-ENC Bekerja?
    Metode ini menggabungkan **Substitusi Angka** dan **Operasi Matematika** berdasarkan pola kunci.
    
    #### Langkah 1: Konversi Huruf
    Setiap huruf diubah menjadi angka urut:
    > A=1, B=2, C=3 ... Z=26, Spasi=0.
    
    #### Langkah 2: Penerapan Kunci Barcode
    Setiap angka akan diubah nilainya berdasarkan bit kunci (0 atau 1) pada posisi tersebut.
    
    | Bit Kunci | Warna Barcode | Operasi Enkripsi | Operasi Dekripsi |
    | :---: | :---: | :---: | :---: |
    | **1** | ⬛ Hitam | **Ditambah 3 (+3)** | **Dikurang 3 (-3)** |
    | **0** | ⬜ Putih | **Dikurang 1 (-1)** | **Ditambah 1 (+1)** |
    """)

# === HALAMAN ENKRIPSI ===
elif selected_menu == "🔒 Enkripsi (Encrypt)":
    st.title("🔒 Proses Enkripsi")
    st.markdown("Ubah teks biasa menjadi sandi angka.")
    st.divider()
    
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.subheader("Input")
        plaintext_input = st.text_area("Masukkan Plaintext:", height=150, placeholder="Ketik pesan di sini... (Huruf A-Z)")
        
        if st.button("🚀 Enkripsi Pesan", type="primary"):
            if plaintext_input:
                cipher_nums, df_enc = encrypt_b_enc(plaintext_input, global_key)
                cipher_str = " ".join(map(str, cipher_nums))
                
                # Simpan ke Session State (Agar otomatis muncul di menu Dekripsi)
                st.session_state['last_ciphertext'] = cipher_str
                st.session_state['last_plaintext'] = plaintext_input
                
                st.success("Enkripsi Berhasil!")
            else:
                st.warning("Mohon isi plaintext terlebih dahulu.")

    with col_result:
        st.subheader("Hasil")
        if 'last_ciphertext' in st.session_state and st.session_state['last_ciphertext']:
            st.info("👇 Salin angka ini:")
            st.code(st.session_state['last_ciphertext'], language="text")
            st.caption("Hasil ini sudah otomatis disalin ke menu Dekripsi.")
            
            # Tampilkan Tabel Detail jika ada data baru diproses
            if plaintext_input == st.session_state.get('last_plaintext', ''):
                 # Hitung ulang untuk tampilan tabel
                 _, df_show = encrypt_b_enc(plaintext_input, global_key)
                 with st.expander("Lihat Tabel Proses Perhitungan"):
                     st.dataframe(df_show, use_container_width=True)

# === HALAMAN DEKRIPSI ===
elif selected_menu == "🔓 Dekripsi (Decrypt)":
    st.title("🔓 Proses Dekripsi")
    st.markdown("Kembalikan sandi angka menjadi teks biasa.")
    st.divider()

    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.subheader("Input Ciphertext")
        # Ambil nilai default dari session state (hasil enkripsi sebelumnya)
        default_val = st.session_state.get('last_ciphertext', "")
        
        cipher_input = st.text_area("Masukkan Deret Angka:", value=default_val, height=150, help="Pisahkan angka dengan spasi")
        
        if st.button("🔍 Dekripsi Pesan", type="primary"):
            if cipher_input:
                res_text, df_dec, err = decrypt_b_enc(cipher_input, global_key)
                
                if err:
                    st.error(err)
                else:
                    st.session_state['result_text'] = res_text
                    st.session_state['result_df'] = df_dec
                    st.success("Dekripsi Berhasil!")
            else:
                st.warning("Isi ciphertext dulu.")

    with col_result:
        st.subheader("Hasil Plaintext")
        if 'result_text' in st.session_state:
            st.markdown(f"### {st.session_state['result_text']}")
            
            if 'result_df' in st.session_state:
                with st.expander("Lihat Tabel Proses Pembalikan"):
                     st.dataframe(st.session_state['result_df'], use_container_width=True)

# === HALAMAN VISUALISASI ===
elif selected_menu == "👀 Visualisasi Kunci":
    st.title("👀 Visualisasi Barcode")
    st.divider()
    
    st.markdown(f"### Kunci Saat Ini: `{global_key}`")
    st.write("Setiap bit 1 diwakili oleh balok hitam, dan bit 0 oleh balok putih.")
    
    st.markdown(generate_barcode_html(global_key), unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("💡 **Tips:** Anda bisa mengubah pola kunci ini melalui menu di Sidebar (sebelah kiri).")

# === HALAMAN TENTANG ===
elif selected_menu == "ℹ️ Tentang":
    st.title("Tentang Pengembang")
    st.divider()
    st.markdown("""
    **Proyek Website B-ENC**
    
    Dibuat sebagai sarana edukasi untuk mata kuliah Kriptografi.
    Website ini tidak menyimpan data apapun ke dalam server (Stateless), sehingga aman untuk digunakan sebagai alat simulasi.
    
    **Fitur Versi 1.0:**
    * Algoritma B-ENC (Simetris)
    * Visualisasi Barcode Real-time
    * Reversibility Check (Hasil Dekripsi = Plaintext Awal)
    """)
