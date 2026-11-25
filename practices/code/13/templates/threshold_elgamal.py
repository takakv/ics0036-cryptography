import secrets
from typing import NamedTuple

from fastecdsa.curve import P384
from fastecdsa.point import Point

G = P384.G
q = P384.q


class Ciphertext(NamedTuple):
    u: Point
    v: Point


def encode_message(msg: bytes) -> Point:
    """Embed a short message into the x-coordinate of a point.

    :param msg: The message, at most 46 bytes
    :return: the point encoding the message
    """
    if len(msg) > 46:
        raise ValueError("Message too long")

    p = P384.p
    for counter in range(256):
        x = int.from_bytes(msg + bytes([counter]), "big")
        y2 = (x ** 3 + P384.a * x + P384.b) % p
        y = pow(y2, (p + 1) // 4, p)
        if y * y % p == y2:
            return Point(x, y, curve=P384)
    raise ValueError("Message cannot be encoded")


def decode_message(m: Point) -> bytes:
    x = m.x >> 8
    return x.to_bytes((x.bit_length() + 7) // 8, "big")


# Please do not use this in production.
class Party:
    def __init__(self, i: int, t: int):
        self.i = i
        self._coeffs = [secrets.randbelow(q) for _ in range(t)]
        self._share = 0
        self.pub = self._coeffs[0] * G

    def share_for(self, j: int) -> int:
        """Evaluate this party's secret polynomial at j.

        :param j: The index of the receiving party
        :return: the share for party j
        """
        s = 0
        for a in reversed(self._coeffs):
            s = (s * j + a) % q
        return s

    def receive(self, s: int):
        """Add a share received from another party to the secret key share.

        :param s: The received share
        """
        self._share = (self._share + s) % q

    def decryption_share(self, u: Point) -> Point:
        """Compute the decryption share d_i for a ciphertext.

        :param u: The first component of the ciphertext
        :return: the decryption share
        """
        return ...


def encrypt(h: Point, m: Point) -> Ciphertext:
    """Encrypt a message under the combined public key.

    :param h: The combined public key
    :param m: The message encoded as a point
    :return: the ciphertext
    """
    r = ...
    return Ciphertext(..., ...)


def lagrange(i: int, indices: list[int]) -> int:
    """Compute the Lagrange coefficient of party i at 0.

    :param i: The index of the party
    :param indices: The indices of all parties taking part in decryption
    :return: the Lagrange coefficient L(i)
    """
    ...


def combine(ct: Ciphertext, shares: dict[int, Point]) -> Point:
    """Recover the message from at least t decryption shares.

    :param ct: The ciphertext
    :param shares: The decryption shares, indexed by party
    :return: the message encoded as a point
    """
    ...


def main():
    t = 3
    n = 5

    parties = [Party(i, t) for i in range(1, n + 1)]
    for sender in parties:
        for receiver in parties:
            receiver.receive(sender.share_for(receiver.i))

    h = 0 * G
    for party in parties:
        h += party.pub

    msg = b"Blablabla"
    ct = encrypt(h, encode_message(msg))
    dshares = {party.i: party.decryption_share(ct.u) for party in parties[:t]}

    print("Decrypted message:", decode_message(combine(ct, dshares)))


if __name__ == "__main__":
    main()
