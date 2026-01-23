import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw

# =========================================
# 👤 CONFIGURATION
# =========================================
DEVELOPER_NAME = "Nayla R"  # <--- GANTI NAMA KAMU
SECRET_KEY = "101011"
APP_TITLE = "B-ENC PROTOCOL"
# =========================================

st.set_page_config(
    page_title=f"{APP_TITLE} | {DEVELOPER_NAME}",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# 🎨 CUSTOM CSS (GLASSMORPHISM THEME)
# =========================================
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Global Style */
    .stApp {
        background: radial-gradient(circle at top left, #1b003a, #0d0d1a, #000000);
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 25, 0.6);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #00C6FF, #0072FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    /* Glass Card Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
    }

    /* Input Fields styling */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #fff !important;
        border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Custom Button */
    .stButton > button {
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.5);
    }
    
    /* Badge Style */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(0, 255, 136, 0.1);
        color: #00ff88;
        border: 1px solid rgba(0, 255, 136, 0.2);
    }

    /* Barcode Label Effect */
    .barcode-container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# =========================================
# 🧠 LOGIC & FUNCTIONS
# =========================================

def generate_real_barcode_visual(cipher_numbers):
    """Generates a realistic looking retail barcode (B/W)."""
    if not cipher_numbers: return None
    multiplier = 4
    height = 120
    # Hitung lebar estimasi
    estimated_width = (len(cipher_numbers) * 6 * multiplier) + 100
    
    img = Image.new('RGB', (estimated_width, height), 'white')
    draw = ImageDraw.Draw(img)
    current_x = 20
    
    # Guard Bar Start
    draw.rectangle([current_x, 0, current_x + multiplier, height], fill="black")
    current_x += multiplier * 2
    draw.rectangle([current_x, 0, current_x + multiplier, height], fill="black")
    current_x += multiplier * 2
    
    # Data Bars
    for num in cipher_numbers:
        unit_width = (abs(num) % 4) + 1
        pixel_width = unit_width * multiplier
        draw.rectangle([current_x, 0, current_x + pixel_width, height - 15], fill="black")
        current_x += pixel_width
        current_x += multiplier * 2 # Spasi putih
        
    # Guard Bar End
    draw.rectangle([current_x, 0, current_x + multiplier, height], fill="black")
    current_x += multiplier * 2
    draw.rectangle([current_x, 0, current_x + multiplier, height], fill="black")
    current_x += multiplier + 20
    
    return img.crop((0, 0, current_x, height))

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
    cipher_nums, []
    details = []
    key_len = len(key)
    for i, num in enumerate(numbers):
        key_bit = key[i % key_len]
        change = 3 if key_bit == '1' else -1
        new_num = num + change
        details.append({"Char": chars[i], "Val": num, "Bit": "◼" if key_bit=='1' else "◻", "Mod": f"{'+3' if change==3 else '-1'}", "Cipher": new_num})
    return [d['Cipher'] for d in details], pd.DataFrame(details)

def decrypt_b_enc(cipher_str, key):
    try:
        cipher_list = [int(x) for x in " ".join(cipher_str.split()).split()]
    except: return None, None, "Format Error"
    plain_nums = []
    details = []
    key_len = len(key)
    for i, val in enumerate(cipher_list):
        key_bit = key[i % key_len]
        change = -3 if key_bit == '1' else 1
        final = val + change
        plain_nums.append(final)
        char_res = chr(final+64) if 1<=final<=26 else ("(Spasi)" if final==0 else "?")
        details.append({"Cipher": val, "Mod": f"{'-3' if change==-3 else '+1'}", "Result": final, "Char": char_res})
    return numbers_to_text(plain_nums), pd.DataFrame(details), None

# --- STATE ---
if 'last_cipher_str' not in st.session_state: st.session_state['last_cipher_str'] = ""
if 'last_cipher_nums' not in st.session_state: st.session_state['last_cipher_nums'] = []

# =========================================
# 📱 LAYOUT & UI
# =========================================

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9373/9373886.png", width=60)
    st.markdown("### SYSTEM CONTROL")
    st.markdown(f"<div class='status-badge'>Dev: {DEVELOPER_NAME}</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("NAVIGATION", ["Dashboard", "Encryption", "Decryption"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("**Secure Key Status:**")
    st.progress(100)
    st.caption("Active & Hardcoded")

# --- MAIN HEADER ---
st.markdown(f"<div class='gradient-text'>{APP_TITLE}</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; opacity: 0.7;'>Secure Barcode Visualization System</p>", unsafe_allow_html=True)
st.write("") # Spacer

# --- DASHBOARD ---
if menu == "Dashboard":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("👋 Welcome back!")
        st.write(f"System is ready, **{DEVELOPER_NAME}**.")
        st.markdown("This tool demonstrates how **B-ENC Algorithm** transforms standard text into numeric cipher and generates realistic retail-style barcodes.")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.metric(label="Algorithm Type", value="Symmetric", delta="B-ENC")
        st.metric(label="Visualization", value="Dynamic Barcode", delta="Generated")
        st.markdown("</div>", unsafe_allow_html=True)

# --- ENCRYPTION ---
elif menu == "Encryption":
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("1. Input Data")
        st.caption("Enter text to generate barcode")
        plaintext = st.text_area("Plaintext:", height=120, placeholder="Type message here...")
        
        if st.button("Generate Secure Barcode ⚡"):
            if plaintext:
                c_nums, df_enc = encrypt_b_enc(plaintext, SECRET_KEY)
                st.session_state['last_cipher_nums'] = c_nums
                st.session_state['last_cipher_str'] = " ".join(map(str, c_nums))
                st.session_state['last_df_enc'] = df_enc
                st.toast("Encryption Successful!", icon="✅")
            else:
                st.toast("Please enter text first.", icon="⚠️")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_right:
        if st.session_state['last_cipher_nums']:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("2. Result")
            
            # --- BAGIAN VISUAL BARCODE ---
            st.write("**Generated Label:**")
            # Container putih khusus gambar
            st.markdown('<div class="barcode-container">', unsafe_allow_html=True)
            img = generate_real_barcode_visual(st.session_state['last_cipher_nums'])
            st.image(img, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
            # -----------------------------
            
            st.write("**Ciphertext Data:**")
            st.code(st.session_state['last_cipher_str'], language="text")
            
            with st.expander("Show Calculation Details"):
                st.dataframe(st.session_state['last_df_enc'], use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Waiting for input...")

# --- DECRYPTION ---
elif menu == "Decryption":
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Scanner Input")
        st.caption("Enter the numeric sequence from the barcode")
        
        default_val = st.session_state['last_cipher_str']
        cipher_in = st.text_area("Cipher Numbers:", value=default_val, height=120)
        
        if st.button("Decrypt Data 🔓"):
            if cipher_in:
                res, df_dec, err = decrypt_b_enc(cipher_in, SECRET_KEY)
                if err: st.error(err)
                else:
                    st.session_state['res_dec'] = res
                    st.session_state['df_dec'] = df_dec
                    st.toast("Decryption Complete!", icon="🔓")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_right:
        if 'res_dec' in st.session_state:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("Decrypted Message")
            st.markdown(f"<h1 style='color: #00C6FF; font-family: JetBrains Mono;'>{st.session_state['res_dec']}</h1>", unsafe_allow_html=True)
            
            st.divider()
            with st.expander("Validation Matrix"):
                st.dataframe(st.session_state['df_dec'], use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #666; font-size: 12px;'>SECURE ENCRYPTION SYSTEM V2.0 <br> Developed by {DEVELOPER_NAME}</div>", unsafe_allow_html=True)
