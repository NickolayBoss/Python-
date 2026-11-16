import sys
from collections.abc import Iterable
from itertools import accumulate, islice


def active_counts(slots: int, requests: Iterable[tuple[int, int]]) -> list[int]:
    changes = [0] * (slots + 1)
    for start, end in requests:
        changes[start] += 1
        changes[end] -= 1
    return list(islice(accumulate(changes), slots))


def main() -> None:
    values = iter(map(int, sys.stdin.buffer.read().split()))
    slots, count = next(values), next(values)
    requests = ((next(values), next(values)) for _ in range(count))
    print(*active_counts(slots, requests))


if __name__ == "__main__":
    main()
