from Crypto.Random import get_random_bytes

key = get_random_bytes(16)  # Šifrēšanas atslēga
mac_key = get_random_bytes(16)  # CMAC atslēga

with open('key.bin', 'w') as f:
    f.write(key.hex())
    f.write(mac_key.hex())
