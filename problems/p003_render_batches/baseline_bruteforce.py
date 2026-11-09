"""Независимый эталон для малых входов: полный перебор границ блоков."""

from collections.abc import Sequence
from itertools import accumulate, combinations, pairwise


def minimum_time_bruteforce(durations: Sequence[int], workers: int) -> int:
    """Перебирает все разбиения на ровно workers непустых блоков.

    При положительных длительностях минимум совпадает с вариантом
    «не больше workers»: любой меньший набор блоков можно дополнительно
    разделить, не увеличив максимальную сумму. Предусловия как у minimum_time.
    Использовать только на малых входах (например, n <= 12).
    """
    count = len(durations)
    prefix = list(accumulate(durations, initial=0))
    best = sum(durations)
    for cuts in combinations(range(1, count), workers - 1):
        boundaries = (0, *cuts, count)
        largest = max(prefix[end] - prefix[start] for start, end in pairwise(boundaries))
        best = min(best, largest)
    return best
