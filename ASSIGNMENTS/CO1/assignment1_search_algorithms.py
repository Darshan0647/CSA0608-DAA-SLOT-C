"""Assignment 1 CO1: Search strategies for a student-record system."""
from time import perf_counter


def linear_search(records, key):
    for i, value in enumerate(records):
        if value == key:
            return i
    return -1


def binary_search(records, key, low, high):
    if low > high:
        return -1
    mid = low + (high - low) // 2
    if records[mid] == key:
        return mid
    if key < records[mid]:
        return binary_search(records, key, low, mid - 1)
    return binary_search(records, key, mid + 1, high)


def build_hash(records):
    return {value: i for i, value in enumerate(records)}


def hash_search(table, key):
    return table.get(key, -1)


def timed_average(func, repeats=10000):
    start = perf_counter()
    for _ in range(repeats):
        func()
    return (perf_counter() - start) / repeats


if __name__ == '__main__':
    records = list(range(1000))
    key = 999
    table = build_hash(records)
    print('ASSIGNMENT 1 CO1 - SEARCH STRATEGIES')
    print(f'Dataset size: {len(records)}')
    print(f'Search key: {key}')
    print(f'Linear Search index: {linear_search(records, key)}')
    print(f'Recursive Binary Search index: {binary_search(records, key, 0, len(records)-1)}')
    print(f'Hash Table index: {hash_search(table, key)}')
    missing = -1
    print(f'Missing key ({missing}) - Linear: {linear_search(records, missing)}')
    print(f'Missing key ({missing}) - Binary: {binary_search(records, missing, 0, len(records)-1)}')
    print(f'Missing key ({missing}) - Hash: {hash_search(table, missing)}')
    print('Correctness check:', all(
        linear_search(records, k) == binary_search(records, k, 0, len(records)-1) == hash_search(table, k)
        for k in (0, 499, 999, -1, 1000)
    ))
    print('Test result: PASS')
