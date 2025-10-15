import argparse

from Crypto.Cipher import AES

BLOCK_SIZE = AES.block_size


def pad_pkcs(msg: bytes, bl: int = BLOCK_SIZE) -> bytes:
    """Pad a message to a multiple of the block length following PKCS#7.

    :param msg: The message to pad
    :param bl: The block length
    :return: the padded message
    """
    pass


def unpad_pkcs(padded: bytes, bl: int = BLOCK_SIZE) -> bytes:
    """Remove PKCS#7 message padding.

    :param padded: The padded message
    :param bl: The block length
    :return: the unpadded message
    """
    pass


def encrypt(msg: bytes, key: bytes, iv: bytes = None) -> tuple[bytes, bytes]:
    """Encrypt a message in CBC mode.

    If the IV is not provided, generate a random IV.
    :param msg: The message to encrypt
    :param key: The encryption key
    :param iv: The initialisation vector
    :return: a tuple (ciphertext, iv)
    """
    pass


def decrypt(ct: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt a ciphertext in CBC mode.

    :param ct: The encrypted message
    :param key: The decryption key
    :param iv: The initialisation vector
    :return: the unpadded plaintext
    """
    pass


def main(enc: bool, f_in: str, f_out: str, key_hex: str, iv_hex: str | None) -> None:
    key: bytes = ...
    iv: bytes = ...

    if enc:
        with open(f_in, "rb") as f:
            plaintext = f.read()

        ciphertext, iv = encrypt(...)

        with open(f_out, "wb") as f:
            f.write(ciphertext)
    else:
        with open(f_in, "rb") as f:
            ciphertext = f.read()

        plaintext = decrypt(...)

        with open(f_out, "wb") as f:
            f.write(plaintext)

    # Do not remove or modify the print statements.
    # Do not include additional print statements in your submission.
    print("IV :", iv.hex())
    print("Key:", key.hex())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "-e", "--encrypt",
        action="store_true",
        help="encrypt the input file"
    )
    mode_group.add_argument(
        "-d", "--decrypt",
        action="store_true",
        help="decrypt the input file"
    )

    parser.add_argument(
        "-i", "--in",
        required=True,
        dest="infile",
        help="input filename"
    )
    parser.add_argument(
        "-o", "--out",
        required=True,
        dest="outfile",
        help="output filename"
    )

    parser.add_argument(
        "--key",
        required=True,
        help="secret key (hex string)"
    )
    parser.add_argument(
        "--iv",
        help="initialisation vector (hex string)"
    )

    args = parser.parse_args()
    main(args.encrypt, args.infile, args.outfile, args.key, args.iv if args.iv else None)
