import base64
from hashlib import sha256

games = ["Majora's Mask", "Spirit Tracks",
         "A Link to the Past", "Breath of the Wild",
         "Ocarina of Time", "The Wind Waker"]


def get_leaf_hash(data: bytes) -> bytes:
    return sha256(b"\x00" + data).digest()


def get_internal_hash(left: bytes, right: bytes) -> bytes:
    return sha256(b"\x01" + left + right).digest()


def get_parent_row(nodes: list[bytes]) -> list[bytes]:
    row = []
    for i in range(0, len(nodes), 2):
        sibling = nodes[i + 1] if i + 1 < len(nodes) else None
        if sibling is None:
            # If the row has an odd number of elements,
            # the last node becomes its own parent.
            row.append(nodes[i])
        else:
            row.append(get_internal_hash(nodes[i], sibling))
    return row


def build_merkle_tree(leaves: list[bytes]) -> tuple[bytes, list[list[bytes]]]:
    all_levels = [leaves]
    current = leaves

    while len(current) > 1:
        current = get_parent_row(current)
        all_levels.append(current)

    return current[0], all_levels


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
    root, tree = build_merkle_tree(leaves)

    print(leaves)
    print(tree)
    print(base64.b64encode(root).decode())


if __name__ == "__main__":
    main()
