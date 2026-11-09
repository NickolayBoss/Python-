"""Бинарный поиск по ответу и жадная проверка. Python 3.10+."""

from collections.abc import Sequence
import sys


def can_finish(durations: Sequence[int], workers: int, limit: int) -> bool:
    """Можно ли разделить очередь на <= workers блоков с суммой <= limit?

    Предусловия: непустая последовательность положительных длительностей,
    workers >= 1. Последовательность не изменяется.
    """
    used = 1
    current = 0
    for duration in durations:
        if duration > limit:
            return False  # одно неделимое задание уже превышает лимит
        if current + duration > limit:
            used += 1
            current = duration
            if used > workers:
                return False
        else:
            current += duration
    return True


def minimum_time(durations: Sequence[int], workers: int) -> int:
    """Минимум максимальной суммы блока при сохранении порядка заданий.

    Предусловия: 1 <= workers <= len(durations); длительности положительны.
    """
    left, right = max(durations), sum(durations)
    while left < right:
        middle = (left + right) // 2
        if can_finish(durations, workers, middle):
            right = middle
        else:
            left = middle + 1
    return left


def solve(data: bytes) -> str:
    """Разбирает корректный конкурсный ввод; возвращает единственный ответ."""
    numbers = iter(map(int, data.split()))
    count, workers = next(numbers), next(numbers)
    durations = [next(numbers) for _ in range(count)]
    return str(minimum_time(durations, workers))


if __name__ == "__main__":
    print(solve(sys.stdin.buffer.read()))
