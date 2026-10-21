# $k$ then

Deadline: `2026-11-08T23:59:59+02:00`

Filename: `recovery.py`

Third-party modules: `cryptography`

## Background

Let $G = (x_g, y_g)$ be the elliptic curve base point (the group generator) and let $n$ be the order of $G$ (the number of points in the group).
Let $d$ be the secret scalar/integer (the private key), and let $Q$ be the public key with $Q = dG$.

Let $m$ be a message string.
The ECDSA signature of $m$ is obtained as follows:

1. Compute $\mathrm{HASH}(m)$ and convert this bit string to an integer $e$.
2. Let $z$ be the $L_n$ leftmost bits of $e$, where $L_n$ is the bit length of the group order.
3. Sample uniformly at random an integer $k$ with $k \in [1, n - 1]$.
4. Compute the curve point $(x_1, y_1) \gets kG$.
5. Compute $r \gets x_1 \bmod{n}$. If $r = 0$, go to step 3.
6. Compute $s \gets k^{-1}(z + dr) \bmod{n}$. If $s = 0$, go to step 3.
7. The signature is the pair $(r, s)$.

> [!NOTE]
> **Fun fact: ECDSA signatures are malleable.**
> If $(r, s)$ is a valid signature on $m$, then so is $(r, -s \bmod n)$.
> Anyone can turn a valid signature into a different valid signature on the same message, without knowing the private key.
> This is why ECDSA is not *strongly* unforgeable (sEUF, see the lecture).
>
> This has caused real problems e.g. in Bitcoin transaction IDs.
> See [BIP 146](https://github.com/bitcoin/bips/blob/master/bip-0146.mediawiki) for more info, if interested.

If $k$ is not sampled fresh for every signature, then using the same $k$ for two different messages $m_1, m_2$ leads to the recovery of the private key $d$.

Given two messages $m_1, m_2$ and their respective signatures $(r_1, s_1)$, $(r_2, s_2)$ that reuse the same $k$ value, $k$ can be recovered by computing

$$
k \gets (z_1 - z_2)(s_1 - s_2)^{-1} \bmod{n}\ .
$$

Given $k$ and a signature $(r, s)$, the private key can be recovered by computing

$$
d \gets (sk - z)r^{-1} \bmod n\ .
$$

## Tips

To compute the modular multiplicative inverse, you can use the built-in `pow()` function with $-1$ as the exponent, e.g. the multiplicative inverse of `a` modulo `b` can be computed with

```python
pow(a, -1, b)
```

Bytes can be converted to an integer with

```python
int.from_bytes(..., "big")
```

`pyca/cryptography` tips:

- The public key can be parsed with [`load_pem_public_key()`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/#cryptography.hazmat.primitives.serialization.load_pem_public_key).
- The $n$ value is the `group_order` of [`EllipticCurve`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#cryptography.hazmat.primitives.asymmetric.ec.EllipticCurve) which in turn is the `curve` of [`EllipticCurvePublicKey`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey).
- ECDSA signature bytes can be parsed into $r$ and $s$ using [`decode_dss_signature()`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/utils/#cryptography.hazmat.primitives.asymmetric.utils.decode_dss_signature).
- Given $d$, the private key object can be recreated with [`derive_private_key()`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#cryptography.hazmat.primitives.asymmetric.ec.derive_private_key).
- The P-384 curve object can be created with [`ec.SECP384R1()`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#cryptography.hazmat.primitives.asymmetric.ec.SECP384R1).

## Task

Contents:

- A function

  ```py
  def recover_k(z1: int, s1: int, z2: int, s2: int, n: int) -> int:
      ...
  ```

  that recovers the $k$ value from $z_1, s_1, z_2, s_2, n$.

- A function

  ```py
  def recover_d(s: int, k: int, z: int, r: int, n: int) -> int:
      ...
  ```

  that recovers the $d$ value from $s, k, z, r, n$.

- A function

  ```py
  def recover_private_key(m1: bytes, sig1: bytes, m2: bytes, sig2: bytes,
                          pk: ec.EllipticCurvePublicKey,
                          h: hashes.HashAlgorithm) -> ec.EllipticCurvePrivateKey:
      ...
  ```

  that takes as argument the two signed messages and their signatures as bytes, the public key object used to verify the signatures, and the hash algorithm used within ECDSA (e.g. [`hashes.SHA384()`](https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/#cryptography.hazmat.primitives.hashes.SHA384)).

  You may assume that the hash algorithm always ‘fits’ the curve size, i.e. $e$ never exceeds the bit-length of the curve, so $L_n$ is not a concern for you and you can simply interpret the hash output as $e$.
  
  The function should return a private key object.

  For example:

  ```py
  with open("pub.pem", "rb") as f:
      pk = load_pem_public_key(f.read())

  if not isinstance(pk, ec.EllipticCurvePublicKey):
      raise TypeError("pub.pem is not an EC public key")

  with open("m1.txt", "rb") as f:
      m1 = f.read()

  with open("m1.sig", "rb") as f:
      sig1 = f.read()

  with open("m2.txt", "rb") as f:
      m2 = f.read()

  with open("m2.sig", "rb") as f:
      sig2 = f.read()

  sk = recover_private_key(m1, sig1, m2, sig2, pk, hashes.SHA384())

  m = b"Hyah!"
  sig = sk.sign(m, ec.ECDSA(hashes.SHA384()))

  try:
      pk.verify(sig, m, ec.ECDSA(hashes.SHA384()))
  except InvalidSignature:
      print("Signature verification failed")
      sys.exit(1)
  ```
