"""Префиксные суммы и частоты ранее встреченных префиксов. Python 3.10+."""
from collections.abc import Iterable
import sys


def count_segments(changes: Iterable[int], target: int) -> int:
    """Число непустых непрерывных фрагментов с суммой target.

    Принимает в том числе одноразовый итератор, не изменяет источник.
    Ожидаемое время O(n), дополнительная память O(n).
    """
    frequencies = {0: 1}  # пустой префикс до первого элемента
    prefix = answer = 0
    for change in changes:
        prefix += change
        answer += frequencies.get(prefix - target, 0)
        # Добавляем текущий префикс после запроса, чтобы не считать пустой отрезок.
        frequencies[prefix] = frequencies.get(prefix, 0) + 1
    return answer


def solve(data: bytes) -> str:
    numbers = iter(map(int, data.split()))
    count, target = next(numbers), next(numbers)
    changes = (next(numbers) for _ in range(count))
    return str(count_segments(changes, target))


if __name__ == '__main__':
    print(solve(sys.stdin.buffer.read()))
