from operator import sub, mul

def skip_factorial(n):
    """Return the product of positive integers n * (n - 2) * (n - 4) * ...

    >>> skip_factorial(5) # 5 * 3 * 1
    15
    >>> skip_factorial(8) # 8 * 6 * 4 * 2
    384
    """
    if n <= 1:
        return 1
    else:
        return n * skip_factorial(n - 2)


def swipe(n):
    """Print the digits of n, one per line, first backward then forward.

    >>> swipe(2837)
    7
    3
    8
    2
    8
    3
    7
    """
    if n < 10:
        print(n)
    else:
        print(n % 10)
        swipe(n // 10)
        print(n % 10)


def is_prime(n):
    """Returns True if n is a prime number and False otherwise.
    >>> is_prime(2)
    True
    >>> is_prime(16)
    False
    >>> is_prime(521)
    True
    >>> is_prime(42)
    False
    >>> is_prime(100003)
    True
    """
    def has_divisor(d):
        """Returns True if d equals n and False if d is smaller than n but n is divisible by d"""
        if d ** 2 > n:
            return True
        elif n % d == 0:
            return False
        else:
            return has_divisor(d + 1)
    return has_divisor(2)


def hailstone(n):
    """Print out the hailstone sequence starting at n, 
    and return the number of elements in the sequence.
    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    >>> b = hailstone(1)
    1
    >>> b
    1
    """
    print(n)
    if n % 2 == 0:
        return even(n)
    else:
        return odd(n)


def even(n):
    return hailstone(n // 2) + 1


def odd(n):
    if n == 1:
        return n
    else:
        return hailstone(n * 3 + 1) + 1


def sevens(n, k):
    """Return the (clockwise) position of who says n among k players.

    >>> sevens(2, 5)
    2
    >>> sevens(6, 5)
    1
    >>> sevens(7, 5)
    2
    >>> sevens(8, 5)
    1
    >>> sevens(9, 5)
    5
    >>> sevens(18, 5)
    2
    """
    def f(i, who, direction):
        if i == n:
            return who
        else:
            if has_seven(i) or i % 7 == 0:
                direction = -direction

            next_who = who + direction
            
            if next_who > k:
                next_who = 1
            if next_who <= 0:
                next_who = k

            return f(i + 1, next_who, direction)
    return f(1, 1, 1)


def has_seven(n):
    if n == 0:
        return False
    elif n % 10 == 7:
        return True
    else:
        return has_seven(n // 10)



def Y(f):
    """The Y ("paradoxical") combinator."""
    return f(lambda: Y(f))

def Y_tester():
    """
    >>> tmp = Y_tester()
    >>> tmp(1)
    1
    >>> tmp(5)
    120
    >>> tmp(2)
    2
    """
    return Y(lambda future_y: lambda n: 1 if n == 1 or n == 0 else mul(n, future_y()(sub(n, 1))))  # Replace 