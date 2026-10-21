#!/usr/bin/env sh

# Runs all commands of the 'Signing with pkeyutl' and
# 'Verifying signatures with pkeyutl' tasks in the current directory.
# Requires OpenSSL 3.5 or later (ML-DSA, -digest without -rawin).

set -e

# Generate keypairs
echo "Generating Ed25519, P-384, RSA-3072 and ML-DSA-65 keypairs"
openssl genpkey -algorithm ed25519 \
  -out ed.priv.pem -outpubkey ed.pem
openssl genpkey -algorithm EC \
  -pkeyopt ec_paramgen_curve:P-384 \
  -out ec.priv.pem -outpubkey ec.pem
openssl genpkey -algorithm RSA \
  -pkeyopt rsa_keygen_bits:3072 -quiet \
  -out rsa.priv.pem -outpubkey rsa.pem
openssl genpkey -algorithm ML-DSA-65 \
  -out mldsa.priv.pem -outpubkey mldsa.pem
echo "Generated OK"

echo

# Create the message file
echo "Message" > message.txt

# Ed25519 in pure mode
echo "Ed25519 (deterministic)"
openssl pkeyutl -sign \
  -in message.txt -inkey ed.priv.pem -out ed1.sig
openssl pkeyutl -sign \
  -in message.txt -inkey ed.priv.pem -out ed2.sig
sha256sum ed*.sig

echo

# ECDSA with SHA-384
echo "ECDSA (probabilistic)"
openssl pkeyutl -sign \
  -digest sha384 \
  -in message.txt -inkey ec.priv.pem -out ec1.sig
openssl pkeyutl -sign \
  -digest sha384 \
  -in message.txt -inkey ec.priv.pem -out ec2.sig
sha256sum ec*.sig

echo

# Deterministic ECDSA with SHA-384
echo "ECDSA with nonce-type:1 (deterministic)"
openssl pkeyutl -sign \
  -digest sha384 -pkeyopt nonce-type:1 \
  -in message.txt -inkey ec.priv.pem -out detec1.sig
openssl pkeyutl -sign \
  -digest sha384 -pkeyopt nonce-type:1 \
  -in message.txt -inkey ec.priv.pem -out detec2.sig
sha256sum detec*.sig

echo

# RSASSA-PSS with SHA-256
echo "RSASSA-PSS (probabilistic)"
openssl pkeyutl -sign \
  -digest sha256 \
  -pkeyopt rsa_padding_mode:pss \
  -pkeyopt rsa_pss_saltlen:digest \
  -pkeyopt rsa_mgf1_md:sha256 \
  -in message.txt -inkey rsa.priv.pem -out pss1.sig
openssl pkeyutl -sign \
  -digest sha256 \
  -pkeyopt rsa_padding_mode:pss \
  -pkeyopt rsa_pss_saltlen:digest \
  -pkeyopt rsa_mgf1_md:sha256 \
  -in message.txt -inkey rsa.priv.pem -out pss2.sig
sha256sum pss*.sig

echo

# RSASSA-PKCS1-v1_5 with SHA-256
echo "RSASSA-PKCS1-v1_5 (deterministic)"
openssl pkeyutl -sign \
  -digest sha256 \
  -pkeyopt rsa_padding_mode:pkcs1 \
  -in message.txt -inkey rsa.priv.pem -out pkcs1-1.sig
openssl pkeyutl -sign \
  -digest sha256 \
  -pkeyopt rsa_padding_mode:pkcs1 \
  -in message.txt -inkey rsa.priv.pem -out pkcs1-2.sig
sha256sum pkcs1*.sig

echo

# ML-DSA-65 in pure mode
echo "ML-DSA-65 (hedged)"
openssl pkeyutl -sign \
  -in message.txt -inkey mldsa.priv.pem -out mldsa1.sig
openssl pkeyutl -sign \
  -in message.txt -inkey mldsa.priv.pem -out mldsa2.sig
sha256sum mldsa*.sig

echo

# Deterministic ML-DSA-65
echo "ML-DSA-65 with deterministic:1 (deterministic)"
openssl pkeyutl -sign -pkeyopt deterministic:1 \
  -in message.txt -inkey mldsa.priv.pem -out detmldsa1.sig
openssl pkeyutl -sign -pkeyopt deterministic:1 \
  -in message.txt -inkey mldsa.priv.pem -out detmldsa2.sig
sha256sum detmldsa*.sig

echo

# Verify signatures
echo "Verifying Ed25519"
openssl pkeyutl -verify \
  -in message.txt -pubin -inkey ed.pem -sigfile ed1.sig

echo "Verifying ECDSA (probabilistic and deterministic)"
openssl pkeyutl -verify -digest sha384 \
  -in message.txt -pubin -inkey ec.pem -sigfile ec1.sig
openssl pkeyutl -verify -digest sha384 \
  -in message.txt -pubin -inkey ec.pem -sigfile detec1.sig

echo "Verifying RSASSA-PSS"
openssl pkeyutl -verify -digest sha256 \
  -pkeyopt rsa_padding_mode:pss \
  -pkeyopt rsa_pss_saltlen:digest \
  -pkeyopt rsa_mgf1_md:sha256 \
  -in message.txt -pubin -inkey rsa.pem -sigfile pss1.sig

echo "Verifying RSASSA-PKCS1-v1_5"
openssl pkeyutl -verify -digest sha256 \
  -pkeyopt rsa_padding_mode:pkcs1 \
  -in message.txt -pubin -inkey rsa.pem -sigfile pkcs1-1.sig

echo "Verifying ML-DSA-65 (hedged and deterministic)"
openssl pkeyutl -verify \
  -in message.txt -pubin -inkey mldsa.pem -sigfile mldsa1.sig
openssl pkeyutl -verify \
  -in message.txt -pubin -inkey mldsa.pem -sigfile detmldsa1.sig

echo

# Compare sizes
echo "Signature sizes (bytes)"
wc -c ./*.sig

echo

echo "Public key sizes (bytes, DER)"
for k in ed ec rsa mldsa; do
  printf "%s.pem: " "$k"
  openssl pkey -pubin -in "$k.pem" -outform DER | wc -c
done
