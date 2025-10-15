#!/usr/bin/env bash

PYSCRIPT="./aes_ecb_cbc.py"

PLAINTEXT="msg.txt"
ENCRYPTED="ct.bin"
DECRYPTED="dec.txt"

echo "Cryptography is typically bypassed, not penetrated. - Adi Shamir" > "$PLAINTEXT"

echo "Test script for $PYSCRIPT"
echo "This script does not cover all edge cases!"

for BYTES in 16 24 32; do
    BITS=$((BYTES * 8))

    echo
    echo "=== AES-${BITS}-CBC ==="

    KEY=$(openssl rand -hex $BYTES)
    IV=$(openssl rand -hex 16)

    python3 $PYSCRIPT -e --in "$PLAINTEXT" --out "$ENCRYPTED" --key "$KEY" --iv "$IV"
    openssl enc -d -aes-${BITS}-cbc -in "$ENCRYPTED" -out "$DECRYPTED" -K "$KEY" -iv "$IV"

    HASH1=$(sha256sum "$PLAINTEXT" | awk '{print $1}')
    HASH2=$(sha256sum "$DECRYPTED" | awk '{print $1}')

    if [[ "$HASH1" == "$HASH2" ]]; then
        echo "Encryption OK"
    else
        echo "Encryption is incorrect"
    fi

    echo

    openssl enc -e -aes-${BITS}-cbc -in "$PLAINTEXT" -out "$ENCRYPTED" -K "$KEY" -iv "$IV"
    python3 $PYSCRIPT -d --in "$ENCRYPTED" --out "$DECRYPTED" --key "$KEY" --iv "$IV"

    HASH1=$(sha256sum "$PLAINTEXT" | awk '{print $1}')
    HASH2=$(sha256sum "$DECRYPTED" | awk '{print $1}')

    if [[ "$HASH1" == "$HASH2" ]]; then
        echo "Decryption OK"
    else
        echo "Decryption is incorrect"
    fi
done
