def knapsack(items, capacity):
    scale = 100  # handles weights like 0.01 kg (1 gram)
    cap_int = int(round(capacity * scale))
    scaled_items = []
    for name, w, v in items:
        scaled_items.append((name, int(round(w * scale)), v))

    n = len(scaled_items)
    dp = [[0] * (cap_int + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, weight, value = scaled_items[i - 1]
        for w in range(cap_int + 1):
            if weight > w:
                dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)

    total_value = dp[n][cap_int]
    w = cap_int
    chosen = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            name, weight, _ = scaled_items[i - 1]
            chosen.append(name)
            w -= weight

    return total_value, chosen[::-1]


def main():
    print("=== Trip Packing Helper ===")
    capacity = float(input("Backpack weight limit (kg): "))

    items = []
    while True:
        name = input("\nItem name (or 'done' to finish): ")
        if name.lower() == 'done':
            break
        weight = float(input(f"Weight of '{name}' (kg): "))
        value = int(input(f"Usefulness (1-10) for '{name}': "))
        items.append((name, weight, value))

    if not items:
        print("No items added. Exiting.")
        return

    total_value, chosen_items = knapsack(items, capacity)

    print("\n--- Optimal Packing ---")
    print(f"Total usefulness: {total_value}")
    total_weight = sum(w for n, w, v in items if n in chosen_items)
    print(f"Total weight: {total_weight:.2f} kg")
    print("Items to take:")
    for name in chosen_items:
        print(f"  - {name}")


if __name__ == "__main__":
    main()