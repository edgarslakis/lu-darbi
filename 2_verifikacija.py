from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Ielādē sertifikātā .pem faila saturu certificate objektā
with open("certificate.pem", "rb") as f:
    cert_pem = f.read()
certificate = x509.load_pem_x509_certificate(cert_pem, default_backend())

# Pārbauda, vai saknes sertifikāta izdevēja un parakstītāja vārds saskan (ir identisks).
issuer = certificate.issuer
subject = certificate.subject
if issuer != subject:
    raise ValueError("Sertifikāta izdevējs un parakstītājs nesaskan. Šis nav derīgs saknes sertifikāts")
print("Sertifikāta izdevējs un parakstītājs sakrīt!")

# Sertifikāta verifikācija 
public_key = certificate.public_key() # paņem publisko atslēgu no sertifikāta
signature = certificate.signature
tbs_certificate_bytes = certificate.tbs_certificate_bytes # paņem parakstāmos (to-be-signed) baitus no sertifikāta

# Mēģina verificēt parakstu ar publisko atslēgu. 
try:
    public_key.verify( # (signature: baitos, data: baitos, padding: AsymmetricPadding, algorithm: HashAlgorithm)
        signature,
        tbs_certificate_bytes,
        padding.PKCS1v15(),
        hashes.SHA3_256()
    )
    print("Sertifikāta paraksts ir verificēts")
except Exception as e:
    raise ValueError(f"Sertifikāta paraksts nav derīgs, jo {e}")
