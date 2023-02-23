import hashlib


def encrypt_password(password: str) -> str:
    c = hashlib.blake2b()
    c.update(password.encode())
    return c.hexdigest()


def verify_password(password: str, hash_pass: str) -> bool:
    test = encrypt_password(password)
    return encrypt_password(password) == hash_pass
