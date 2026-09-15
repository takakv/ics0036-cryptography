import secrets

from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher


class Challenger:
    def __init__(self):
        self._key = secrets.token_bytes(16)
        self._challenge: None | tuple[bytes, bytes] = None
        self._b: None | int = None
        self._finished = False

    def encrypt(self, m: bytes) -> tuple[bytes, bytes]:
        """Encrypt the message using AES-CTR and return the ciphertext and nonce."""
        nonce = secrets.token_bytes(16)
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(nonce))

        encryptor = cipher.encryptor()
        ct = encryptor.update(m) + encryptor.finalize()

        return ct, nonce

    def _decrypt(self, ct: bytes, nonce: bytes) -> bytes:
        if len(nonce) != 16:
            raise ValueError("The nonce should be 16 bytes long")

        cipher = Cipher(algorithms.AES(self._key), modes.CTR(nonce))

        decryptor = cipher.decryptor()
        pt = decryptor.update(ct) + decryptor.finalize()

        return pt

    def decrypt(self, ct: bytes, nonce: bytes) -> bytes:
        """Decrypt the ciphertext using AES-CTR and return the decrypted message."""
        if self._challenge is not None:
            if ct == self._challenge[0] and nonce == self._challenge[1]:
                raise ValueError("The challenge may not be decrypted")

        return self._decrypt(ct, nonce)

    def request_challenge(self, m0: bytes, m1: bytes) -> tuple[bytes, bytes]:
        """Encrypt one of the two plaintexts and return the challenge ciphertext."""
        if self._challenge is not None:
            raise ValueError("The challenge may only be requested once")

        if len(m0) != len(m1):
            raise ValueError("Plaintexts must be of equal length")

        self._b = secrets.randbelow(2)
        ct, nonce = self.encrypt((m0, m1)[self._b])

        self._challenge = (ct, nonce)
        return ct, nonce

    def verify_guess(self, b: int) -> bool:
        """Verify the adversary's guess. Returns True when it is correct."""
        if self._challenge is None:
            raise ValueError("No challenge has been requested")

        if self._finished:
            raise ValueError("The guess may only be submitted once")

        self._finished = True
        return b == self._b
