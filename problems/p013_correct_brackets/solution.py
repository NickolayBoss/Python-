"""Первая ошибка в строке из круглых, квадратных и фигурных скобок."""

import sys


def first_bracket_error(sequence: str) -> int | None:
    """Позиция ошибки с единицы; None для правильной последовательности.

    Предусловие: sequence состоит только из ()[]{}.
    При отсутствии ошибочной закрывающей возвращается самая ранняя
    незакрытая открывающая скобка.
    """
    matching_open = {')': '(', ']': '[', '}': '{'}
    stack: list[tuple[str, int]] = []
    for position, bracket in enumerate(sequence, start=1):
        if bracket in '([{':
            stack.append((bracket, position))
        else:
            if not stack or stack[-1][0] != matching_open[bracket]:
                return position
            stack.pop()
    return stack[0][1] if stack else None


def main() -> None:
    raw = sys.stdin.buffer.readline()
    if not raw:
        raise ValueError('Ожидалась строка скобок, хотя бы пустая')
    if raw.endswith(b'\n'):
        raw = raw[:-1]
        if raw.endswith(b'\r'):
            raw = raw[:-1]
    sequence = raw.decode('ascii')
    answer = first_bracket_error(sequence)
    print('Success' if answer is None else answer)


if __name__ == '__main__':
    main()
