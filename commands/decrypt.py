import json, sys
from pathlib import Path
from getpass import getpass
from cryptography.hazmat.primitives import serialization
from crypto_utils.utils import detect_debugger
from crypto_utils.keys import load_private_key
from crypto_utils.crypto import decrypt_blob

def cmd_decrypt(args):
    if detect_debugger():
        print('Debugger detected — decrypt operation is blocked for security.')
        return

    passphrase = None
    if args.protect:
        p = getpass('Enter passphrase for private key: ')
        passphrase = p.encode('utf-8')

    try:
        priv = load_private_key(args.priv, passphrase=passphrase)
    except FileNotFoundError:
        print(f'Private key not found: {args.priv}')
        choice = input('Enter private key manually? (y/N): ').strip().lower()
        if choice != 'y':
            return
        print('Paste PEM (end with a single line containing END):')
        lines = []
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            if line.strip() == 'END':
                break
            lines.append(line)
        pem_data = ''.join(lines).encode('utf-8')
        priv = serialization.load_pem_private_key(pem_data, password=passphrase, backend=None)

    blob = json.loads(Path(args.infile).read_text(encoding='utf-8'))

    try:
        plaintext = decrypt_blob(blob, priv)
    except Exception as e:
        print('Decryption failed:', e)
        return

    if args.out:
        Path(args.out).write_bytes(plaintext)
        print(f'Decrypted data written to: {args.out}')
    else:
        try:
            print(plaintext.decode('utf-8'))
        except Exception:
            sys.stdout.buffer.write(plaintext)
