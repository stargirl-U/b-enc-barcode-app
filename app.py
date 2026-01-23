import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# =========================================
# 👤 IDENTITAS DEVELOPER & KUNCI RAHASIA
# =========================================
DEVELOPER_NAME = "Nayla R" 
# Kunci ini "tertanam" dalam sistem, tidak dilihat user.
SECRET_KEY = "101011" 
# =========================================

st.set_page_config(
    page_title=f"B-ENC Project by {DEVELOPER_NAME}",
    page_icon="📊",
    layout="wide"
)

# --- FUNGSI BARU: VISUALISASI CIPHERTEXT JADI GAMBAR ---
def generate_ciphertext_visual(cipher_numbers):
    """
    Mengubah deretan angka ciphertext menjadi gambar barcode dinamis.
    - Lebar batang = Nilai angka (absolut).
    - Warna Hitam = Angka Positif.
    - Warna Merah = Angka Negatif.
    """
    if not cipher_numbers:
        return None

    height = 80    # Tinggi gambar
    gap = 3        # Jarak antar batang
    multiplier = 5 # Pengali lebar agar tidak terlalu kurus (misal angka 1 jadi 5px)
    
    # 1. Hitung total lebar kanvas yang dibutuhkan
    total_width = 0
    for num in cipher_numbers:
        w = abs(num) * multiplier
        if w == 0: w = 5 # Lebar minimal untuk angka 0
        total_width += w + gap
    
    # Tambah sedikit padding di akhir
    total_width += 10

    # 2. Buat Kanvas Putih
    img = Image.new('RGB', (total_width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    current_x = 5 # Posisi awal menggambar (x)

    # 3. Mulai Menggambar Batang per Angka
    for num in cipher_numbers:
        # Tentukan lebar batang berdasarkan nilai angka
        bar_width = abs(num) * multiplier
        if bar_width == 0: bar_width = 5
        
        # Tentukan warna (Hitam jika positif, Merah jika negatif/nol)
        color = "black" if num > 0 else "#d62728" # Merah cerah
        
        # Gambar persegi panjang (batang)
        # Koordinat: [x_kiri, y_atas, x_kanan, y_bawah]
        draw.rectangle(
            [current_x, 0, current_x + bar_width, height - 20], 
            fill=color
        )
        
        # (Opsional) Tulis angkanya kecil di bawah batang agar jelas
        # draw.text((current_x, height - 15), str(num), fill="black", font_size=10)
        # Catatan: Menulis teks butuh font, kita skip dulu agar tidak ribet setupnya.
        
        # Geser posisi X untuk batang berikutnya
        current_x += bar_width + gap
            
    return img

# --- LOGIKA KRIPTOGRAFI (TETAP SAMA) ---
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
        change = 3 if key_bit == '1' else -1
        new_num = original_num + change
        
        cipher_numbers.append(new_num)
        
        # Sembunyikan kunci di tabel detail agar misterius
        visual_bit = "Hidden Key" 
        
        details.append({
            "Karakter": chars[i],
            "Angka Awal": original_num,
            "Kunci": visual_bit,
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

        details.append({
            "Cipher": cipher_val,
            "Operasi Balik": f"{'-3' if change == -3 else '+1'}",
            "Hasil Angka": final_num,
            "Hasil Huruf": char_res
        })
        
    return numbers_to_text(plain_numbers), pd.DataFrame(details), None

# --- STATE MANAGEMENT ---
if 'last_ciphertext_nums' not in st.session_state: st.session_state['last_ciphertext_nums'] = []
if 'last_ciphertext_str' not in st.session_state: st.session_state['last_ciphertext_str'] = ""

# --- SIDEBAR ---
with st.sidebar:
    st.header("B-ENC System")
    st.markdown(f"Developed by:\n### {DEVELOPER_NAME}")
    st.caption("© 2024 Teknik Komputer")
    st.markdown("---")
    
    menu = st.radio("Navigasi Utama", ["Enkripsi", "Dekripsi", "Tentang"])
    
    st.markdown("---")
    st.info("Sistem menggunakan Kunci Rahasia yang tertanam. Fokus pada visualisasi hasil.")

# --- HALAMAN ENKRIPSI (FOKUS UTAMA PERUBAHAN) ---
if menu == "Enkripsi":
    st.title("🔒 Enkripsi & Visualisasi")
    st.write("Masukkan pesan, sistem akan mengubahnya menjadi angka dan gambar barcode dinamis.")
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("1. Input Pesan")
        plaintext = st.text_area("Ketik di sini (Huruf A-Z):", height=150, placeholder="Contoh: HALO BANDUNG")
        
        if st.button("⚡ Proses Enkripsi", type="primary", use_container_width=True):
            if plaintext:
                # Proses Enkripsi
                cipher_nums, df_enc = encrypt_b_enc(plaintext, SECRET_KEY)
                
                # Simpan hasil ke session state
                st.session_state['last_ciphertext_nums'] = cipher_nums
                st.session_state['last_ciphertext_str'] = " ".join(map(str, cipher_nums))
                st.session_state['last_df_enc'] = df_enc
                
                st.success("Berhasil! Lihat visualisasi di samping 👉")
            else:
                st.warning("Isi pesan dulu.")
                
    with col2:
        st.subheader("2. Hasil Visualisasi Barcode")
        
        # Cek apakah ada data hasil enkripsi
        if st.session_state['last_ciphertext_nums']:
            # --- BAGIAN INI YANG MENAMPILKAN GAMBAR ---
            st.write("Berikut adalah representasi visual dari ciphertext Anda:")
            
            # Panggil fungsi pembuat gambar
            barcode_img = generate_ciphertext_visual(st.session_state['last_ciphertext_nums'])
            
            # Tampilkan gambarnya
            st.image(barcode_img, caption="Visualisasi Ciphertext Dinamis (Hitam=Positif, putih=Negatif)", use_container_width=False)
            # ------------------------------------------
            
            st.write("📃 **Bentuk Angka (Ciphertext):**")
            st.code(st.session_state['last_ciphertext_str'])

            with st.expander("🔍 Lihat Tabel Detail Perhitungan"):
                st.dataframe(st.session_state['last_df_enc'], use_container_width=True)
        else:
            st.info("Visualisasi akan muncul di sini setelah Anda melakukan enkripsi.")

# --- HALAMAN DEKRIPSI ---
elif menu == "Dekripsi":
    st.title("🔓 Dekripsi Data")
    st.write("Kembalikan angka ciphertext menjadi pesan yang bisa dibaca.")
    
    col1, col2 = st.columns(2)
    with col1:
        # Ambil nilai default dari hasil enkripsi sebelumnya
        default_val = st.session_state['last_ciphertext_str']
        cipher_in = st.text_area("Masukkan Ciphertext (Angka):", value=default_val, height=150)
        
        if st.button("🔓 Buka Pesan", use_container_width=True):
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
            st.subheader("Hasil Plaintext:")
            st.markdown(f"### {st.session_state['res_dec']}")
            
            with st.expander("Lihat Proses Pembalikan"):
                st.dataframe(st.session_state['df_dec'], use_container_width=True)

# --- HALAMAN TENTANG ---
elif menu == "Tentang":
    st.title("Tentang Project")
    st.write("Dibuat oleh:")
    st.header(DEVELOPER_NAME)
    st.divider()
    st.markdown("""
    ### Konsep Visualisasi Ciphertext
    Website ini mendemonstrasikan bagaimana data angka (ciphertext) dapat direpresentasikan menjadi bentuk visual.
    
    * **Lebar Batang:** Merepresentasikan besar nilai angka.
    * **Warna:** Hitam untuk positif, Putih untuk negatif.
    
    Tujuannya adalah menunjukkan bahwa data dapat diubah menjadi berbagai bentuk representasi lain yang tidak lazim dibaca manusia secara langsung.
    """)
