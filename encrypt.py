import os
import random
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# * Folder names
SRC_FOLDER = "SRC"
X_FOLDER = "X"
AREA51_FOLDER = os.path.join(X_FOLDER, "area51")

os.makedirs(AREA51_FOLDER, exist_ok=True)
# TODO ^ Create the Area51 folder in the x folder (if not exists)

def generate_key_iv():
    key = get_random_bytes(32)  # 256-bit key
    iv = get_random_bytes(16)    # 128-bit IV
    return key, iv

def encrypt_aes_cbc(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data, AES.block_size))

def encrypt_file(file_path):
    original_filename = os.path.basename(file_path)
    master_key, iv = generate_key_iv()
    
    master_key_hex = master_key.hex()
    iv_hex = iv.hex()
    
    random_number = random.randint(11111111, 99999999)
    #  TODO ^ Create a random file name
    xlist_filename = f"{random_number:x}.xlist"
    xlist_path = os.path.join(AREA51_FOLDER, xlist_filename)

    with open(xlist_path, "w") as xlist_file:
        xlist_file.write(f"[{master_key_hex};{original_filename}]")
    #  TODO ^ Write content to your .xlist file

    enc_filename = f"{iv_hex}.enc"
    enc_file_path = os.path.join(X_FOLDER, enc_filename)

    with open(file_path, "rb") as input_file:
        with open(enc_file_path, "wb") as enc_file:
            while True:
                data = input_file.read(512 * 1024 * 1024)  # 512 MB
                if not data:
                    break
                encrypted_data = encrypt_aes_cbc(data, master_key, iv)
                enc_file.write(encrypted_data)
    
    #  TODO ^ Read the file piece by piece and password

    print(f"{original_filename} was successfully encrypted and recorded as: {enc_filename}.")

def encrypt_files():
    for filename in os.listdir(SRC_FOLDER):
        file_path = os.path.join(SRC_FOLDER, filename)
        if os.path.isfile(file_path):
            encrypt_file(file_path)

encrypt_files()
input("The process has been completed, press Enter to continue ...")
# TODO ^ Start the encryption process