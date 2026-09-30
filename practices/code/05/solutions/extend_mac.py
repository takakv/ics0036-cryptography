import hmac
import secrets
from hashlib import sha256

import hlextend

KEY = secrets.token_bytes(16)


def verify(message: bytes, tag: bytes) -> bool:
    verif = sha256(KEY + message).digest()
    return hmac.compare_digest(verif, tag)


def authenticate(message: bytes) -> bytes:
    return sha256(KEY + message).digest()


def main():
    message = b"Length extension"
    tag = authenticate(message)

    # No knowledge of the key starting from now.

    hasher = hlextend.new('sha256')
    # The secret length of 16 bytes is known to us.
    extended_message = hasher.extend(b"Forgery!", message, 16, tag.hex())

    forged_tag = bytes.fromhex(hasher.hexdigest())

    print("Extended message:", extended_message)
    print("Forged tag:", hasher.hexdigest())

    # External verifier with knowledge of the key.

    print("Forged tag verifies:", verify(extended_message, forged_tag))


if __name__ == "__main__":
    main()
