import argparse

from pyasn1.codec.der import encoder
from pyasn1.type.namedtype import NamedTypes, NamedType
from pyasn1.type.univ import Sequence, Integer


class ECDSASignature(Sequence):
    componentType = NamedTypes(
        NamedType("r", Integer()),
        NamedType("s", Integer()),
    )


def main(infile: str, outfile: str):
    with open(infile, "rb") as f:
        data = f.read()

    assert len(data) == 96
    r = int.from_bytes(data[:48], "big")
    s = int.from_bytes(data[48:], "big")

    sig = ECDSASignature()
    sig["r"] = r
    sig["s"] = s

    with open(outfile, "wb") as f:
        f.write(encoder.encode(sig))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="infile", help="the raw signature file")
    parser.add_argument(dest="outfile", help="the well-formed signature file")

    args = parser.parse_args()
    main(args.infile, args.outfile)
