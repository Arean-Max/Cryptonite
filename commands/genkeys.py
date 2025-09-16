from getpass import getpass
from crypto_utils.keys import gen_keys

def cmd_genkeys(args):
    passphrase = None
    if args.protect:
        p = getpass('Enter passphrase for private key: ')
        p2 = getpass('Confirm passphrase: ')
        if p != p2:
            print('Passphrases do not match')
            return
        passphrase = p.encode('utf-8')

    gen_keys(args.priv, args.pub, bits=args.bits, passphrase=passphrase)
