import secrets
from typing import NamedTuple

from fastecdsa.curve import P384
from fastecdsa.point import Point


class Ciphertext(NamedTuple):
    u: Point
    v: Point


class ElGamal:
    def __init__(self):
        self.curve = P384
        # q denotes the number of elements in the group and scalars
        # thus belong to [0, ..., q - 1].
        # Since the group is cyclic, qG = 0G, (q+1)G = 1G and so on.
        self._secret = secrets.randbelow(self.curve.q)
        # G is a ‘standard’ generator of the group, sometimes called the base point.
        self.pub = self._secret * self.curve.G

    def encrypt(self, m: Point) -> Ciphertext:
        # The ephemeral random value is also a scalar.
        r = secrets.randbelow(self.curve.q)

        u = r * self.curve.G  # g^r in multiplicative notation
        v = m + (r * self.pub)  # m * h^r in multiplicative notation
        return Ciphertext(u, v)

    def lifted_encrypt(self, m: int) -> Ciphertext:
        lifted = m * self.curve.G
        return self.encrypt(lifted)

    def decrypt(self, ct: Ciphertext) -> Point:
        return ct.v - self._secret * ct.u  # v * u^{-x} in multiplicative notation

    def lifted_decrypt(self, ct: Ciphertext, candidates: list[int]) -> int | None:
        dec = self.decrypt(ct)
        for m in candidates:
            if m * self.curve.G == dec:
                return m

        return None


def main():
    m1 = 1
    m2 = 5

    eg = ElGamal()

    ct1 = eg.lifted_encrypt(m1)
    ct2 = eg.lifted_encrypt(m2)

    ct3 = Ciphertext(ct1.u + ct2.u, ct1.v + ct2.v)

    recovered = eg.lifted_decrypt(ct3, [m1, m2, m1 + m2])

    if recovered is None:
        print("[-] Failed to decrypt message")
        return

    print("[+] Decrypted:", recovered)


if __name__ == "__main__":
    main()
