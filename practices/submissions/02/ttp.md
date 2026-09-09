# Two-time pad

Deadline: `2026-09-27T23:59:59+03:00`

Filename: `ttp.py`

Contents:

- A function

  ```py
    def xor(a: bytes b: bytes) -> bytes:
        ...
  ```

  that returns the XOR of the two byte strings.

- A function

  ```py
    def recover_words(ct1: bytes, ct2: bytes, words: list[str]) -> tuple[str, str]:
        ...
  ```

  that recovers the two words from two ciphertexts of equal length using words from a wordlist.
