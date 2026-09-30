# Hash chain

Deadline: `2026-10-18T23:59:59+03:00`

Filename: `chain.py`

Contents:

- A function

  ```py
  def hash_chain(data: list[str]) -> list[bytes]:
      ...
  ```

  that links the given strings into a SHA-256 hash chain and returns the chain.

  Each string `d_i` is encoded as UTF-8 and linked to the previous element of the chain:

  ```
  x_0 = 0x00 * 32                    (32 zero bytes)
  x_i = SHA256(x_{i-1} || d_i)       for i = 1, ..., n
  ```

  where `||` denotes concatenation and each `x_i` is the raw 32-byte digest (not hex).

  The function must return the list `[x_1, x_2, ..., x_n]`, i.e. one element per input string, in the same order as the input.
  `x_0` is not part of the returned chain.
  An empty input yields an empty chain.

  For example:

  ```py
  chain = hash_chain(["Majora's Mask", "Spirit Tracks", "A Link to the Past"])

  assert len(chain) == 3
  assert chain[0] == sha256(bytes(32) + "Majora's Mask".encode()).digest()
  ```
