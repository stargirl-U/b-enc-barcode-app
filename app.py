import streamlit as st
import pandas as pd
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

# =========================================
# 👤 CONFIGURATION (Ubah di sini)
# =========================================
DEVELOPER_NAME = "Nayla R"
SECRET_KEY = "101011"
APP_TITLE = "B-ENC PROTOCOL"
# =========================================

st.set_page_config(
    page_title=f"{APP_TITLE}",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# 🎬 FUNGSI ANIMASI & GAMBAR
# =========================================
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Load Animasi
lottie_security = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5rImXb.json")
lottie_coding = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_w51pcehl.json")

# =========================================
# 🎨 CUSTOM CSS (Tampilan Cyber & Animasi)
# =========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 25, 0.6);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #00C6FF, #0072FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0px 0px 20px rgba(0, 198, 255, 0.3);
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
    }

    .stTextArea textarea, .stTextInput input {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #fff !important;
        border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 0 20px rgba(0, 114, 255, 0.6);
    }

    .barcode-container {
        background-color: white;
        padding: 25px; /* Tambah padding luar */
        border-radius: 12px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================
# 🧠 LOGIC: ENCRYPTION & BARCODE
# =========================================

def generate_scannable_barcode(data_string):
    """Membuat Barcode Standard Code 128 dengan Jarak Teks yang Lega."""
    if not data_string: return None
    
    Code128 = barcode.get_barcode_class('code128')
    rv = BytesIO()
    code = Code128(data_string, writer=ImageWriter())
    
    # Pengaturan agar angka tidak mepet batang
    options = {
        "module_height": 12.0,    # Tinggi batang
        "text_distance": 8.0,     # Jarak teks (sebelumnya mepet)
        "font_size": 10,          # Ukuran font
        "quiet_zone": 5.0,        # Margin pinggir
        "center_text": True
    }
    
    code.write(rv, options=options)
    return rv

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
        details.append({"Char": chars[i], "Val": num, "Bit": key_bit, "Mod": change, "Cipher": new_num})
    return cipher_nums, pd.DataFrame(details)

def decrypt_b_enc(cipher_str, key):
    try:
        cipher_list = [int(x) for x in " ".join(cipher_str.split()).split()]
    except: return None, None, "Format Error"
    plain_nums = []
    key_len = len(key)
    for i, val in enumerate(cipher_list):
        key_bit = key[i % key_len]
        change = -3 if key_bit == '1' else 1
        plain_nums.append(val + change)
    return numbers_to_text(plain_nums)

# --- STATE ---
if 'last_cipher_str' not in st.session_state: st.session_state['last_cipher_str'] = ""

# =========================================
# 📱 LAYOUT & SIDEBAR
# =========================================

with st.sidebar:
    # 1. Tampilkan LOGO image_0.png di kiri atas tulisan
    try:
        st.image("image_0.png", use_container_width=True)
    except:
        st.error("File 'image_0.png' belum di-upload!")

    # 2. Judul Sidebar
    st.markdown("### SYSTEM CONTROL")
    
    # 3. Menu Navigasi
    menu = st.radio("NAVIGATION", ["Dashboard", "Encryption", "Decryption"])
    
    # 4. Animasi Lottie di bawah menu
    if lottie_security:
        st_lottie(lottie_security, height=150, key="sidebar_anim")

# --- MAIN PAGE ---
st.markdown(f"<div class='gradient-text'>{APP_TITLE}</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>Animated & Scannable Security System</p>", unsafe_allow_html=True)

if menu == "Dashboard":
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("👋 Welcome!")
        st.write("Sistem ini mendukung Google Lens. Coba enkripsi pesan dan scan hasilnya!")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        if lottie_coding:
            st_lottie(lottie_coding, height=200)

elif menu == "Encryption":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    plaintext = st.text_input("Masukkan Pesan:")
    if st.button("Generate"):
        if plaintext:
            with st.spinner("Processing..."):
                c_nums, df = encrypt_b_enc(plaintext, SECRET_KEY)
                st.session_state['last_cipher_str'] = " ".join(map(str, c_nums))
                
                st.success("Barcode Ready!")
                st.markdown('<div class="barcode-container">', unsafe_allow_html=True)
                # Tampilkan barcode scannable
                img = generate_scannable_barcode(st.session_state['last_cipher_str'])
                st.image(img)
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Decryption":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    cipher_in = st.text_area("Masukkan Angka Cipher:", value=st.session_state['last_cipher_str'])
    if st.button("Decrypt"):
        hasil = decrypt_b_enc(cipher_in, SECRET_KEY)
        st.info(f"Hasil Pesan: {hasil}")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption(f"© 2024 {DEVELOPER_NAME} - B-ENC Protocol V4.1")
