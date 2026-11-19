"""Независимый квадратичный эталон для коротких корректных по алфавиту строк."""


def first_bracket_error_reduction(sequence: str) -> int | None:
    remaining = list(enumerate(sequence, start=1))
    while True:
        reduced = []
        index = 0
        while index < len(remaining):
            if (index + 1 < len(remaining)
                    and remaining[index][1] + remaining[index + 1][1]
                    in ('()', '[]', '{}')):
                index += 2
            else:
                reduced.append(remaining[index])
                index += 1
        if len(reduced) == len(remaining):
            break
        remaining = reduced
    for position, bracket in remaining:
        if bracket in ')]}':
            return position
    return remaining[0][0] if remaining else None
