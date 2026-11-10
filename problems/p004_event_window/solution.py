"""Самый длинный фрагмент с не более k типами: скользящее окно."""
from collections.abc import Sequence
import sys


def longest_window(events: Sequence[int], limit: int) -> tuple[int, int]:
    """Возвращает границы [left, right) с нуля; при равенстве — самый ранний.

    Предусловие: limit >= 0. Для пустого ответа возвращает (0, 0).
    Не изменяет вход. Ожидаемое время O(n) при стандартной модели хеширования.
    """
    counts: dict[int, int] = {}
    left = best_left = best_right = 0
    for right, event in enumerate(events):
        counts[event] = counts.get(event, 0) + 1
        while len(counts) > limit:
            removed = events[left]
            counts[removed] -= 1
            if counts[removed] == 0:
                del counts[removed]
            left += 1
        if right + 1 - left > best_right - best_left:
            best_left, best_right = left, right + 1
    return best_left, best_right


def solve(data: bytes) -> str:
    numbers = iter(map(int, data.split()))
    count, limit = next(numbers), next(numbers)
    events = [next(numbers) for _ in range(count)]
    left, right = longest_window(events, limit)
    if left == right:
        return "0\n0 0"
    return f"{right - left}\n{left + 1} {right}"


if __name__ == "__main__":
    print(solve(sys.stdin.buffer.read()))
