# Authenticating your ciphertexts

Deadline: `2026-10-04T23:59:59+03:00`

Filename: `gcm.py`

Third-party modules: `cryptography`

Contents:

- A data structure for holding the ciphertext, nonce, authentication tag triple.

  ```py
  from typing import NamedTuple

  class Ciphertext(NamedTuple):
      nonce: bytes
      ct: bytes
      tag: bytes
  ```

- A function

  ```py
  def validator(key: bytes, ciphertexts: list[Ciphertext]) -> list[Ciphertext]:
      ...
  ```

  that takes as input an AES key, a list of AES-GCM encrypted ciphertexts (including nonces and auth tags) and returns a list of ciphertexts whose authentication tag does not validate.

  If all authentication tags validate, the validator should return an empty list.

  > Tip: write your own challenger to test your validator.
  > You may leave your challenger code in the submitted file.
