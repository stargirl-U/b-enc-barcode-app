import streamlit as st
import barcode
from barcode.writer import ImageWriter
from PIL import Image
from pyzbar.pyzbar import decode
import numpy as np
import cv2
import os

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
# B-ENC
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
# BARCODE
# ======================
def generate_barcode(data):
    code = barcode.get("code128", data, writer=ImageWriter())
    path = os.path.join(BARCODE_DIR, "cipher_barcode")
    return code.save(path)

# ======================
# UI
# ======================
st.title("🔐 B-ENC Barcode Cipher (Camera Scan)")

menu = st.radio("Mode:", ["Enkripsi → Barcode", "Scan Barcode → Dekripsi"])

# ======================
# ENKRIPSI
# ======================
if menu == "Enkripsi → Barcode":
    plaintext = st.text_area("Masukkan Plaintext")

    if st.button("Enkripsi & Buat Barcode"):
        nums = text_to_numbers(plaintext)
        cipher_nums = benc(nums, "encrypt")
        cipher_text = "-".join(map(str, cipher_nums))

        st.subheader("Ciphertext")
        st.code(cipher_text)

        barcode_path = generate_barcode(cipher_text)
        st.image(Image.open(barcode_path), caption="Scan barcode ini")

# ======================
# SCAN
# ======================
if menu == "Scan Barcode → Dekripsi":
    st.write("Ambil foto barcode menggunakan kamera")

    image = st.camera_input("Kamera")

    if image:
        img = Image.open(image)
        img_np = np.array(img)
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        decoded = decode(img_gray)

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
            st.error("Barcode tidak terbaca, coba ambil foto lebih jelas")
