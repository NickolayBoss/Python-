"""Офлайн-запросы связности: сортировка и DSU. Python 3.10+."""

import sys
from collections.abc import Sequence


class DisjointSetUnion:
    """DSU активных клеток: сжатие путей и объединение по размеру."""

    def __init__(self, count: int) -> None:
        self.parent = [-1] * count  # -1 означает неактивную клетку
        self.size = [0] * count
        self.components = 0
        self.largest = 0

    def activate(self, cell: int) -> None:
        """Вызывается ровно один раз для каждой клетки."""
        self.parent[cell] = cell
        self.size[cell] = 1
        self.components += 1
        self.largest = max(self.largest, 1)

    def find(self, cell: int) -> int:
        """Находит представителя активной клетки, сокращая путь к корню."""
        while self.parent[cell] != cell:
            self.parent[cell] = self.parent[self.parent[cell]]
            cell = self.parent[cell]
        return cell

    def union(self, first: int, second: int) -> None:
        first = self.find(first)
        second = self.find(second)
        if first == second:
            return  # уже одна сеть: счётчик уменьшать нельзя
        if self.size[first] < self.size[second]:
            first, second = second, first
        self.parent[second] = first
        self.size[first] += self.size[second]
        self.components -= 1
        self.largest = max(self.largest, self.size[first])


def analyze_network(
    grid: Sequence[Sequence[int]], thresholds: Sequence[int]
) -> list[tuple[int, int]]:
    """Возвращает (число сетей, максимальный размер) в порядке запросов.

    Предусловия: непустая прямоугольная сетка; целочисленные значения.
    Ввод соответствует ограничениям задачи; функция не меняет аргументы.
    """
    rows, cols = len(grid), len(grid[0])
    values = [value for row in grid for value in row]
    cells = sorted(range(rows * cols), key=values.__getitem__, reverse=True)
    queries = sorted(range(len(thresholds)), key=thresholds.__getitem__, reverse=True)
    dsu = DisjointSetUnion(rows * cols)
    answers = [(0, 0)] * len(thresholds)
    next_cell = 0

    for query in queries:
        threshold = thresholds[query]
        while next_cell < len(cells) and values[cells[next_cell]] >= threshold:
            cell = cells[next_cell]
            next_cell += 1
            dsu.activate(cell)
            row, col = divmod(cell, cols)
            # Проверяем все четыре направления, а не только вверх и влево:
            # порядок активации зависит от устойчивости, а не от координат.
            for nr, nc in (
                (row - 1, col), (row + 1, col),
                (row, col - 1), (row, col + 1),
            ):
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor = nr * cols + nc
                    if dsu.parent[neighbor] != -1:
                        dsu.union(cell, neighbor)
        answers[query] = (dsu.components, dsu.largest)
    return answers


def solve(data: bytes) -> str:
    """Разбирает корректный конкурсный ввод и формирует ответ."""
    numbers = iter(map(int, data.split()))
    rows, cols, count = next(numbers), next(numbers), next(numbers)
    grid = [[next(numbers) for _ in range(cols)] for _ in range(rows)]
    thresholds = [next(numbers) for _ in range(count)]
    return "\n".join(
        f"{components} {largest}"
        for components, largest in analyze_network(grid, thresholds)
    )


if __name__ == "__main__":
    print(solve(sys.stdin.buffer.read()))
