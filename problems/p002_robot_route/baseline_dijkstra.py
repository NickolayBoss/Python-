"""Независимый эталон стоимости: Дейкстра с бинарной кучей.

Возвращает только стоимость; используется для сравнения с 0–1 BFS.
Соседи и расстояния представлены иначе, чем в основном решении.
"""

from collections.abc import Sequence
from heapq import heappop, heappush
from math import inf


def minimum_cost_dijkstra(
    grid: Sequence[str], start: tuple[int, int], target: tuple[int, int]
) -> int:
    """Предусловия поля и координат совпадают с find_route."""
    rows, cols = len(grid), len(grid[0])
    distances = [[inf] * cols for _ in range(rows)]
    distances[start[0]][start[1]] = 0
    heap = [(0, start[0], start[1])]

    while heap:
        cost, row, col = heappop(heap)
        if cost != distances[row][col]:
            continue
        if (row, col) == target:
            return cost
        for nr, nc, direction in (
            (row - 1, col, "U"), (row + 1, col, "D"),
            (row, col - 1, "L"), (row, col + 1, "R"),
        ):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                next_cost = cost + (grid[row][col] != direction)
                if next_cost < distances[nr][nc]:
                    distances[nr][nc] = next_cost
                    heappush(heap, (next_cost, nr, nc))
    return -1
