import sys
from collections.abc import Iterable


def max_meetings(meetings: Iterable[tuple[int, int]]) -> int:
    last_end = 0
    count = 0
    for start, end in sorted(meetings, key=lambda meeting: meeting[1]):
        if start >= last_end:
            last_end = end
            count += 1
    return count


def main() -> None:
    values = iter(map(int, sys.stdin.buffer.read().split()))
    count = next(values)
    meetings = ((next(values), next(values)) for _ in range(count))
    print(max_meetings(meetings))


if __name__ == "__main__":
    main()
