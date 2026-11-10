"""Независимый эталон: накапливаем сумму для каждой левой границы."""
from collections.abc import Sequence


def count_segments_bruteforce(changes: Sequence[int], target: int) -> int:
    answer = 0
    for left in range(len(changes)):
        total = 0
        for right in range(left, len(changes)):
            total += changes[right]
            if total == target:
                answer += 1
    return answer
