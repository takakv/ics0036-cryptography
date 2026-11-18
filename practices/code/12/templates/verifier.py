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


def verify_interactive(h: Point, tr: Transcript) -> bool:
    """Verify a transcript of the interactive protocol.

    :param h: The public key of the prover
    :param tr: The transcript
    :return: whether the transcript is accepting
    """
    ...


def verify_fiatshamir(h: Point, tr: Transcript) -> bool:
    """Verify a non-interactive proof of knowledge of the discrete logarithm of h.

    :param h: The public key of the prover
    :param tr: The transcript
    :return: whether the proof is valid
    """
    ...


def simulate(h: Point) -> Transcript:
    """Simulate an accepting transcript without knowing the discrete logarithm of h.

    :param h: The public key of the prover
    :return: the simulated transcript
    """
    c = ...
    z = ...
    u = ...

    return Transcript(u, c, z)


def main():
    pub = Point(
        0xab3b7b9b705eb1cfb24d62fcbffbded4b9853ab2b1b87c2655531d4ad7f9b5d98fbc0994c1dcb977a0fe5b194fac0922,
        0x12c52aaae454361469d1c654191c895612785142b93bdfb4b265d50a2c978e8602ee3024b43729de9097dec799f6f343,
        curve=P384,
    )
    tr = Transcript(
        Point(
            0xdfb14dbff8dfbf253fadca531d52d72df7483b7b22d626eec4c3adfd6708a3da0a41d6a634efc4e8fb9c63ac7b8b3dad,
            0xe2525ed8dcc94a3abebe2e39569c8801951c11541a52e4fef1109462c7de5eb312b7aee34cb3b745341347130ef4228a,
            curve=P384,
        ),
        0xa0763e1b5427a16e2d145d8ff1042ddf12856d7286830f7b9002aa5098fd0a53010313dc49269b9ee0dd122a455b1448,
        0x7d244bf077a3fbc78b310d5631bd766a433e0a74a1618b99d7d4e4d4ddb75bb99abb14b44a6a595efa739c90a34b9d96,
    )

    if not verify_fiatshamir(pub, tr):
        print("[-] Invalid proof")
        return

    print("[+] Proof verified")

    sim = simulate(pub)

    if not verify_interactive(pub, sim):
        print("[-] Simulated transcript rejected by the interactive verifier")
        return

    if verify_fiatshamir(pub, sim):
        print("[-] Simulated transcript accepted by the Fiat-Shamir verifier")
        return

    print("[+] Simulated transcript accepted by the interactive verifier only")


if __name__ == "__main__":
    main()
