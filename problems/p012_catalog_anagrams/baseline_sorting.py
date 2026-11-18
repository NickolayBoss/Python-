"""Независимый эталон: сортируем все символы каждой строки."""

from collections.abc import Iterable


def group_anagrams_sorting(names: Iterable[str]) -> list[list[int]]:
    groups: dict[str, list[int]] = {}
    for index, name in enumerate(names, start=1):
        key = "".join(sorted(name))
        if key not in groups:
            groups[key] = []
        groups[key].append(index)
    return list(groups.values())
