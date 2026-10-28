def coin_combinations(coins: list[int], target: int) -> None:
    """Print all ways to reach target using at least one of each coin in `coins`.
    
    >>> coin_combinations([25, 10, 5], 40)
    [1 x 25c][1 x 10c][1 x 5c]
    
    >>> coin_combinations([10, 5], 25)
    [1 x 10c][3 x 5c]
    [2 x 10c][1 x 5c]
    """
    def backtrack(remaining_coins: list[int], amount_left: int, solution: str) -> None:
        # Base Case 1: Valid combination found
        if remaining_coins == [] and amount_left == 0:
            print(solution)
            return

        # Base Case 2: Out of coins or amount dropped below zero
        if not remaining_coins or amount_left <= 0:
            return

        current_coin = remaining_coins[0]

        # Determine the loop range for 'count' (number of current_coins to use)
        # Hint: Must use at least 1 coin, and cannot exceed amount_left
        for count in range(1, (target // current_coin) + 1):
            
            # Format display string for current selection
            item_str = f"[{count} x {current_coin}c]"
            
            # Recursive call: move to remaining coins, update amount, update solution string
            backtrack(
                remaining_coins[1:],             # remaining coins
                amount_left - (current_coin * count),             # new amount left
                solution + item_str              # updated solution string
            )

    backtrack(coins, target, "")