def brute_force(slots: int, requests: list[tuple[int, int]]) -> list[int]:
    return [
        sum(start <= slot < end for start, end in requests)
        for slot in range(slots)
    ]
