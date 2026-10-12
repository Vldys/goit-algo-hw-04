"""Compare insertion sort, merge sort and Python's Timsort with timeit."""
import random
import statistics
import timeit


def insertion_sort(items: list[int]) -> list[int]:
    result = items.copy()
    for index in range(1, len(result)):
        value = result[index]
        position = index - 1
        while position >= 0 and result[position] > value:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = value
    return result


def merge_sort(items: list[int]) -> list[int]:
    if len(items) <= 1:
        return items.copy()
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def create_data(kind: str, size: int, rng: random.Random) -> list[int]:
    if kind == 'random':
        return [rng.randint(0, size * 10) for _ in range(size)]
    if kind == 'sorted':
        return list(range(size))
    if kind == 'reversed':
        return list(range(size, 0, -1))
    if kind == 'nearly_sorted':
        result = list(range(size))
        for _ in range(max(1, size // 100)):
            a, b = rng.randrange(size), rng.randrange(size)
            result[a], result[b] = result[b], result[a]
        return result
    raise ValueError(kind)


def benchmark(repeats: int = 3) -> None:
    rng = random.Random(42)
    methods = {'Insertion sort': insertion_sort, 'Merge sort': merge_sort, 'Timsort (sorted)': sorted}
    print(f"{'Тип даних':<16} {'N':>6} {'Insertion':>12} {'Merge':>12} {'Timsort':>12}")
    print('-' * 65)
    for kind in ('random', 'sorted', 'reversed', 'nearly_sorted'):
        for size in (100, 1000, 5000):
            data = create_data(kind, size, rng)
            expected = sorted(data)
            results = {}
            for name, func in methods.items():
                assert func(data) == expected, f"Некоректне сортування: {name}"
                timings = timeit.repeat(lambda: func(data), repeat=repeats, number=1)
                results[name] = statistics.median(timings) * 1000
            print(f"{kind:<16} {size:>6} {results['Insertion sort']:>12.3f} "
                  f"{results['Merge sort']:>12.3f} {results['Timsort (sorted)']:>12.3f}")
    print('Час у мілісекундах (медіана трьох запусків). Менше — краще.')


if __name__ == '__main__':
    benchmark()
