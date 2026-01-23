KEY = "101011"

def char_to_num(c):
    if c == " ":
        return 0
    return ord(c.upper()) - 64

def num_to_char(n):
    if n == 0:
        return " "
    return chr(n + 64)

def encrypt_benc(plaintext):
    result = []
    table = []
    key_len = len(KEY)

    for i, char in enumerate(plaintext):
        base = char_to_num(char)
        bit = KEY[i % key_len]

        if bit == "1":
            cipher = base + 3
            op = "+3"
        else:
            cipher = base - 1
            op = "-1"

        cipher = max(0, cipher)
        result.append(cipher)

        table.append({
            "Karakter": char,
            "Nilai Awal": base,
            "Bit Key": bit,
            "Operasi": op,
            "Hasil": cipher
        })

    return result, table


def decrypt_benc(ciphertext):
    result = []
    table = []
    key_len = len(KEY)

    for i, num in enumerate(ciphertext):
        bit = KEY[i % key_len]

        if bit == "1":
            plain_num = num - 3
            op = "-3"
        else:
            plain_num = num + 1
            op = "+1"

        plain_num = max(0, plain_num)
        char = num_to_char(plain_num)
        result.append(char)

        table.append({
            "Cipher": num,
            "Bit Key": bit,
            "Operasi": op,
            "Hasil Angka": plain_num,
            "Karakter": char
        })

    return "".join(result), table
