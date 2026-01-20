import streamlit as st
import qrcode
from PIL import Image
from streamlit_qrcode_scanner import qrcode_scanner
import os

KEY = "101011"
QR_DIR = "qrcodes"
os.makedirs(QR_DIR, exist_ok=True)

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
# UI
# ======================
st.title("🔐 B-ENC Cipher dengan QR Code (Auto Scan)")

menu = st.radio("Mode:", ["Enkripsi → QR", "Scan QR → Dekripsi"])

# ======================
# ENKRIPSI
# ======================
if menu == "Enkripsi → QR":
    plaintext = st.text_area("Masukkan Plaintext")

    if st.button("Enkripsi & Buat QR"):
        nums = text_to_numbers(plaintext)
        cipher_nums = benc(nums, "encrypt")
        cipher_text = "-".join(map(str, cipher_nums))

        st.subheader("Ciphertext")
        st.code(cipher_text)

        qr = qrcode.make(cipher_text)
        path = os.path.join(QR_DIR, "cipher_qr.png")
        qr.save(path)

        st.subheader("QR Code (Scan Langsung)")
        st.image(Image.open(path))

# ======================
# SCAN QR
# ======================
if menu == "Scan QR → Dekripsi":
    st.write("Arahkan kamera ke QR Code")

    scanned = qrcode_scanner()

    if scanned:
        st.subheader("Ciphertext Terdeteksi")
        st.code(scanned)

        cipher_nums = list(map(int, scanned.split("-")))
        plain_nums = benc(cipher_nums, "decrypt")
        plaintext = numbers_to_text(plain_nums)

        st.subheader("Plaintext Asli")
        st.success(plaintext)
