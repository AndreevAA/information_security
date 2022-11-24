import argparse
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pss


def sign(data):
    # получаем на основе данных хеш с помощью SHA256
    hash = SHA256.new(data)

    # генерируем открытый и закрытый ключ на основе RSA
    # The FIPS standard only defines 1024 (это минимум), 2048 and 3072.
    key = RSA.generate(2048)

    # отправляем в функцию шифрования (алгоритм PSS) закрытый ключ
    cipher = pss.new(key)
    private_key_file = open('key.pem', 'wb')
    # записываю ключ в файл key.pem
    private_key_file.write(key.exportKey('PEM'))
    private_key_file.close()

    public_key = key.publickey()
    public_key_file = open('pub.pem', 'wb')
    # Записываю открытый сгенерированный в generate ключ
    public_key_file.write(public_key.exportKey('PEM'))
    public_key_file.close()

    # отправляем в функцию шифрования (алгоритм PSS) хеш c помощью sha256 на основе data
    crypted_digest = cipher.sign(hash)
    
    sign_file = open(args.filename+'.sign', 'wb')
    # записываю в файл зашифрованный дайджест 
    sign_file.write(crypted_digest)
    sign_file.close()


def check(data, public_key=None):
    assert public_key
    # получаем на основе данных хеш с помощью SHA256
    hash = SHA256.new(data)
    public_key_file = open(public_key, 'rb')
    key = RSA.import_key(public_key_file.read())

    cipher = pss.new(key)

    try:
        signature = open(args.filename+".sign", "rb").read()
        # сравниваем два хеша
        с(hash, signature)
        print("OK")

    except (ValueError, TypeError):
        print("Error!")


parser = argparse.ArgumentParser(description='Check digital signs of files')
parser.add_argument('--sign', dest='sign', action='store_const', const=sign,
                    help='Check specified file instead of signing it,'
                                       ' public key specification is required!')
parser.add_argument('filename', metavar='filename', type=str,
                    help='a file to sign')
parser.add_argument('--verify', dest='check', action='store_const', const=check,
                    help='Check specified file instead of signing it,'
                                       ' public key specification is required!')
parser.add_argument('--public_key', metavar='public_key', type=str,
                    help='a private key for sign')



if __name__ == '__main__':
    args = parser.parse_args()
    # использую sing как аргумент
    if args.sign is not None:
        with open(args.filename, 'rb') as input_file:
            data = input_file.read()
            result = args.sign(data)
    # использую verify как аргумент
    if args.check is not None:
        with open(args.filename, 'rb') as input_file:
            data = input_file.read()
            result = args.check(data, args.public_key)