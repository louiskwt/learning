def python(n, d):
    """
    Return the length of the longest python of digit d in integer n.
    >>> python(2125262, 2) # positions of 2s: [0,2,4,6] -> all 2 apart -> length 4
    4
    >>> python(2020211202, 2) # positions of 2s: [0,2,4,7,9] -> longest python is 3 (at 0,2,4)
    3
    >>> python(20211120202, 2) # positions of 2s: [0,2,6,8,10] -> longest python is 3 (at 6,8,10)
    3
    >>> python(1010, 0)
    2
    >>> python(123456, 7) # no 7 exists within n
    0
    """
    lengths = []
    while n > 0:
        copied_n = n
        length = 0
        while copied_n % 10 == d and copied_n > 0:
            length += 1
            copied_n = copied_n // 100
        lengths.extend([length])
        n = n // 10
    return max(lengths)


def is_valid(n):
    """
    >>> is_valid(3412) # 1 is two digits to the right of 3, 2 is two digits to the right of 4.
    True
    >>> is_valid(43) # 2 or fewer digits
    True
    >>> is_valid(3443) # No odd number within two digits of leftmost 3.
    False
    >>> is_valid(213) # No even number to the right of 2.
    False
    """
    def helper(last, second, n):
        if n == 0:
            return True
        curr = n % 10
        if curr % 2 != last % 2 and curr % 2 != second % 2:
            return False
        return helper(second, curr, n // 10)
    return helper(n % 10, n // 10 % 10, n // 100)

def shift(k, f):
    """ 
    >>> square = lambda x: x * x
    >>> g = shift(2, square)
    >>> g(3)
    25
    """
    return lambda x: f(x + k)

def num_long_groups(n, k):
    group_size, count = 0, 0
    while n:
        group_size += 1
        if group_size == k:
            count += 1
        if n % 10 % 2 != (n // 10 % 10) % 2:
            group_size = 0
        n = n // 10
    return count

def gap(n, term):
    k, largest = 1, 0
    while k < n:
        largest = max(largest, abs(term(k + 1) - term(k)))
        k = k + 1
    return largest
