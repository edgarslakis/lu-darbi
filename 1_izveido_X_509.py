from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from datetime import datetime, timedelta

# Sertifikāta informāciju nolasa no faila informacija.txt
info = {}
with open('informacija.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        info[key] = value

# Ģenerē RSA privāto atslēgu ar Cryptography bibliotēkas funkciju, norādot atslēgas izmēru
private_key = rsa.generate_private_key(
    public_exponent=3, # vai pemēģināt ar pirmskaitļiem 17 vai, piemēram, 65537
    key_size=2048,
)

# Ievieto sertifikātā izdevēja informāciju, kura nolasīta no infromacija.txt augstāk
name = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, info['Valsts']),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, info['Novads']),
    x509.NameAttribute(NameOID.LOCALITY_NAME, info['Pilseta']),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, info['Organizacija']),
    x509.NameAttribute(NameOID.COMMON_NAME, info['Vards']),
])

# Izveido sertifikātu norādot, ka tas ir Certificate Authority (ca=True pie BasicConstraints)
certificate = x509.CertificateBuilder().subject_name(
    name
).issuer_name(
    name #pašparakstītā sertifikātā izdevējs un parakstītājs ir viens un tas pats.
).public_key(
    private_key.public_key() #izveido publisko atslēgu no privātās atslēgas
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.now()
).not_valid_after(
    datetime.now() + timedelta(days=30)  # Derīgs 30 dienas
).add_extension(
    x509.BasicConstraints(ca=True, path_length=None),
    critical=True,
).sign(private_key, hashes.SHA3_256()) #paraksta sertifikātu izmantojot privāto atslēgu un SHA-3 hash algoritmu 

# Privāto atslēgu saglabā mašīnlasāmā .PEM failā
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption()
    ))

# Sertifikātu saglabā mašīnlasāmā .PEM failā
with open("certificate.pem", "wb") as f:
    f.write(certificate.public_bytes(Encoding.PEM))

print("Saknes sertifikāts ir izveidots")
