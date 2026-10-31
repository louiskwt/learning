def count_partitions(n, m):
        """Count the ways to partition n using parts up to m."""
        if n == 0:
            return 1
        elif n < 0:
            return 0
        elif m == 0:
            return 0
        else:
            return count_partitions(n-m, m) + count_partitions(n, m-1)

# DP Knapsack
from functools import lru_cache

def knapsack(weights, values, c):
    @lru_cache(maxsize=None)
    def sack_partitions(i, current_c):
        # Inspect cache performance (hits, misses, current size)
        if current_c <= 0 or i >= len(weights):
            return 0
        
        if weights[i] <= current_c:
            include = values[i] + sack_partitions(i + 1, current_c - weights[i])
            exclude = sack_partitions(i + 1, current_c)
            return max(include, exclude)
        else:
            return sack_partitions(i + 1, current_c)

    result = sack_partitions(0, c)
    print(sack_partitions.cache_info())
    return result

w = [2, 6, 3, 3]
v = [1, 5, 3, 3]

a = knapsack(w, v, 6)
print(a)
