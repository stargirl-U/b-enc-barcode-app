import streamlit as st
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import os

# ===============================
# KONFIGURASI
# ===============================
KEY = "101011"
BARCODE_DIR = "barcodes"

if not os.path.exists(BARCODE_DIR):
    os.makedirs(BARCODE_DIR)

# ===============================
# KONVERSI TEKS <-> ANGKA
# ===============================
def text_to_numbers(text):
    nums = []
    for c in text.upper():
        if c == " ":
            nums.append(0)
        elif c.isalpha():
            nums.append(ord(c) - 64)
    return nums

def numbers_to_text(nums):
    text = ""
    for n in nums:
        if n == 0:
            text += " "
        elif 1 <= n <= 26:
            text += chr(n + 64)
    return text.lower()

# ===============================
# B-ENC CORE
# ===============================
def benc_process(numbers, mode="encrypt"):
    result = []
    for num in numbers:
        value = num
        for bit in KEY:
            if mode == "encrypt":
                value += 3 if bit == "1" else -1
            else:
                value -= 3 if bit == "1" else +1
        result.append(value)
    return result

# ===============================
# BARCODE GENERATOR
# ===============================
def generate_barcode(data):
    code128 = barcode.get("code128", data, writer=ImageWriter())
    filename = os.path.join(BARCODE_DIR, "cipher_barcode")
    saved = code128.save(filename)
    return saved

# ===============================
# STREAMLIT UI
# ===============================
st.set_page_config(page_title="B-ENC Barcode Cipher", layout="centered")

st.title("🔐 B-ENC Barcode Cipher")
st.write("Enkripsi & Dekripsi berbasis Barcode (Scannable)")

menu = st.radio("Pilih Mode:", ["Enkripsi → Barcode", "Dekripsi dari Ciphertext"])

# ===============================
# ENKRIPSI
# ===============================
if menu == "Enkripsi → Barcode":
    plaintext = st.text_area("Masukkan Plaintext:")

    if st.button("Enkripsi & Buat Barcode"):
        nums = text_to_numbers(plaintext)
        cipher_nums = benc_process(nums, "encrypt")
        cipher_text = " ".join(map(str, cipher_nums))

        st.subheader("Ciphertext (Numerik)")
        st.code(cipher_text)

        barcode_path = generate_barcode(cipher_text)
        img = Image.open(barcode_path)

        st.subheader("Barcode (Scannable)")
        st.image(img, caption="Scan barcode ini untuk mendapatkan ciphertext")

# ===============================
# DEKRIPSI
# ===============================
elif menu == "Dekripsi dari Ciphertext":
    cipher_input = st.text_area(
        "Masukkan Ciphertext (hasil scan barcode, angka dipisah spasi):"
    )

    if st.button("Dekripsi"):
        try:
            cipher_nums = list(map(int, cipher_input.split()))
            plain_nums = benc_process(cipher_nums, "decrypt")
            plaintext = numbers_to_text(plain_nums)

            st.subheader("Plaintext")
            st.success(plaintext)

        except:
            st.error("Format ciphertext tidak valid.")
