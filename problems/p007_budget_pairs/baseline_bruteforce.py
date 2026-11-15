from itertools import combinations


def count_pairs_bruteforce(prices: list[int], budget: int) -> int:
    return sum(first + second <= budget for first, second in combinations(prices, 2))
