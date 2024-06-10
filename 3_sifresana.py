from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Ielasa sertifikātu no .PEM faila
with open("certificate.pem", "rb") as f:
    cert_pem = f.read()
certificate = x509.load_pem_x509_certificate(cert_pem, default_backend())

# Paņem publisko atslēgu no sertifikāta
public_key = certificate.public_key()

# Paņem privāto atslēgu no .PEM faila
with open("private_key.pem", "rb") as f:
    private_key_pem = f.read()

private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())

# Šifrējamā ziņa
message = b"Testa zinojums"

# Šifrē ziņu ar RSA publisko atslēgu, izmantojot bibliotēkā pieejamu Optimal Asymmetric Encryption Padding (OAEP) funkciju. 
def encrypt_message(public_key, message):
    encrypted_message = public_key.encrypt(
        message,
        # Šoreiz šifrējamam tekstam pievieno random simbolus un padding, lai identiski teksti nedotu vienādu šifrējumu. 
        # Tas pasargā no Chosen Plaintext Attacks. 
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), # MFG (mask generation function) ģenerē random simbolus pēc SHA-256 algoritma
            algorithm=hashes.SHA256(), #SHA-256 algoritms izvada 32 baitu virkni un OAEP pievieno vēl 2 baitus.
            label=None
        )
    )
    return encrypted_message

# Atšifrē ziņu, izmantojot RSA privāto atslēgu un OAEP
def decrypt_message(private_key, encrypted_message):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message

# Ielasa šifrējamo ziņu no faila un to šifrē
with open("input.bin", "rb") as f:
    plaintext_message = f.read()

# Pārbauda, vai faila izmērs nepārsniedz RSA pieļaujamo ar 2048 bitu atslēgu
key_size = public_key.key_size // 8  # in bytes
padding_size = 2 * hashes.SHA256().digest_size + 2
max_message_size = key_size - padding_size
if len(plaintext_message) > max_message_size:
    raise ValueError(f"Teksta izmērs ir par lielu, lai to šifrētu ar pašreizējo RSA atslēgas garumu. Maksimālais pieļaujamais garums {max_message_size} baiti.")

encrypted_message = encrypt_message(public_key, plaintext_message)

# Saglabā šifrēto failu
with open("encrypted_message.bin", "wb") as f:
    f.write(encrypted_message)

# Ielasa šifrētu ziņu no faila un to atšifrē
with open("encrypted_message.bin", "rb") as f:
    encrypted_message = f.read()
decrypted_message = decrypt_message(private_key, encrypted_message)

# Saglabā atšifrēto failu
with open("output.bin", "wb") as f:
    f.write(decrypted_message)
    print("Šifrēšana+atšifrēšana pabeigta. Atšifrētais fails: output.bin")