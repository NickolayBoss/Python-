"""Группировка по частотам символов с сохранением порядка записей."""

from collections import Counter
from collections.abc import Iterable
import sys


def anagram_key(name: str) -> tuple[tuple[str, int], ...]:
    """Каноническая неизменяемая запись состава строки."""
    return tuple(sorted(Counter(name).items()))


def group_anagrams(names: Iterable[str]) -> list[list[int]]:
    """Индексы с единицы; группы упорядочены по первому появлению."""
    groups: dict[tuple[tuple[str, int], ...], list[int]] = {}
    for index, name in enumerate(names, start=1):
        key = anagram_key(name)
        if key not in groups:
            groups[key] = []
        groups[key].append(index)
    return list(groups.values())


def main() -> None:
    stream = sys.stdin.buffer
    count = int(stream.readline())

    def read_names() -> Iterable[str]:
        for _ in range(count):
            raw = stream.readline()
            if not raw:
                raise ValueError("Недостаточно строк каталога")
            # Удаляем только разделитель записей; пробелы значимы.
            if raw.endswith(b"\n"):
                raw = raw[:-1]
                if raw.endswith(b"\r"):
                    raw = raw[:-1]
            yield raw.decode("utf-8")

    groups = group_anagrams(read_names())
    print(len(groups))
    for group in groups:
        print(len(group), *group)


if __name__ == "__main__":
    main()
