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
        self._r = None
        self.pub = self._secret * self.curve.G

    def commit(self) -> Point:
        """Start a proof by committing to a fresh random value.

        :return: the commitment
        """
        self._r = ...
        return ...

    def respond(self, c: int) -> int:
        """Respond to the verifier's challenge.

        :param c: The challenge
        :return: the response
        """
        z = ...
        self._r = None
        return z

    def prove(self) -> Transcript:
        """Prove knowledge of the discrete logarithm of the public key.

        :return: the transcript
        """
        u = ...
        c = ...
        z = ...

        return Transcript(u, c, z)


def print_transcript(h: Point, tr: Transcript):
    print("h:", serialize_point(h).hex())
    print("u:", serialize_point(tr.u).hex())
    print("c:", f"{tr.c:x}")
    print("z:", f"{tr.z:x}")


def main():
    prover = Prover()

    print("Non-interactive proof:")
    print_transcript(prover.pub, prover.prove())
    print()

    print("Interactive proof:")
    print("h:", serialize_point(prover.pub).hex())
    print("u:", serialize_point(prover.commit()).hex())
    c = int(input("c: "), 16)
    print("z:", f"{prover.respond(c):x}")


if __name__ == "__main__":
    main()
