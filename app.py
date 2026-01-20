import streamlit as st
import barcode
from barcode.writer import ImageWriter
from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import os

# ======================
# KONFIGURASI
# ======================
KEY = "101011"
BARCODE_DIR = "barcodes"
os.makedirs(BARCODE_DIR, exist_ok=True)

# ======================
# KONVERSI
# ======================
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

# ======================
# B-ENC CORE
# ======================
def benc(numbers, mode="encrypt"):
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

# ======================
# BARCODE GENERATOR
# ======================
def generate_barcode(data):
    code = barcode.get("code128", data, writer=ImageWriter())
    path = os.path.join(BARCODE_DIR, "cipher_barcode")
    return code.save(path)

# ======================
# STREAMLIT UI
# ======================
st.title("🔐 B-ENC Barcode Cipher (Auto Scan & Dekripsi)")

menu = st.radio("Mode:", ["Enkripsi → Barcode", "Scan Barcode → Plaintext"])

# ======================
# ENKRIPSI
# ======================
if menu == "Enkripsi → Barcode":
    plaintext = st.text_area("Masukkan Plaintext")

    if st.button("Enkripsi & Buat Barcode"):
        nums = text_to_numbers(plaintext)
        cipher_nums = benc(nums, "encrypt")
        cipher_text = "-".join(map(str, cipher_nums))

        st.subheader("Ciphertext (tersimpan di barcode)")
        st.code(cipher_text)

        barcode_path = generate_barcode(cipher_text)
        img = Image.open(barcode_path)

        st.subheader("Barcode (Scan dengan kamera)")
        st.image(img)

# ======================
# SCAN & DEKRIPSI
# ======================
if menu == "Scan Barcode → Plaintext":
    st.write("Arahkan kamera ke barcode")

    image = st.camera_input("Scan Barcode")

    if image is not None:
        # konversi ke OpenCV
        img = Image.open(image)
        img_np = np.array(img)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        decoded = decode(img_cv)

        if decoded:
            cipher_text = decoded[0].data.decode("utf-8")
            st.subheader("Ciphertext Terdeteksi")
            st.code(cipher_text)

            cipher_nums = list(map(int, cipher_text.split("-")))
            plain_nums = benc(cipher_nums, "decrypt")
            plaintext = numbers_to_text(plain_nums)

            st.subheader("Plaintext Asli")
            st.success(plaintext)
        else:
            st.warning("Barcode belum terbaca dengan jelas")
