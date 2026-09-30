# Proof of inclusion

Deadline: `2026-10-18T23:59:59+03:00`

Filename: `merkle.py`

Contents:

- A function

  ```py
  def inclusion_proof(tree: list[list[bytes]], leaf: str) -> list[bytes]:
      ...
  ```

  that takes as input a binary SHA-256 Merkle tree and a string whose leaf is in the tree, and returns the proof of inclusion for that leaf: all hashes needed to reconstruct the root from the leaf.

  **The tree.**

  The tree is built with the *duplicate last leaf* approach from the practice session:

  - A leaf is the hash of the UTF-8 encoded string: `SHA256(s)`.
  - A parent is the hash of its two children: `SHA256(left || right)`.
  - If a level has an odd number of nodes, the last node is paired with itself.

  The tree is given as a list of levels, from the leaves up to the root:
  `tree[0]` holds the leaves in order, `tree[1]` their parents, and so on, and `tree[-1] == [root]`.
  Every node is a raw 32-byte digest.

  The duplicated nodes are **not** stored in the tree.
  For example, a tree with five leaves is given as

  ```
  tree[0]:  X1 X2 X3 X4 X5
  tree[1]:  H1 H2 H3
  tree[2]:  G1 G2
  tree[3]:  Root
  ```

  where all leaves are distinct.

  **The proof.**

  The proof contains exactly one hash per level below the root, ordered from the leaf level upwards: the sibling of the leaf, then the sibling of its parent, and so on.
  If a node has no sibling, because it was paired with itself, its own hash is the sibling.
  The root and the leaf itself are not part of the proof.

  For the tree above, the proof for `X3` is `[X4, H1, G2]`, and the proof for `X5` is `[X5, H3, G1]`.
  A tree with a single leaf has an empty proof.

  For example:

  ```py
  proof = inclusion_proof(tree, "A Link Between Worlds")
  ```

  > Tip: build your own trees (and potentially a validator) to test your function.
  > You may leave that code in the submitted file.
