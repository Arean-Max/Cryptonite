from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def gen_keys(priv_path: str, pub_path: str, bits: int = 4096, passphrase: bytes | None = None):
    if bits < 2048:
        raise ValueError('RSA key size must be >= 2048 bits')

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits, backend=default_backend())

    if passphrase:
        encryption = serialization.BestAvailableEncryption(passphrase)
    else:
        encryption = serialization.NoEncryption()

    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption,
    )
    pub_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    Path(priv_path).write_bytes(priv_pem)
    Path(pub_path).write_bytes(pub_pem)
    print(f'Keys written: {priv_path}, {pub_path} (bits={bits})')

def load_public_key(path: str):
    data = Path(path).read_bytes()
    return serialization.load_pem_public_key(data, backend=default_backend())

def load_private_key(path: str, passphrase: bytes | None = None):
    data = Path(path).read_bytes()
    return serialization.load_pem_private_key(data, password=passphrase, backend=default_backend())
