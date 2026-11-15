import sys
from collections.abc import Iterable


def count_pairs(prices: Iterable[int], budget: int) -> int:
    ordered = sorted(prices)
    left, right = 0, len(ordered) - 1
    total = 0
    while left < right:
        if ordered[left] + ordered[right] <= budget:
            total += right - left
            left += 1
        else:
            right -= 1
    return total


def main() -> None:
    _, budget = map(int, sys.stdin.buffer.readline().split())
    prices = map(int, sys.stdin.buffer.read().split())
    print(count_pairs(prices, budget))


if __name__ == "__main__":
    main()
