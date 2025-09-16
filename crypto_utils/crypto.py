import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from crypto_utils.utils import b64, ub64, wipe_bytes

def encrypt_bytes(plaintext: bytes, public_key) -> dict:
    aes_key = bytearray(AESGCM.generate_key(bit_length=256))
    try:
        aesgcm = AESGCM(bytes(aes_key))
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

        encrypted_key = public_key.encrypt(
            bytes(aes_key),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
        )

        return {
            'encrypted_key': b64(encrypted_key),
            'nonce': b64(nonce),
            'ciphertext': b64(ciphertext),
            'schema': 'RSA-OAEP-SHA256+AES-256-GCM',
        }
    finally:
        try:
            wipe_bytes(aes_key)
        except Exception:
            pass

def decrypt_blob(blob: dict, private_key) -> bytes:
    encrypted_key = ub64(blob['encrypted_key'])
    nonce = ub64(blob['nonce'])
    ciphertext = ub64(blob['ciphertext'])

    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

    aes_ba = bytearray(aes_key)
    try:
        aesgcm = AESGCM(bytes(aes_ba))
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
        return plaintext
    finally:
        try:
            wipe_bytes(aes_ba)
        except Exception:
            pass
