import streamlit as st
import qrcode
from PIL import Image
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
# UI
# ======================
st.set_page_config(page_title="B-ENC Cipher Web", layout="centered")
st.title("🔐 B-ENC Cipher Web App")

menu = st.radio("Pilih Mode:", ["Enkripsi → QR Code", "Dekripsi dari Ciphertext"])

# ======================
# ENKRIPSI
# ======================
if menu == "Enkripsi → QR Code":
    plaintext = st.text_area("Masukkan Plaintext")

    if st.button("Enkripsi & Buat QR Code"):
        nums = text_to_numbers(plaintext)
        cipher_nums = benc(nums, "encrypt")
        cipher_text = "-".join(map(str, cipher_nums))

        st.subheader("Ciphertext")
        st.code(cipher_text)

        qr = qrcode.make(cipher_text)
        path = os.path.join(QR_DIR, "cipher_qr.png")
        qr.save(path)

        st.subheader("QR Code (Scan dengan HP)")
        st.image(Image.open(path))

# ======================
# DEKRIPSI
# ======================
if menu == "Dekripsi dari Ciphertext":
    cipher_input = st.text_area(
        "Masukkan Ciphertext (hasil scan QR Code)"
    )

    if st.button("Dekripsi"):
        try:
            cipher_nums = list(map(int, cipher_input.split("-")))
            plain_nums = benc(cipher_nums, "decrypt")
            plaintext = numbers_to_text(plain_nums)

            st.subheader("Plaintext Asli")
            st.success(plaintext)
        except:
            st.error("Format ciphertext tidak valid")
