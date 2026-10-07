# Man-in-the-middle

Deadline: `2026-10-25T23:59:59+03:00`

Filename: `mitm.py`

Third-party modules: `cryptography` (version 47 or later)

Helper code: `channel.py`

Contents:

- A function

  ```py
  def mitm(channel: Channel) -> bytes:
      ...
  ```

  that sniffs the `channel` between Alice and Bob, and returns the message sent by Alice.
  Neither Bob nor Alice must notice the attack.

  Alice encrypts her message to Bob's public key with HPKE, using `SUITE` and `INFO` from `channel.py`.
  Public keys are PEM encoded P-384 keys.
  See [HPKE](https://cryptography.io/en/latest/hazmat/primitives/hpke/) and [key serialization](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/).

  Bob's public key: `channel.bob_public_key() -> bytes`

  Alice's ciphertext, encrypted to the public key given to her: `channel.alice_encrypt(pk: bytes) -> bytes`

  Deliver a ciphertext to Bob: `channel.bob_receive(ct: bytes)`

  The attack should succeed 100% of the time.

  For example:

  ```py
  channel = Channel()
  m = mitm(channel)
  ```

  > Tip: verify your attack locally with `channel.verify(m)`.
  > It returns `True` when `m` is the message sent by Alice and received by Bob.
