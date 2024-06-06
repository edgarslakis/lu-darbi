from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import CMAC
import binascii
import argparse

# Ievades teksta papildināšanai līdz apaļam bloka izmēram
def pad(text, block_size):
    padding_len = block_size - len(text) % block_size
    padding = bytes([padding_len] * padding_len)
    return text + padding

# Teksta attīrīšana no papildinājumiem bloka izmēram
def unpad(padded_text):
    padding_len = padded_text[-1]
    return padded_text[:-padding_len]

# XOR divām baitu virknēm rāvējslēdzējā
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# Šifrēšanas funkcija vienam blokam no Cryptodome bibliotēkas
def encrypt_block(block, key):
    # Izveido jaunu AES šifrētāju ar atslēgu un atgriež šifrētu bloku
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)
# Simetriska atšifrēšanas funkcija vienam blokam
def decrypt_block(block, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(block)

# Teksta šifrēšana ar CFB metodi
def encrypt_text_cfb(plain_text, key, mac_key):
    block_size = AES.block_size
    # ģenerē inicializēšanas vektoru viena bloka garumā (16 baiti)
    iv = get_random_bytes(block_size)
    # Papildina (pad) tekstu tā, lai tas būtu pilnā AES 16 baitu bloka garumā
    padded_text = plain_text.encode()
    cipher_text = b''

    # Šifrēšana pa blokiem. Sāk ar iv bloku
    previous_block = iv
    for i in range(0, len(padded_text), block_size):
        current_block = padded_text[i:i + block_size]
        # Šifrē iepriekšējo bloku
        encrypted_block = encrypt_block(previous_block, key)
        # XOR starp iepriekšējo un tekošo teksta bloku
        encrypted_output = xor_bytes(current_block, encrypted_block)
        cipher_text += encrypted_output
        # Šifrētais bloks kļūst par iepriekšējo bloku nākamajam ciklam
        previous_block = encrypted_output

    # Izrēķina CMAC vērtību ar Cryptodome funkciju bibliotēku
    cmac = CMAC.new(mac_key, ciphermod=AES)
    cmac.update(cipher_text)
    mac = cmac.digest()

    return iv + cipher_text + mac

# Teksta atšifrēšana ar CFB metodi. Pretējā virzienā šifrēšanai
def decrypt_text_cfb(data, key, mac_key):
    block_size = AES.block_size
    # Izdala inicializēšanas vektoru un ziņu no šifrētās baitu virknes
    iv = data[:block_size]
    mac = data[-block_size:]
    cipher_text = data[block_size:-block_size]
    decrypted_text = b''

    # Verificē ziņas autentiskumu, pārbaudot CMAC
    cmac = CMAC.new(mac_key, ciphermod=AES)
    cmac.update(cipher_text)
    try:
        cmac.verify(mac)
        print("MAC sakrīt!")
    except ValueError:
        raise ValueError("MAC check failed")

    previous_block = iv
    for i in range(0, len(cipher_text), block_size):
        current_block = cipher_text[i:i + block_size]
        # Šifrē iepriekšējo bloku
        encrypted_block = encrypt_block(previous_block, key)
        # XOR starp iepriekšējo un tekošo teksta bloku
        decrypted_output = xor_bytes(current_block, encrypted_block)
        decrypted_text += decrypted_output
        # Šifrētais bloks kļūst par "iepriekšējais bloks" nākamajam ciklam
        previous_block = current_block

    return decrypted_text.decode('utf-8')

# Teksta šifrēšana ar CBC metodi
def encrypt_text_cbc(plain_text, key):
    block_size = AES.block_size
    # ģenerē inicializēšanas vektoru viena bloka garumā
    iv = get_random_bytes(block_size)
    # Papildina (pad) tekstu tā, lai tas būtu pilnā AES 16 baitu bloka garumā
    padded_text = pad(plain_text.encode(), block_size)
    cipher_text = b''
    print("Padded teksts:", padded_text)

    # Šifrēšana pa blokiem. Sāk ar iv bloku
    previous_block = iv
    for i in range(0, len(padded_text), block_size):
        current_block = padded_text[i:i + block_size]
        block_to_encrypt = xor_bytes(current_block, previous_block)
        encrypted_block = encrypt_block(block_to_encrypt, key)
        cipher_text += encrypted_block
        previous_block = encrypted_block
    
    return iv + cipher_text

# Teksta atšifrēšana ar CBC metodi pretējā virzienā
def decrypt_text_cbc(cipher_text_encoded, key):
    block_size = AES.block_size
    # Izdala inicializēšanas vektoru un ziņu no šifrētās un base64 iekodētās virknes
    iv = cipher_text_encoded[:block_size]
    cipher_text = cipher_text_encoded[block_size:]
    decrypted_text = b''

    previous_block = iv
    for i in range(0, len(cipher_text), block_size):
        current_block = cipher_text[i:i + block_size]
        decrypted_block = decrypt_block(current_block, key)
        decrypted_block = xor_bytes(decrypted_block, previous_block)
        decrypted_text += decrypted_block
        previous_block = current_block

    decrypted_text = unpad(decrypted_text)
    return decrypted_text.decode('utf-8')

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a file using AES in CFB or CBC mode with CMAC.')
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='Mode to operate in')
    parser.add_argument('chaining', choices=['cfb', 'cbc'], help='Chaining mode to use')
    parser.add_argument('input_file', help='Input file')
    parser.add_argument('key_file', help='Key file')
    parser.add_argument('output_file', help='Output file')
    args = parser.parse_args()

    with open(args.key_file, 'r') as f:
        hex_keys = f.read().strip()
        key = binascii.unhexlify(hex_keys[:32])
        mac_key = binascii.unhexlify(hex_keys[32:64]) if args.chaining == 'cfb' else None
        print("Šifrēšanas atslēga:", key)
        print("MAC atslēga:", mac_key)

    if args.mode == 'encrypt':
        with open(args.input_file, 'r') as f:
            plain_text = f.read()

        if args.chaining == 'cfb':
            encrypted_data = encrypt_text_cfb(plain_text, key, mac_key)
        else:  # CBC
            encrypted_data = encrypt_text_cbc(plain_text, key)

        with open(args.output_file, 'wb') as f:
            f.write(encrypted_data)

    elif args.mode == 'decrypt':
        with open(args.input_file, 'rb') as f:
            encrypted_data = f.read()

        if args.chaining == 'cfb':
            try:
                decrypted_text = decrypt_text_cfb(encrypted_data, key, mac_key)
            except ValueError as e:
                print(str(e))
                return
        else:  # CBC
            decrypted_text = decrypt_text_cbc(encrypted_data, key)

        with open(args.output_file, 'w') as f:
            f.write(decrypted_text)

if __name__ == '__main__':
    main()