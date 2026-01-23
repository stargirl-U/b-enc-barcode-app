import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw

# =========================================
# 👤 IDENTITAS & KUNCI (JANGAN DIUBAH)
# =========================================
DEVELOPER_NAME = "Nayla R"  # <--- GANTI INI PENTING!
SECRET_KEY = "101011" 
# =========================================

# --- KONFIGURASI HALAMAN DAN CSS CUSTOM ---
st.set_page_config(
    page_title=f"CYBER-ENC | {DEVELOPER_NAME}",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS UNTUK TAMPILAN CYBER DARK
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono&display=swap');
    .stApp { background: linear-gradient(to bottom right, #0f0c29, #302b63, #24243e); color: #e0e0e0; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 1px; }
    .main-title { font-size: 3em; font-weight: 700; background: linear-gradient(90deg, #00f260, #0575E6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 10px; }
    [data-testid="stSidebar"] { background-color: #1a1a2e; border-right: 1px solid #302b63; }
    .stTextArea textarea, .stTextInput input { background-color: #24243e !important; color: #00f260 !important; border: 1px solid #0575E6 !important; border-radius: 10px; font-family: 'Roboto Mono', monospace; }
    .stButton > button { width: 100%; background: linear-gradient(45deg, #0575E6, #021B79); color: white; border: none; padding: 12px 24px; font-family: 'Orbitron', sans-serif; border-radius: 12px; transition: 0.3s; box-shadow: 0 0 10px #0575E6; }
    .stButton > button:hover { background: linear-gradient(45deg, #00f260, #0575E6); box-shadow: 0 0 20px #00f260; transform: scale(1.02); }
    .cyber-card { background: rgba(40, 40, 70, 0.7); border-radius: 15px; padding: 20px; border: 1px solid #0575E6; box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-bottom: 20px; }
    [data-testid="stDataFrame"] { background-color: #24243e; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI CORE BARU: VISUALISASI REALISTIS ---

def generate_real_barcode_visual(cipher_numbers):
    """
    Membuat gambar yang meniru struktur barcode ritel (UPC/EAN).
    Hanya Hitam dan Putih.
    Lebar batang ditentukan oleh nilai ciphertext.
    """
    if not cipher_numbers: return None
    
    # Konfigurasi Ukuran
    multiplier = 4 # Pengali lebar dasar (makin besar makin tebal)
    height = 120   # Tinggi barcode
    
    # Estimasi lebar kanvas (agak berlebih dulu gapapa, nanti di-crop)
    estimated_width = (len(cipher_numbers) * 6 * multiplier) + 100
    
    # Buat Kanvas Background Putih Solid
    img = Image.new('RGB', (estimated_width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    current_x = 20 # Margin kiri
    
    # --- 1. GAMBAR GUARD BAR AWAL (Garis pembuka tipis ||) ---
    draw.rectangle([current_x, 0, current_x + multiplier, height], fill="black")
    current_x += multiplier * 2 # Geser melewati batang hitam + spasi putih
    draw.rectangle([current_x, 0, current_x + multiplier, height], fill="black")
    current_x += multiplier * 2 # Geser untuk mulai data
    
    # --- 2. GAMBAR DATA CIPHERTEXT ---
    for num in cipher_numbers:
        # Logika Lebar: Gunakan Modulo 4 agar variasi lebar hanya 1, 2, 3, atau 4 unit.
        # Ini menciptakan pola tebal-tipis yang realistis.
        # Kita gunakan nilai absolut (abs) karena barcode tidak mengenal negatif.
        unit_width = (abs(num) % 4) + 1
        pixel_width = unit_width * multiplier
        
        # Gambar Batang Hitam
        draw.rectangle([current_x, 0, current_x + pixel_width, height - 15], fill="black")
        current_x += pixel_width
        
        # Gambar Spasi Putih Standar (lebar 2 unit) setelah setiap batang
        current_x += multiplier * 2
        
    # --- 3. GAMBAR GUARD BAR AKHIR (Garis penutup tipis ||) ---
    draw.rectangle([current_x, 0, current_x + multiplier, height], fill="black")
    current_x += multiplier * 2
    draw.rectangle([current_x, 0, current_x + multiplier, height], fill="black")
    current_x += multiplier + 20 # Margin kanan
    
    # Crop gambar agar lebarnya pas sesuai konten
    img = img.crop((0, 0, current_x, height))
    
    return img

# --- LOGIKA KRIPTOGRAFI (TIDAK BERUBAH) ---
def text_to_numbers(text):
    text = text.upper()
    return [c for c in text if 'A'<=c<='Z' or c==' '], [ord(c)-64 if 'A'<=c<='Z' else 0 for c in text if 'A'<=c<='Z' or c==' ']

def numbers_to_text(numbers):
    res = ""
    for n in numbers:
        try:
            val = int(n)
            res += chr(val+64) if 1<=val<=26 else (" " if val==0 else "?")
        except: pass
    return res

def encrypt_b_enc(plaintext, key):
    chars, numbers = text_to_numbers(plaintext)
    if not numbers: return [], pd.DataFrame()
    cipher_nums = []
    details = []
    key_len = len(key)
    for i, num in enumerate(numbers):
        key_bit = key[i % key_len]
        change = 3 if key_bit == '1' else -1
        new_num = num + change
        cipher_nums.append(new_num)
        details.append({"Char": chars[i], "Awal": num, "Op": f"{'+3' if change==3 else '-1'}", "Akhir": new_num})
    return cipher_nums, pd.DataFrame(details)

def decrypt_b_enc(cipher_str, key):
    try:
        cipher_list = [int(x) for x in " ".join(cipher_str.split()).split()]
    except: return None, None, "Input error."
    plain_nums = []
    details = []
    key_len = len(key)
    for i, val in enumerate(cipher_list):
        key_bit = key[i % key_len]
        change = -3 if key_bit == '1' else 1
        final = val + change
        plain_nums.append(final)
        char_res = chr(final+64) if 1<=final<=26 else ("(Spasi)" if final==0 else "?")
        details.append({"Cipher": val, "Op Balik": f"{'-3' if change==-3 else '+1'}", "Hasil": final, "Huruf": char_res})
    return numbers_to_text(plain_nums), pd.DataFrame(details), None

# --- STATE ---
if 'last_ciphertext_str' not in st.session_state: st.session_state['last_ciphertext_str'] = ""
if 'last_ciphertext_nums' not in st.session_state: st.session_state['last_ciphertext_nums'] = []

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(f"<h2 style='text-align: center; color: #00f260;'>BERKAS SISTEM</h2>", unsafe_allow_html=True)
    st.caption(f"🔒 Authorized Access: {DEVELOPER_NAME}")
    st.markdown("---")
    menu = st.radio("PILIH MODUL:", ["🖥️ Dashboard", "🔒 Enkripsi Data", "🔓 Dekripsi Data"], index=1)
    st.markdown("---")
    st.info("Status Sistem: AMAN. Kunci Rahasia tertanam aktif.")

# --- MAIN CONTENT ---
st.markdown(f"<div class='main-title'>SISTEM ENKRIPSI B-ENC</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-family: Roboto Mono;'>Advanced Barcode-Based Security Protocol | Dev: {DEVELOPER_NAME}</p>", unsafe_allow_html=True)
st.divider()

if menu == "🖥️ Dashboard":
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.subheader("Selamat Datang di Pusat Kontrol")
    st.write("Sistem ini mendemonstrasikan pengamanan data menggunakan substitusi dinamis.")
    st.write("Data yang dienkripsi akan dirender menjadi visualisasi barcode ritel yang realistis.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🔒 Enkripsi Data":
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.subheader("📥 Input Terminal")
        plaintext = st.text_area("Masukkan Plaintext (A-Z):", height=150, placeholder="Ketik pesan rahasia...")
        if st.button("⚡ INISIALISASI ENKRIPSI"):
            if plaintext:
                c_nums, df_enc = encrypt_b_enc(plaintext, SECRET_KEY)
                st.session_state['last_ciphertext_nums'] = c_nums
                st.session_state['last_ciphertext_str'] = " ".join(map(str, c_nums))
                st.session_state['last_df_enc'] = df_enc
                st.success("DATA BERHASIL DIAMANKAN!")
            else: st.error("TERMINAL KOSONG.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.subheader("Generation Output")
        if st.session_state['last_ciphertext_nums']:
            st.write("Visualisasi Barcode Realistis (B/W):")
            # Wadah putih agar barcode terlihat jelas
            st.markdown('<div style="background: #ffffff; padding: 15px; border-radius: 10px; border: 3px solid #000; text-align: center;">', unsafe_allow_html=True)
            
            # PANGGIL FUNGSI BARU DI SINI
            img = generate_real_barcode_visual(st.session_state['last_ciphertext_nums'])
            st.image(img, use_container_width=False)
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption("Visualisasi ini meniru struktur barcode ritel berdasarkan nilai data ciphertext.")
            
            st.divider()
            st.write("Data Numerik:")
            st.code(st.session_state['last_ciphertext_str'], language="powershell")
        else: st.info("Menunggu input data...")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🔓 Dekripsi Data":
    # (Bagian Dekripsi sama seperti sebelumnya)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.subheader("🔑 Terminal Dekripsi")
        default_val = st.session_state['last_ciphertext_str']
        cipher_in = st.text_area("Input Ciphertext Numerik:", value=default_val, height=150)
        if st.button("🔓 BUKA PENGAMANAN DATA"):
            if cipher_in:
                res, df_dec, err = decrypt_b_enc(cipher_in, SECRET_KEY)
                if err: st.error(err)
                else:
                    st.session_state['res_dec'] = res
                    st.session_state['df_dec'] = df_dec
                    st.success("AKSES DITERIMA.")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.subheader("📄 Hasil Plaintext")
        if 'res_dec' in st.session_state:
            st.markdown(f"<h2 style='color: #00f260; font-family: Roboto Mono;'>{st.session_state['res_dec']}</h2>", unsafe_allow_html=True)
        else: st.write("Hasil akan muncul di sini.")
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align: center; font-family: Roboto Mono; font-size: 0.8em; color: gray;'>SECURE SYSTEM | Property of {DEVELOPER_NAME} | 2024</div>", unsafe_allow_html=True)
