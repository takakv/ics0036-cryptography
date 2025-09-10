import random
import secrets

# True if the challenge is from the CSPRNG, False otherwise
challenger_picks: list[bool] = []


def challenger(clen: int) -> bytes:
    b = secrets.choice([True, False])
    challenger_picks.append(b)

    challenge: bytes
    if b:
        challenge = secrets.token_bytes(clen)
    else:
        challenge = random.randbytes(clen)

    return challenge


def distinguisher() -> bool:
    # TODO: write the distinguisher/adversary logic.
    challenge = challenger(1)
    return secrets.choice([True, False])


def main():
    results: list[bool] = []

    total_count = 1000

    for _ in range(total_count):
        results.append(distinguisher())

    success_count = 0
    for i in range(total_count):
        if results[i] == challenger_picks[i]:
            success_count += 1

    print("Success rate:", success_count / total_count)


if __name__ == "__main__":
    main()
