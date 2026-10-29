"""
Q1 Representing Expressions

(+ 1 (* 2 3))

(and (< 1 0) (/ 1 0))

Q2 Evaluation

if 
<
x
0
- 
x
"""

def print_evals(expr):
        """Print the expressions that are evaluated while evaluating expr.

        expr: a Scheme expression containing only (, ), +, *, and numbers.

        >>> nested_expr = Link('+', Link(Link('*', Link(3, Link(4, nil))), Link(5, nil)))
        >>> print_evals(nested_expr)
        (+ (* 3 4) 5)
        +
        (* 3 4)
        *
        3
        4
        5
        >>> print_evals(Link('*', Link(6, Link(7, Link(nested_expr, Link(8, nil))))))
        (* 6 7 (+ (* 3 4) 5) 8)
        *
        6
        7
        (+ (* 3 4) 5)
        +
        (* 3 4)
        *
        3
        4
        5
        8
        """
        if not isinstance(expr, Link):
            return
        print(expr)
        while expr is not nil:
            if isinstance(expr.first, Link):
                print_evals(expr.first)
            else:
                print(expr.first)
            expr = expr.rest
    

class Link:
    """A linked list.
    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    (5 7 (8 9))
    >>> print(Link(9, 10))
    (9 . 10)
    >>> print(Link(s, 10))
    ((5 7 (8 9)) . 10)
    >>> print(Link.empty)
    ()
    >>> print(Link(Link.empty))
    (())
    """
    empty = ()

    def __init__(self, first, rest=empty):
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is Link.empty:
            rest_repr = ''
        else:
            rest_repr = ', ' + repr(self.rest)
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        s = '(' + repl_str(self.first)
        rest = self.rest
        while isinstance(rest, Link):
            s += ' ' + repl_str(rest.first)
            rest = rest.rest
        if rest is not Link.empty:
            s += ' . ' + repl_str(rest)
        return s + ')'

nil = Link.empty

def repl_str(val):
    """Show the value in the Scheme REPL."""
    if val is True:
        return "#t"
    if val is False:
        return "#f"
    if val is None:
        return "undefined"
    if isinstance(val, str) and val and val[0] == "\"":
        return "\"" + repr(val[1:-1])[1:-1] + "\""
    return str(val)

def len_link(s):
    """Return the length of a linked list.
    >>> len_link(Link(1, Link(2, Link(3))))
    3
    >>> len_link(Link.empty)
    0
    """
    result = 0
    while isinstance(s, Link):
        result, s = result + 1, s.rest
    return result

def map_link(f, s):
    """Map function f over linked list s.
    >>> square = lambda x: x * x
    >>> map_link(square, Link(1, Link(2, Link(3))))
    Link(1, Link(4, Link(9)))
    """
    if s is Link.empty:
        return s
    return Link(f(s.first), map_link(f, s.rest))