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
        self.pub = ...

    def encrypt(self, m: Point) -> Ciphertext:
        # The ephemeral random value is also a scalar.
        r = ...

        u = ...
        v = ...
        return Ciphertext(u, v)

    def lifted_encrypt(self, m: int) -> Ciphertext:
        lifted = ...
        return self.encrypt(lifted)

    def decrypt(self, ct: Ciphertext) -> Point:
        return ...

    def lifted_decrypt(self, ct: Ciphertext, candidates: list[int]) -> int | None:
        dec = self.decrypt(ct)
        for m in candidates:
            if m * self.curve.G == dec:
                return m

        return None


def main():
    eg = ElGamal()

    recovered = eg.lifted_decrypt(..., [])

    if recovered is None:
        print("[-] Failed to decrypt message")
        return

    print("[+] Decrypted:", recovered)


if __name__ == "__main__":
    main()
