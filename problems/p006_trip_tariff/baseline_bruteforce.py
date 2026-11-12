"""Эталон для малых входов: просмотр всех тарифов для каждой поездки."""
from collections.abc import Iterable, Sequence


def cheapest_tariffs_bruteforce(
    tariffs: Sequence[tuple[int, int]], trips: Iterable[int]
) -> list[int]:
    return [
        min((price for limit, price in tariffs if limit >= distance), default=-1)
        for distance in trips
    ]
