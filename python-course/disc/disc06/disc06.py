from functools import reduce

def gen_fib():
    n, add = 0, 1
    while True:
        yield n
        n, add = n + add, n

next(filter(lambda n: n < 2026, gen_fib()))

def repeated(t, k):
    """Return the first value in iterator t that appears k times in a row,
    calling next on t as few times as possible.

    >>> s = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(s, 2)
    9
    >>> t = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(t, 3)
    8
    >>> u = iter([3, 2, 2, 2, 1, 2, 1, 4, 4, 5, 5, 5])
    >>> repeated(u, 3)
    2
    >>> repeated(u, 3)
    5
    >>> v = iter([4, 1, 6, 6, 7, 7, 8, 8, 2, 2, 2, 5])
    >>> repeated(v, 3)
    2
    """
    assert k > 1, "k must be larger than 1"
    count, current_val = 1, next(t) 
    while count < k: 
        next_val = next(t)
        if current_val == next_val:
            count += 1
        else:
            count, current_val = 1, next_val
    return current_val


def differences(t):
    """Yield the differences between adjacent values from iterator t.

    >>> list(differences(iter([5, 2, -100, 103])))
    [-3, -102, 203]
    >>> next(differences(iter([39, 100])))
    61
    """
    try:
        current_val = next(t)
        while True:
            adj_val = next(t)
            diff = adj_val - current_val
            yield diff
            current_val = adj_val
    except StopIteration:
        pass

def partition_gen(n, m):
    """Yield the partitions of n using parts up to size m.
    >>> for partition in sorted(partition_gen(6, 4)):
    ...     print(partition)
    1 + 1 + 1 + 1 + 1 + 1
    1 + 1 + 1 + 1 + 2
    1 + 1 + 1 + 3
    1 + 1 + 2 + 2
    1 + 1 + 4
    1 + 2 + 3
    2 + 2 + 2
    2 + 4
    3 + 3
    """
    assert n > 0 and m > 0
    if n == m:
        yield f"{n}"
    if n - m > 0:
        for p in partition_gen(n - m, m):
            yield p + " + " + f"{m}"
    if m > 1:
        yield from partition_gen(n, m - 1)


def squares(total, k):
    """Yield the ways in which perfect squares greater or equal to k*k sum to total.

    >>> list(squares(10, 1))  # All lists of perfect squares that sum to 10
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [4, 1, 1, 1, 1, 1, 1], [4, 4, 1, 1], [9, 1]]
    >>> list(squares(20, 2))  # Only use perfect squares greater or equal to 4 (2*2).
    [[4, 4, 4, 4, 4], [16, 4]]
    """
    assert total > 0 and k > 0
    if total == k * k:
        yield [k * k] 
    elif total > k * k:
        for rest in squares(total - k * k, k):
            yield rest + [k * k]
        yield from squares(total, k + 1)


def church_generator(f):
    """Takes in a function f and yields functions which apply f
    to their argument one more time than the previously generated
    function.

    >>> increment = lambda x: x + 1
    >>> church = church_generator(increment)
    >>> for _ in range(5):
    ...     fn = next(church)
    ...     print(fn(0))
    0
    1
    2
    3
    4
    """
    g = 0 
    while True:
        yield lambda n: reduce(lambda acc, _: f(acc), range(g), n)
        g += 1
