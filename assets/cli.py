import argparse
from commands.genkeys import cmd_genkeys
from commands.encrypt import cmd_encrypt
from commands.decrypt import cmd_decrypt

def main():
    help_text = """\
1) Install dependency:
   Command:
     pip install cryptography

   Purpose:
     Installs the cryptography library used for RSA and AES-GCM operations.
     Use a virtual environment (venv) or conda.

2) Generate keys (recommended 4096 bits, minimum 2048 bits):
   Example:
     python main.py genkeys --bits 4096 --protect

   Details:
     --bits <n>           — RSA key size in bits (>=2048). 4096 recommended.
     --protect            — prompts for a passphrase and encrypts the private key PEM.
     --priv, --pub        — default filenames: private_key.pem, public_key.pem.
                          You can override them.

   Recommendations:
     - Keep the private key in a secure location and set tight file permissions (chmod 600).
     - Use a secrets manager if automating key handling.

3) Encrypt text:
   Example:
     python main.py encrypt --text "Akin Foundation" --pub public_key.pem --out message.enc

   Details:
     --text "..."         — text to encrypt.
     --pub <path>         — public key PEM file.
     --out <file>         — output JSON file (default message.enc).

4) Encrypt file:
   Example:
     python main.py encrypt --in secret.bin --pub public_key.pem --out message.enc

   Details:
     --in <file>          — input file read as binary.

5) Decrypt:
   Example:
     python main.py decrypt --in message.enc --priv private_key.pem --protect --out decrypted.bin

   Details:
     --in <file>          — input JSON.
     --priv <path>        — private key PEM.
     --protect            — if private key is encrypted, prompts for passphrase.
     --out <file>         — optional output path. If omitted, plaintext is printed
                           (binary safe).

   Missing private key:
     - The program offers to paste PEM into the console. End manual input with:
         END
"""

    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Secure E2E encryptor (RSA-OAEP + AES-256-GCM)"
    )
    parser.add_argument(
        "--use",
        action="store_true",
        help="Show usage examples and security notes"
    )

    sub = parser.add_subparsers(dest='cmd')

    p_gen = sub.add_parser('genkeys', help='Generate RSA keypair')
    p_gen.add_argument('--priv', default='private_key.pem')
    p_gen.add_argument('--pub', default='public_key.pem')
    p_gen.add_argument('--bits', type=int, default=4096, help='RSA key size in bits (>=2048)')
    p_gen.add_argument('--protect', action='store_true', help='Protect private key with passphrase')
    p_gen.set_defaults(func=cmd_genkeys)

    p_enc = sub.add_parser('encrypt', help='Encrypt text or file')
    p_enc.add_argument('--pub', default='public_key.pem')
    group = p_enc.add_mutually_exclusive_group(required=True)
    group.add_argument('--text', help='Text to encrypt')
    group.add_argument('--in', dest='infile', help='Input file to encrypt')
    p_enc.add_argument('--out', default='message.enc', help='Output file (JSON)')
    p_enc.set_defaults(func=cmd_encrypt)

    p_dec = sub.add_parser('decrypt', help='Decrypt file')
    p_dec.add_argument('--priv', default='private_key.pem')
    p_dec.add_argument('--in', dest='infile', required=True)
    p_dec.add_argument('--out', help='File for decrypted output (optional)')
    p_dec.add_argument('--protect', action='store_true', help='Passphrase protected private key')
    p_dec.set_defaults(func=cmd_decrypt)

    args = parser.parse_args()

    if args.use:
        print(help_text)
        return

    if not hasattr(args, 'func') or args.func is None:
        parser.print_help()
        return

    args.func(args)
