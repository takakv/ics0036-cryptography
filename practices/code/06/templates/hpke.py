import secrets  # noqa: F401

from cryptography.hazmat.primitives import hashes, hpke
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # noqa: F401
from cryptography.hazmat.primitives.kdf.hkdf import HKDF, HKDFExpand
from fastecdsa.curve import P384
from fastecdsa.encoding.sec1 import SEC1Encoder
from fastecdsa.point import Point

KEM_ID = 0x0011  # DHKEM(P-384, HKDF-SHA384)
KDF_ID = 0x0002  # HKDF-SHA384
AEAD_ID = 0x0001  # AES-128-GCM

KEM_SUITE_ID = b"KEM" + KEM_ID.to_bytes(2, "big")
HPKE_SUITE_ID = (b"HPKE" + KEM_ID.to_bytes(2, "big")
                 + KDF_ID.to_bytes(2, "big") + AEAD_ID.to_bytes(2, "big"))

N_SECRET = 48  # length of the KEM shared secret
N_K = 16  # length of the AEAD key
N_N = 12  # length of the AEAD nonce

MODE_BASE = 0x00


def labeled_extract(suite_id: bytes, salt: bytes, label: bytes, ikm: bytes) -> bytes:
    return HKDF.extract(hashes.SHA384(), salt or None, b"HPKE-v1" + suite_id + label + ikm)


def labeled_expand(suite_id: bytes, prk: bytes, label: bytes, info: bytes, length: int) -> bytes:
    labeled_info = length.to_bytes(2, "big") + b"HPKE-v1" + suite_id + label + info
    return HKDFExpand(hashes.SHA384(), length, labeled_info).derive(prk)


def serialize_point(p: Point) -> bytes:
    """Encode a point in the uncompressed SEC1 format (0x04 || x || y)."""
    return SEC1Encoder().encode_public_key(p, compressed=False)


def dh_bytes(s: Point) -> bytes:
    """Encode the DH output: only the x-coordinate of the shared point is used."""
    return s.x.to_bytes(48, "big")


def extract_and_expand(dh: bytes, kem_context: bytes) -> bytes:
    """Derive the KEM shared secret from the DH output (RFC 9180, section 4.1)."""
    eae_prk = labeled_extract(KEM_SUITE_ID, b"", b"eae_prk", dh)
    return labeled_expand(KEM_SUITE_ID, eae_prk, b"shared_secret", kem_context, N_SECRET)


def key_schedule(shared_secret: bytes, info: bytes) -> tuple[bytes, bytes]:
    """Derive the AEAD key and base nonce in base mode (RFC 9180, section 5.1)."""
    psk_id_hash = labeled_extract(HPKE_SUITE_ID, b"", b"psk_id_hash", b"")
    info_hash = labeled_extract(HPKE_SUITE_ID, b"", b"info_hash", info)
    context = bytes([MODE_BASE]) + psk_id_hash + info_hash

    secret = labeled_extract(HPKE_SUITE_ID, shared_secret, b"secret", b"")
    key = labeled_expand(HPKE_SUITE_ID, secret, b"key", context, N_K)
    base_nonce = labeled_expand(HPKE_SUITE_ID, secret, b"base_nonce", context, N_N)
    return key, base_nonce


# Please don't use this in production, it's for learning only.
def encrypt(pk_b: Point, info: bytes, m: bytes) -> bytes:
    """Encrypt a message with HPKE in base mode.

    :param pk_b: The recipient's public key K_B
    :param info: The application context
    :param m: The message to encrypt
    :return: the encapsulation R concatenated with the ciphertext c
    """
    # Step 1: R = rG
    # TODO: sample r uniformly from Z_n^* and compute the encapsulation R
    r = ...
    R = ...

    # Step 2: S = rK_B
    # TODO: compute the shared DH point
    S = ...

    # Step 3: s = KDF(S, R || K_B)
    # TODO: build the KEM context and derive the shared secret with extract_and_expand
    kem_context = ...
    s = ...

    # Step 4: k, nonce = KDF(s, info)
    # TODO: derive the AEAD key and nonce with key_schedule
    k, nonce = ...

    # Step 5: c = ENC_k(nonce, aad, m)
    # TODO: encrypt with AES-128-GCM (use an empty AAD)
    c = ...

    # Step 6: output R || c
    # TODO: return the serialized encapsulation followed by the ciphertext
    return ...


def main():
    info = b"ICS0036 week 6"
    message = "It's dangerous to go alone! Take this. 🗡️".encode("utf-8")

    # The recipient's keypair.
    sk_b = ec.generate_private_key(ec.SECP384R1())
    numbers = sk_b.public_key().public_numbers()
    pk_b = Point(numbers.x, numbers.y, curve=P384)

    ct = encrypt(pk_b, info, message)
    print("Ciphertext:", ct.hex())

    # We check the result against a known implementation.
    suite = hpke.Suite(hpke.KEM.P384, hpke.KDF.HKDF_SHA384, hpke.AEAD.AES_128_GCM)
    pt = suite.decrypt(ct, sk_b, info=info)
    print("Decrypted :", pt.decode("utf-8"))


if __name__ == "__main__":
    main()
