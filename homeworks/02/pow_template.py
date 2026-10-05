import datetime
import hashlib
import sys


def merkle_root(entries: list[str]) -> bytes:
    """Return the Merkle root of the entries (duplicate last leaf).

    :param entries: the entries of the tree
    :return: the Merkle root
    :raises ValueError: on error
    """
    pass


def l0_bits(bs: bytes) -> int:
    """Return the number of leading zero bits.

    :param bs: the byte string
    :return: the number of leading zero bits
    """
    pass


def bruteforce(seed: bytes, difficulty: int) -> tuple[int, bytes]:
    """Find the smallest 8-byte nonce such that the hash starts with >= difficulty zero bits.

    :param seed: the seed of the hash function
    :param difficulty: the minimum number of leading zero bits
    :return: the suitable nonce and the corresponding double-SHA256 hash
    :raises ValueError: on error
    """
    pass


def main():
    difficulty = 25  # The minimum number of leading zero bits.
    username = "takraa" # Change this to your student username.

    blocks = [["Stone", "Coal Ore", "Iron Ore", "Diamond Ore", username],
              ["Obsidian", "Ancient Debris", username]]

    prev_hash = bytes(32)
    for i, entries in enumerate(blocks, start=1):
        try:
            root = merkle_root(entries)
            seed = prev_hash + root + len(entries).to_bytes(4, "big")

            start = datetime.datetime.now()
            nonce, block_hash = bruteforce(seed, difficulty)
            end = datetime.datetime.now()
        except ValueError as e:
            print(f"Handled: {e}")
            sys.exit(1)

        elapsed = (end - start).total_seconds()
        rate = round(nonce / (elapsed * 1_000_000), 4) if elapsed else 0

        print(f"Block {i} (solved in {elapsed} sec, {rate} Mhash/sec)")
        print("  Previous hash:", prev_hash.hex())
        print("  Merkle root:  ", root.hex())
        print("  Leaf count:   ", len(entries))
        print("  Nonce:        ", nonce)
        print("  Block hash:   ", block_hash.hex())

        header = seed + nonce.to_bytes(8, "big")
        assert block_hash == hashlib.sha256(hashlib.sha256(header).digest()).digest()
        assert int.from_bytes(block_hash, "big") < 2 ** (256 - difficulty)

        prev_hash = block_hash


if __name__ == "__main__":
    main()
