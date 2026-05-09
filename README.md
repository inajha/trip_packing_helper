# 🎒 Trip Packing Helper

A command‑line tool that uses the **0/1 knapsack dynamic programming** algorithm to help you pack the most valuable (useful) set of items for a trip, without exceeding your backpack’s weight limit.

## 🔍 Problem It Solves

You have a weight limit and a list of items (each with a weight and a “usefulness” score 1–10). The program finds the optimal combination that maximizes total usefulness while staying within the weight limit.

## 🧠 Algorithm

- **Dynamic Programming** (0/1 knapsack)
- Time complexity: `O(n × capacity)` after scaling weights to integers.
- Space complexity: `O(n × capacity)` – can be optimised to `O(capacity)`.

## 🚀 How to Use

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/trip-packing-helper.git
   cd trip-packing-helper
   ```

## 📦 Example Inputs

Backpack weight limit (kg): 5

Item name: Laptop
Weight: 2
Usefulness: 9

Item name: Headphones
Weight: 1
Usefulness: 4

Item name: Water bottle
Weight: 3
Usefulness: 8

Item name: Book
Weight: 4
Usefulness: 6

Item name: done

--- Optimal Packing ---
Total usefulness: 17
Total weight: 5.00 kg
Items to take:
  - Laptop
  - Water bottle


