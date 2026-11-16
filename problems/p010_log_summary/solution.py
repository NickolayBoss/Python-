import sys
from bisect import bisect_left
from collections import defaultdict
from itertools import accumulate


class LogSummary:
    def __init__(self, codes: list[int], values: list[int], limit: int) -> None:
        self.totals = list(accumulate(values, initial=0))
        self.positions: dict[int, list[int]] = defaultdict(list)
        counts: dict[int, int] = {}
        left = 0
        self.longest = 0

        for right, code in enumerate(codes):
            self.positions[code].append(right)
            counts[code] = counts.get(code, 0) + 1
            while len(counts) > limit:
                outgoing = codes[left]
                counts[outgoing] -= 1
                if counts[outgoing] == 0:
                    del counts[outgoing]
                left += 1
            self.longest = max(self.longest, right - left + 1)

    def range_sum(self, left: int, right: int) -> int:
        return self.totals[right] - self.totals[left]

    def frequency(self, left: int, right: int, code: int) -> int:
        positions = self.positions.get(code, ())
        return bisect_left(positions, right) - bisect_left(positions, left)


def main() -> None:
    stream = sys.stdin.buffer
    size, query_count, limit = map(int, stream.readline().split())
    codes, values = [], []
    for _ in range(size):
        code, value = map(int, stream.readline().split())
        codes.append(code)
        values.append(value)

    summary = LogSummary(codes, values, limit)
    answers = []
    for _ in range(query_count):
        kind, *args = map(int, stream.readline().split())
        if kind == 1:
            answer = summary.range_sum(*args)
        elif kind == 2:
            answer = summary.frequency(*args)
        else:
            answer = summary.longest
        answers.append(str(answer))
    sys.stdout.write("\n".join(answers) + "\n")


if __name__ == "__main__":
    main()
