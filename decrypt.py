import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

X_FOLDER = "X"
AREA51_FOLDER = os.path.join(X_FOLDER, "area51")
LOOK_AT_HERE_FOLDER = "LOOK-AT-ME"

os.makedirs(LOOK_AT_HERE_FOLDER, exist_ok=True)

def decrypt_aes_cbc(encrypted_data, key_hex, iv_hex):
    key = bytes.fromhex(key_hex)
    iv = bytes.fromhex(iv_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data

def decrypt_files():
    for enc_filename in os.listdir(X_FOLDER):
        if not enc_filename.endswith(".enc"):
            continue
        
        iv_hex = enc_filename.split(".")[0]
        enc_file_path = os.path.join(X_FOLDER, enc_filename)
        
        with open(enc_file_path, "rb") as enc_file:
            encrypted_data = enc_file.read()

        for xlist_filename in os.listdir(AREA51_FOLDER):
            if not xlist_filename.endswith(".xlist"):
                continue

            xlist_path = os.path.join(AREA51_FOLDER, xlist_filename)
            with open(xlist_path, "r") as xlist_file:
                xlist_content = xlist_file.read().strip()
                
            xlist_key_hex, original_filename = xlist_content.strip("[]").split(";")

            if xlist_key_hex:
                try:
                    decrypted_data = decrypt_aes_cbc(encrypted_data, xlist_key_hex, iv_hex)

                    output_path = os.path.join(LOOK_AT_HERE_FOLDER, original_filename)
                    with open(output_path, "wb") as output_file:
                        output_file.write(decrypted_data)

                    print(f"The {enc_filename} file was successfully solved using the '{xlist_key_hex}' key and saved as {original_filename}.\n")
                    break 

                except Exception as e:
                    continue

decrypt_files()
input("The process has been completed, press Enter to continue ...")