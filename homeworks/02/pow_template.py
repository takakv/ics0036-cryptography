import datetime
import hashlib


def l0_bits(bs: bytes) -> int:
    """Return the number of leading 0 bits.

    :param bs: the byte string
    :return: the number of leading 0 bits
    """
    pass


def bruteforce(seed: bytes, difficulty: int = 0) -> tuple[int, bytes]:
    """Find an 8-byte nonce such that the hash starts with >= x 0-bits.

    :param seed: the seed of the hash function
    :param difficulty: the minimum number of expected 0-bits
    :return: the suitable nonce and the corresponding double-SHA256 input
    """
    assert difficulty >= 0

    nonce = 0
    lead = 0
    hash_result = b""

    return nonce, hash_result


def main():
    difficulty = 25  # The minimum number of leading 0-bits.
    seed = b"takraa" # Change this to your student username.

    start = datetime.datetime.now()
    nonce, res = bruteforce(seed, difficulty)
    end = datetime.datetime.now()

    ip = seed + nonce.to_bytes(8, "big")

    elapsed = (end - start).total_seconds()
    unit_time = round(nonce / (elapsed * 1_000_000), 4)

    print(f"Solved in {elapsed} sec ({unit_time} Mhash/sec)")
    print("Seed:", seed.decode())
    print("Nonce:", nonce)
    print("Input:", ip.hex())
    print("Solution:", res.hex())

    res_int = int.from_bytes(res, "big")
    assert res_int < pow(2, 256 - difficulty)


if __name__ == "__main__":
    main()
