class BruteLogSummary:
    def __init__(self, codes: list[int], values: list[int], limit: int) -> None:
        self.codes = codes
        self.values = values
        self.longest = max(
            right - left
            for left in range(len(codes) + 1)
            for right in range(left, len(codes) + 1)
            if len(set(codes[left:right])) <= limit
        )

    def range_sum(self, left: int, right: int) -> int:
        return sum(self.values[left:right])

    def frequency(self, left: int, right: int, code: int) -> int:
        return self.codes[left:right].count(code)
