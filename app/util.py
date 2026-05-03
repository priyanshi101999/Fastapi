import hashlib

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash(password: str):
    # hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password_hash.hash(password)

def verify(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

