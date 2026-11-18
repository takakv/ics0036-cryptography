import secrets
from hashlib import sha384
from typing import NamedTuple

from fastecdsa.curve import P384
from fastecdsa.encoding.sec1 import SEC1Encoder
from fastecdsa.point import Point


class Transcript(NamedTuple):
    u: Point
    c: int
    z: int


def serialize_point(p: Point) -> bytes:
    return SEC1Encoder().encode_public_key(p, compressed=False)


def fiatshamir(h: Point, u: Point) -> int:
    """Compute the challenge as a hash of the statement and the commitment.

    :param h: The public key of the prover
    :param u: The commitment
    :return: the challenge
    """
    data = b""
    data += serialize_point(P384.G)
    data += serialize_point(h)
    data += serialize_point(u)

    return int.from_bytes(sha384(data).digest(), "big") % P384.q


# Please do not use this in production.
class Prover:
    def __init__(self):
        self.curve = P384
        self._secret = secrets.randbelow(self.curve.q)
        self.pub = self._secret * self.curve.G 

    def prove(self) -> Transcript:
        """Prove knowledge of the discrete logarithm of the public key.

        :return: the transcript
        """
        r = ...
        u = ...
        c = ...
        z = ...

        return Transcript(u, c, z)


def main():
    prover = Prover()
    proof = prover.prove()

    print("Public key:")
    print(prover.pub)
    print()

    print(proof)


if __name__ == "__main__":
    main()
