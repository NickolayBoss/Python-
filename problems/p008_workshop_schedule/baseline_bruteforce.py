from itertools import combinations


def brute_force(meetings: list[tuple[int, int]]) -> int:
    for size in range(len(meetings), 0, -1):
        for candidate in combinations(meetings, size):
            ordered = sorted(candidate)
            if all(first[1] <= second[0] for first, second in zip(ordered, ordered[1:])):
                return size
    return 0
