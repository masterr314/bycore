import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_key(pass_phrase: str, salt: str) -> bytes:
    """
    https://nitratine.net/blog/post/encryption-and-decryption-in-python/
    """

    _pass_phrase = pass_phrase.encode()
    _salt = salt.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(_pass_phrase))  # kdf

    return key

