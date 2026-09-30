import base64
from hashlib import sha256


def build_merkle_tree(leaves: list[bytes]) -> tuple[bytes, list[list[bytes]]]:
    intermediates = []
    current = leaves

    while len(current) > 1:
        pass

    # Exclude the root from the intermediates
    return current[0], intermediates[:-1]


def main():
    # NB! The hashes are computed without prepending 0x00 to the leaf data.
    # This must be taken into account when verifying membership.
    leaf_hashes = ["nLkU3/nPBhi/OZRR+b4rknyDWszFvCO1TEkRrbvO6ms=",
                   "pP+OvcT4nlZ36CZ9prYB4LIxgFqUHm+x+Lotn78mvOc=",
                   "cOdF38vZqJgJINeSnUqz7QAtxlcZOijFGvIqxIXLW1Q=",
                   "I6O6kkf6/7jA9P2i6Y0vRKhddV0rEQJunMkOppsmRDA=",
                   "GybMHxLyUz16PEXgC0Znr6cCjK9HSJS88S/pqUYhNuc=",
                   "V33lVhKtuEAmJGdzoJAa3+hJTentNAnV5F9Prbk5DkA="]

    leaves = [base64.b64decode(h) for h in leaf_hashes]
    root, intermediates = build_merkle_tree(leaves)

    print(leaves)
    print(intermediates)
    print(base64.b64encode(root).decode())

    data = b"A Link to the Past"
    print(base64.b64encode(sha256(data).digest()).decode())


if __name__ == "__main__":
    main()
