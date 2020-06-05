from base64 import b64encode
from hashlib import sha256

import bcrypt


def hashpw(password: str) -> str:
    if isinstance(password, str):
        password = password.encode()
    return bcrypt.hashpw(
        b64encode(sha256(password).digest()),
        bcrypt.gensalt()
    ).decode()


def checkpw(password: str, hashed: str) -> str:
    if isinstance(password, str):
        password = password.encode()
    if isinstance(hashed, str):
        hashed = hashed.encode()
    return bcrypt.checkpw(
        b64encode(sha256(password).digest()),
        hashed
    )
