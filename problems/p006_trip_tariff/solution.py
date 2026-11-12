"""Поиск первой подходящей границы и минимум цены на суффиксе."""
from bisect import bisect_left
from collections.abc import Iterable, Sequence
import sys


def cheapest_tariffs(
    tariffs: Sequence[tuple[int, int]], trips: Iterable[int]
) -> list[int]:
    """Возвращает цены в порядке поездок. Тарифы отсортированы по дальности."""
    limits = [limit for limit, _ in tariffs]
    best = [price for _, price in tariffs]
    for index in range(len(best) - 2, -1, -1):
        best[index] = min(best[index], best[index + 1])

    answers = []
    for distance in trips:
        start = bisect_left(limits, distance)
        answers.append(best[start] if start < len(best) else -1)
    return answers


def solve(data: bytes) -> str:
    numbers = iter(map(int, data.split()))
    count, query_count = next(numbers), next(numbers)
    tariffs = [(next(numbers), next(numbers)) for _ in range(count)]
    trips = (next(numbers) for _ in range(query_count))
    return "\n".join(map(str, cheapest_tariffs(tariffs, trips)))


if __name__ == "__main__":
    print(solve(sys.stdin.buffer.read()))
