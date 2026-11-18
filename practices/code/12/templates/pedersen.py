import secrets
from hashlib import sha384

from fastecdsa.curve import P384
from fastecdsa.encoding.sec1 import SEC1Encoder
from fastecdsa.point import Point


def hash_to_point(seed: bytes) -> Point:
    """Derive a point whose discrete logarithm w.r.t. G is not known to anyone.

    :param seed: The public seed
    :return: the derived point
    """
    p = P384.p
    counter = 0
    while True:
        x = int.from_bytes(sha384(seed + counter.to_bytes(4, "big")).digest(), "big") % p
        y2 = (x ** 3 + P384.a * x + P384.b) % p
        y = pow(y2, (p + 1) // 4, p)
        if y * y % p == y2:
            return Point(x, y, curve=P384)
        counter += 1


G = P384.G
H = hash_to_point(b"ICS0036 Pedersen H")


def serialize_point(p: Point) -> bytes:
    return SEC1Encoder().encode_public_key(p, compressed=False)


def deserialize_point(octets: bytes) -> Point:
    return SEC1Encoder().decode_public_key(octets, P384)


def commit(m: int) -> tuple[Point, int]:
    """Commit to a message.

    :param m: The message to commit to
    :return: the commitment and the randomness needed to open it
    """
    r = ...
    c = ...
    return c, r


def verify(c: Point, m: int, r: int) -> bool:
    """Check whether (m, r) opens the commitment.

    :param c: The commitment
    :param m: The claimed message
    :param r: The claimed randomness
    :return: whether the opening is valid
    """
    return ...


def load_test_vectors(path: str) -> list[dict[str, str]]:
    with open(path) as f:
        blocks = f.read().strip().split("\n\n")

    return [dict(line.split(" = ") for line in block.splitlines()) for block in blocks]


def main():
    m1 = 7
    m2 = 35

    c1, r1 = commit(m1)
    c2, r2 = commit(m2)

    assert verify(c1, m1, r1)
    assert not verify(c1, m2, r1)

    assert verify(c1 + c2, m1 + m2, r1 + r2)

    for i, tv in enumerate(load_test_vectors("pedersen.txt")):
        c = deserialize_point(bytes.fromhex(tv["c"]))
        expected = tv["valid"] == "true"
        if verify(c, int(tv["m"]), int(tv["r"], 16)) != expected:
            print("[-] Test vector", i, "failed")
            return

    print("[+] All tests passed")


if __name__ == "__main__":
    main()
