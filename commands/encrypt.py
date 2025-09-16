import json
from pathlib import Path
from crypto_utils.utils import detect_debugger
from crypto_utils.keys import load_public_key
from crypto_utils.crypto import encrypt_bytes

def cmd_encrypt(args):
    if detect_debugger():
        print('Debugger detected — encrypt operation is blocked for security.')
        return

    pub = load_public_key(args.pub)

    if args.text is not None:
        plaintext = args.text.encode('utf-8')
    else:
        plaintext = Path(args.infile).read_bytes()

    blob = encrypt_bytes(plaintext, pub)

    out_path = args.out
    Path(out_path).write_text(json.dumps(blob, ensure_ascii=False), encoding='utf-8')
    print(f'Encrypted output written to: {out_path}')
