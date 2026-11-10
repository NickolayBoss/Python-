"""Независимый квадратичный эталон: все старты, множество типов."""
from collections.abc import Sequence


def longest_window_bruteforce(events: Sequence[int], limit: int) -> tuple[int, int]:
    """Тот же контракт, что у longest_window; предназначен для малых входов."""
    best = (0, 0)
    for left in range(len(events)):
        types = set()
        for right in range(left, len(events)):
            types.add(events[right])
            if len(types) > limit:
                break
            if right + 1 - left > best[1] - best[0]:
                best = (left, right + 1)
    return best
