import base64
from hashlib import sha256

games = ["Majora's Mask", "Spirit Tracks",
         "A Link to the Past", "Breath of the Wild",
         "Ocarina of Time", "The Wind Waker"]


def get_hash(data: bytes) -> bytes:
    return sha256(data).digest()


def get_joint_parent(left: bytes, right: bytes) -> bytes:
    return get_hash(left + right)


def get_parent_row(nodes: list[bytes]) -> list[bytes]:
    row = []
    for i in range(0, len(nodes), 2):
        # If the row has an odd number of elements, duplicate the last one.
        # Otherwise, use the right sibling.
        sibling = nodes[i + 1] if i + 1 < len(nodes) else nodes[i]
        row.append(get_joint_parent(nodes[i], sibling))
    return row


def build_merkle_tree(leaves: list[bytes]) -> tuple[bytes, list[list[bytes]]]:
    intermediates = []
    current = leaves

    while len(current) > 1:
        current = get_parent_row(current)
        intermediates.append(current)

    # Exclude the root from the intermediates
    return current[0], intermediates[:-1]


def main():
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


if __name__ == "__main__":
    main()
