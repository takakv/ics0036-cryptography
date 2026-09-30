import hmac
import secrets


# noinspection SpellCheckingInspection
def main():
    message = "MACs are important!"
    key = secrets.token_bytes(16)
    mac = ...

    received = "MACs are importantǃ"
    check_mac = ...

    # TODO: verify the MAC using constant-time comparison!
    ...

    # TODO: encrypt the original message using authenticated chacha20
    ciphertext, tag = ...

    # TODO: change the ciphertext and try to decrypt it

    # TODO: change the tag and try to decrypt the AEAD ciphertext

    # TODO: change the AAD and try to decrypt the AEAD ciphertext


if __name__ == "__main__":
    main()
