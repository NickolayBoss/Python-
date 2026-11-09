"""Минимальная стоимость маршрута: 0–1 BFS и восстановление пути.

Python 3.10+. Координаты функций — с нуля; координаты ввода/вывода — с единицы.
"""

from collections import deque
from collections.abc import Sequence
import sys

# Фиксированный порядок делает выбор одного из оптимальных путей воспроизводимым.
DIRECTIONS = ((-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R"))


def find_route(
    grid: Sequence[str], start: tuple[int, int], target: tuple[int, int]
) -> tuple[int, list[tuple[int, int]]]:
    """Возвращает (минимальная стоимость, путь) или (-1, []).

    Предусловия: непустое прямоугольное поле из UDLR#; start и target
    находятся внутри поля и не являются стенами. Аргументы не изменяются.
    Из нескольких оптимальных путей разрешён любой; число шагов не минимизируется.
    """
    rows, cols = len(grid), len(grid[0])
    count = rows * cols
    source = start[0] * cols + start[1]
    destination = target[0] * cols + target[1]

    # Любой достижимый минимум реализуется простым путём длины <= count - 1.
    infinity = count + 1
    distance = [infinity] * count
    parent = [-1] * count
    distance[source] = 0
    queue = deque([(0, source)])

    while queue:
        current_distance, cell = queue.popleft()
        if current_distance != distance[cell]:
            continue  # устаревшая запись: клетку уже достигли дешевле
        if cell == destination:
            break  # минимальная актуальная метка цели окончательна

        row, col = divmod(cell, cols)
        for dr, dc, direction in DIRECTIONS:
            nr, nc = row + dr, col + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == "#":
                continue

            neighbor = nr * cols + nc
            weight = int(grid[row][col] != direction)
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                parent[neighbor] = cell
                entry = (candidate, neighbor)
                if weight == 0:
                    queue.appendleft(entry)
                else:
                    queue.append(entry)

    if distance[destination] == infinity:
        return -1, []

    path = []
    cell = destination
    while cell != -1:
        path.append(divmod(cell, cols))
        cell = parent[cell]
    path.reverse()
    return distance[destination], path


def solve(data: bytes) -> str:
    """Разбирает корректный ввод и форматирует один допустимый ответ."""
    tokens = iter(data.split())
    rows, cols = int(next(tokens)), int(next(tokens))
    grid = [next(tokens).decode("ascii") for _ in range(rows)]
    start = (int(next(tokens)) - 1, int(next(tokens)) - 1)
    target = (int(next(tokens)) - 1, int(next(tokens)) - 1)
    cost, path = find_route(grid, start, target)
    if cost == -1:
        return "-1"
    lines = [str(cost), str(len(path))]
    lines.extend(f"{row + 1} {col + 1}" for row, col in path)
    return "\n".join(lines)


if __name__ == "__main__":
    print(solve(sys.stdin.buffer.read()))
