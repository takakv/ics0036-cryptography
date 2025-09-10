def strings():
    # This is a regular UTF-8 string.
    utf8_string = "This is a string 💥 三味線 عود"

    # This is a (UTF-8) string that contains only ASCII characters.
    ascii_string = "This is an ascii-compatible string"

    # ASCII representations of strings can be written directly with the b prefix.
    # More specifically, this approach only works for characters that can be
    # represented with one byte only.
    byte_string = b"This is a byte string"

    # String variables can be converted into bytes with the
    # str.encode() method. By default, the encoding is UTF-8.
    utf8_string_as_bytes = utf8_string.encode()

    # You could specify also some other encoding, e.g. ASCII.
    ascii_string_as_bytes = ascii_string.encode("ascii")

    # Trying to encode a string in a format which does not support the represented characters
    # will raise an exception.
    try:
        utf8_string.encode("ascii")
    except UnicodeEncodeError:
        # We ignore the exception here.
        pass

    # Decoding works like the str.encode() method, just with
    # bytes.decode(). By default (no argument specified), UTF-8 is used.
    decoded = utf8_string_as_bytes.decode()

    print(f"{type(utf8_string)}: {utf8_string=}")
    print(f"{type(ascii_string)}: {ascii_string=}")
    print(f"{type(byte_string)}: {byte_string=}")
    print(f"{type(utf8_string_as_bytes)}: {utf8_string_as_bytes=}")
    print(f"{type(ascii_string_as_bytes)}: {ascii_string_as_bytes=}")
    print(f"{type(decoded)}: {decoded=}")


# The name/keyword 'bytes' is reserved and represents the bytes type.
# Therefore, naming the function bytes() is bad practice, even if it works.
def bytes_and_hex():
    # Byte strings can be represented directly with the b prefix.
    # To represent byte values directly, you can use the HEX-representation of the byte
    # and prepend \x to it.
    b = b"These are some bytes \x00\xff"

    # You can obtain a hex-string from bytes with the bytes.hex() method.
    b_as_hex = b.hex()
    print(f"{b_as_hex=}")

    # By default, this yields a lowercase hex string.
    # For uppercase hex, you can use the str.upper() method.
    b_as_uppercase_hex = b_as_hex.upper()
    print(f"{b_as_uppercase_hex=}")

    # The hex characters can also be separated for better readability
    # by passing the separator to the bytes.hex() method.
    b_as_space_separated_hex = b.hex(" ")
    print(f"{b_as_space_separated_hex=}")

    # Bytes can be obtained from hex strings with the bytes.fromhex() method.
    b_from_hex = bytes.fromhex(b_as_hex)
    print(f"{b_from_hex=}")


def bytes_and_b64():
    b = b"These are some bytes \x00\xff"

    # For base64 encodings, you need to import the built-in 'base64' python module.
    import base64

    # Bytes can be base64-encoded with the base64.b64encode() method.
    # The output of a base64 encoding is the 'bytes' type.
    b_b64_bytes = base64.b64encode(b)
    print(f"{b_b64_bytes=}")

    # To get a base64 string:
    b_b64_string = base64.b64encode(b).decode()
    print(f"{b_b64_string=}")

    # Likewise, the base64.b64decode() method can be used to convert
    # base64-encoded strings/byte objects back into regular bytes.
    b_from_b64_string = base64.b64decode(b_b64_string)
    b_from_b64_bytes = base64.b64decode(b_b64_bytes)
    print(f"{b_from_b64_string=}")
    print(f"{b_from_b64_bytes=}")


def loops_and_conditionals():
    # 'sum' is a built-in name, so you should not name a variable that.
    loop_sum = 0

    # The loop iterates 10 times, starting from 0, and ending at 9.
    # That is, for the range() method, the upper bound is exclusive.
    for _ in range(10):
        # This will add 1 to the 'loop_sum' on each iteration.
        loop_sum += 1

    # Lists or strings can be iterated over with the same syntax.
    string = "This is some string"
    string2 = ""  # an empty string
    for c in string:
        # This will add the current character to the string.
        string2 += c

    # Assertions will abort the program execution if the condition fails.
    assert string == string2

    numbers = [1, 1, 1, 1, 1]
    n_sum = 0
    for n in numbers:
        n_sum += n

    # Equalities can be chained.
    assert sum(numbers) == n_sum == 5

    # Booleans are written with a capital.
    boolean_true = True
    boolean_false = False

    if boolean_true:
        print("If")

    if boolean_false:
        print("This will not print")
    elif boolean_true:
        print("Else if")
    else:
        print("This will print")

    if boolean_false:
        print("This will not print")
    else:
        print("Else")

    print()

    # Logical AND, NOT operators.
    if boolean_true and not boolean_false:
        print("[boolean_true is true] and [(not boolean_false) is true]")

    # Logical OR, NOT operators.
    if boolean_false or not boolean_true or boolean_true:
        print("One of the statements is true")

    # The None type
    empty = None
    not_empty = ""

    if empty is not None:
        print("This will not print")

    if not_empty is None:
        print("This will not print")


def xor(a: bytes, b: bytes) -> bytes:
    # The a, b are interpreted as integers (0 <= x < 256).
    return bytes(a ^ b for a, b in zip(a, b))


def bitwise_operators():
    b = b"\x00\x01\x10\xAE\xFF"

    # You can repeat a character by multiplying it by a number.
    # You can get the length of a list/string with the len() method.
    assert xor(b, b) == b"\x00" * len(b)  # XOR of a bitstring with itself is the 0-bitstring

    # Integers can be assigned directly as hex with the '0x' prefix
    i1 = 0x01
    i3 = 0x03

    assert i1 == 1 and i3 == 3

    # Bitwise OR: (bit is one if at least either input bit is one)
    assert 0x03 == i1 | i3

    # The hex-representation of integers can be printed as a string as follows.
    # The 02 specifies that print the least significant 2 hex-digits with 0 prefix, if needed.
    print(f"0x{i1:02x} | 0x{i3:02x}:")

    # The bit-representation of integers can be printed as a string as follows.
    # The 08 specifies that print the least significant 8 bits with 0 prefix, if needed.
    print(f"    {i1:08b}")
    print(f" OR {i3:08b}")
    print(f"    {i1 | i3:08b}")

    # Bitwise AND: (bit is one only if both input bits are one)
    assert 0x01 == i1 & i3

    print()
    print(f"0x{i1:02x} & 0x{i3:02x}:")
    print(f"    {i1:08b}")
    print(f"AND {i3:08b}")
    print(f"    {i1 & i3:08b}")

    # XOR: (bit is one only if only one input bit is one)
    assert 0x02 == i1 ^ i3

    print()
    print(f"0x{i1:02x} ^ 0x{i3:02x}:")
    print(f"    {i1:08b}")
    print(f"XOR {i3:08b}")
    print(f"    {i1 ^ i3:08b}")


def main():
    print("NB! Encodings/decodings and other operations may fail.")
    print("It is your responsibility to look up the appropriate error handling.")
    print()

    strings()
    print()

    bytes_and_hex()
    print()

    bytes_and_b64()
    print()

    loops_and_conditionals()
    print()

    bitwise_operators()


if __name__ == "__main__":
    main()
