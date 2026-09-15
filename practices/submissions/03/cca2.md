# Winning IND-CCA2

Deadline: `2026-10-04T23:59:59+03:00`

Filename: `cca.py`

Third-party modules: `cryptography`

Helper script: `challenger.py`

Contents:

- A function

  ```py
  def distinguisher(challenger: Challenger) -> int:
      ...
  ```

  that uses the `challenger` as an IND-CCA2 adversary.
  See the code comments for the API.

  Encryption: `challenger.encrypt(m: bytes)`

  Decryption: `challenger.decrypt(c: bytes, nonce: bytes)`

  Request the challenge: `challenger.request_challenge(m0: bytes, m1: bytes)`

  Verify your guess locally: `challenger.verify_guess(guess: int)`

  The distinguisher must return `0` if the first message was encrypted, `1` otherwise.
  The distinguisher should be correct 100% of the time.

  For example:

  ```py
  challenger = Challenger()
  guess = distinguisher(challenger)

  print(challenger.verify_guess(guess))
  ```
