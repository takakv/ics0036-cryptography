import secrets

from cryptography.hazmat.primitives import hpke, serialization
from cryptography.hazmat.primitives.asymmetric import ec

SUITE = hpke.Suite(hpke.KEM.P384, hpke.KDF.HKDF_SHA384, hpke.AEAD.AES_128_GCM)
INFO = b"ICS0036"


class Channel:
    def __init__(self):
        self._sk_b = ec.generate_private_key(ec.SECP384R1())

        self._message = f"Meet me at {secrets.token_hex(8)}".encode()
        self._received: None | bytes = None

        self._step = 0
        self._finished = False

    def _advance(self, step: int, name: str):
        if self._step != step:
            raise ValueError(f"{name} may only be called once and in protocol order")
        self._step += 1

    def bob_public_key(self) -> bytes:
        """Return Bob's public key."""
        self._advance(0, "bob_public_key")
        return self._sk_b.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def alice_encrypt(self, pk: bytes) -> bytes:
        """Return Alice's ciphertext, encrypted to the given public key."""
        self._advance(1, "alice_encrypt")
        public_key = serialization.load_pem_public_key(pk)
        if not isinstance(public_key, ec.EllipticCurvePublicKey) \
                or not isinstance(public_key.curve, ec.SECP384R1):
            raise ValueError("Alice expects a P-384 public key")

        return SUITE.encrypt(self._message, public_key, info=INFO)

    def bob_receive(self, ct: bytes):
        """Deliver a ciphertext to Bob."""
        self._advance(2, "bob_receive")
        try:
            self._received = SUITE.decrypt(ct, self._sk_b, info=INFO)
        except Exception:
            raise ValueError("Bob could not decrypt the ciphertext") from None

    def verify(self, m: bytes) -> bool:
        if self._step != 3:
            raise ValueError("The protocol has not finished")

        if self._finished:
            raise ValueError("The result may only be verified once")

        self._finished = True
        return m == self._message and self._received == self._message
