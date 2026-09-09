# Dubious IND-CPA

Deadline: `2026-09-27T23:59:59+03:00`

Filename: `cpa.py`

Contents:

- A function

  ```py
  def challenger(m1: bytes, m2: bytes) -> tuple[bytes, bytes]:
      ...
  ```

  that takes as input two messages of potentially different length, selects one of them uniformly at random, generates a ChaCha20 key, encrypts the chosen message with it, and returns the pair `(ciphertext, nonce)`.

- A function

  ```py
  from collections.abc import Callable

  def distinguisher(challenger: Callable[[bytes, bytes], bytes]) -> bool:
      ...
  ```

  that calls the given `challenger` with two messages of the adversary's own choice, and returns `True` if the first message was encrypted, `False` otherwise.
  The adversary should win the game 100% of the time.

  For example:

  ```py
  guessed_first = distinguisher(challenger)
  ```
