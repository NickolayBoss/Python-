"""Независимое эталонное решение: BFS заново для каждого запроса."""

import sys
from collections import deque
from collections.abc import Sequence


def analyze_network_bfs(
    grid: Sequence[Sequence[int]], thresholds: Sequence[int]
) -> list[tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    answers = []
    for threshold in thresholds:
        visited = [[False] * cols for _ in range(rows)]
        components = largest = 0
        for row in range(rows):
            for col in range(cols):
                if visited[row][col] or grid[row][col] < threshold:
                    continue
                components += 1
                visited[row][col] = True
                queue = deque([(row, col)])
                area = 0
                while queue:
                    r, c = queue.popleft()
                    area += 1
                    for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if not visited[nr][nc] and grid[nr][nc] >= threshold:
                                visited[nr][nc] = True
                                queue.append((nr, nc))
                largest = max(largest, area)
        answers.append((components, largest))
    return answers


def solve(data: bytes) -> str:
    numbers = iter(map(int, data.split()))
    rows, cols, count = next(numbers), next(numbers), next(numbers)
    grid = [[next(numbers) for _ in range(cols)] for _ in range(rows)]
    thresholds = [next(numbers) for _ in range(count)]
    return "\n".join(
        f"{components} {largest}"
        for components, largest in analyze_network_bfs(grid, thresholds)
    )


if __name__ == "__main__":
    print(solve(sys.stdin.buffer.read()))
