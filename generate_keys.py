from Crypto.Random import get_random_bytes
import os

# Izveido random baitu failu ar izvēlētu izmēru
file_size = 1030
random_bytes = os.urandom(file_size)
file_path = 'input.bin'
with open(file_path, 'wb') as file:
    file.write(random_bytes)

key = get_random_bytes(16)  # Šifrēšanas atslēga
mac_key = get_random_bytes(16)  # CMAC atslēga

with open('key.bin', 'w') as f:
    f.write(key.hex())
    f.write(mac_key.hex())
