import hashlib
import secrets

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from ecdsa import SigningKey
from ecdsa.util import sigencode_der


def main():
    private_key = ec.generate_private_key(ec.SECP384R1())
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open("p384.key.pem", "wb") as f:
        f.write(private_pem)

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("p384.pub.pem", "wb") as f:
        f.write(public_pem)

    m1 = b"This is message 1"
    m2 = b"This is message 2"

    with open("m1.bin", "wb") as f:
        f.write(m1)

    with open("m2.bin", "wb") as f:
        f.write(m2)

    sk = SigningKey.from_pem(private_pem.decode("ascii"))

    rand_len = sk.curve.generator.order().bit_length()
    k = secrets.randbits(rand_len)

    sig1 = sk.sign(m1, hashfunc=hashlib.sha384, sigencode=sigencode_der, k=k)
    sig2 = sk.sign(m2, hashfunc=hashlib.sha384, sigencode=sigencode_der, k=k)

    with open("m1.sig", "wb") as f:
        f.write(sig1)

    with open("m2.sig", "wb") as f:
        f.write(sig2)


if __name__ == "__main__":
    main()
