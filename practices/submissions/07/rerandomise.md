# Nifty homomorphism

Deadline: `2026-11-08T23:59:59+02:00`

Filename: `rerandomise.py`

Third-party modules: `fastecdsa` (preferred) or `tinyec`, `cryptography`

**The scenario.**

The legendary cryptographer Mr. Cry has developed the following authentication protocol:

- Authorised users know the secret authentication code.
- To gain access to the server, users encrypt this code with EC ElGamal (P-384) to obtain the *token*, submit the token to the server, and the server decrypts it.
  If the decrypted result corresponds to the authentication code, the user is granted access.
- To avoid authentication token re-use, the server remembers all previously used tokens.
  If you submit a previously used token, the server will deny you access.
- To mitigate "double-submission" (you submit the same token twice e.g. due to bad latency), the server displays the previously used token to the user.

Your goal is to forge a fresh token from a previously used one and thus gain access.
You do not know the authentication code, nor the server's private key.

Contents:

- A function

  ```py
  def octets_to_point(octets: bytes, curve: Curve) -> Point:
      ...
  ```

  that parses a SEC 1 uncompressed point (`0x04 || xCoordBytes || yCoordBytes`, see [SEC 1 v2.0 §2.3.3](https://www.secg.org/sec1-v2.pdf#subsubsection.2.3.3)) and returns the corresponding point on the given curve.

- A function

  ```py
  def point_to_octets(p: Point) -> bytes:
      ...
  ```

  that serialises a point into the SEC 1 uncompressed point representation.

  The `Point` and `Curve` types may be taken from `fastecdsa` or `tinyec`.
  If the library has appropriate methods for (de)serialisation, you may use those in the functions.

- A function

  ```py
  def rerandomise(u: bytes, v: bytes, pk: bytes) -> tuple[bytes, bytes]:
      ...
  ```

  that takes as input a token `(U, V)` and the server's public key, and returns a fresh token `(U', V')`.
  The points `U` and `V` are given and must be returned as SEC 1 uncompressed points.
  The public key `pk` is a PEM encoded P-384 public key in the standard SubjectPublicKeyInfo format ([RFC 5480](https://datatracker.ietf.org/doc/html/rfc5480)), see [key serialization](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/).

  The fresh token is accepted if:

  - it decrypts to the same message as the given token: `DEC((U, V)) == DEC((U', V'))`, and
  - it differs from the given token: `U != U'` or `V != V'`.

  The forgery should succeed 100% of the time.

  For example:

  ```py
  u2, v2 = rerandomise(u, v, pk)

  assert (u2, v2) != (u, v)
  ```

  > Tip: get a test token and public key from the Discord bot with `/eg_auth`, and submit your fresh token to it to validate your solution.
