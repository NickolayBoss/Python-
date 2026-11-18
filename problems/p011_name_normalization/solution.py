import sys


def normalize_name(name: str) -> str:
    return " ".join(name.split()).casefold()


def names_match(first: str, second: str) -> bool:
    return normalize_name(first) == normalize_name(second)


def main() -> None:
    first = sys.stdin.buffer.readline().decode("utf-8")
    second = sys.stdin.buffer.readline().decode("utf-8")
    print("YES" if names_match(first, second) else "NO")


if __name__ == "__main__":
    main()
