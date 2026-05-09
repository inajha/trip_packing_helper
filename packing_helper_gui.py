import tkinter as tk
from tkinter import messagebox, ttk

def knapsack(items, capacity):
    scale = 100
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


class PackingHelperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trip Packing Helper")
        self.root.geometry("650x550")
        self.items = []

        # --- Weight Limit Frame ---
        limit_frame = tk.LabelFrame(root, text="Backpack Limit", padx=10, pady=10)
        limit_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(limit_frame, text="Weight (kg):").grid(row=0, column=0, sticky="e")
        self.capacity_entry = tk.Entry(limit_frame, width=10)
        self.capacity_entry.grid(row=0, column=1, padx=5)
        self.capacity_entry.insert(0, "5")

        # --- Add Item Frame ---
        add_frame = tk.LabelFrame(root, text="Add New Item", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(add_frame, width=15)
        self.name_entry.grid(row=0, column=1, padx=5)
        self.name_entry.bind("<Return>", lambda e: self.weight_entry.focus())  # Enter moves to weight

        tk.Label(add_frame, text="Weight (kg):").grid(row=0, column=2, sticky="e")
        self.weight_entry = tk.Entry(add_frame, width=8)
        self.weight_entry.grid(row=0, column=3, padx=5)
        self.weight_entry.bind("<Return>", lambda e: self.value_entry.focus())

        tk.Label(add_frame, text="Usefulness (1-10):").grid(row=0, column=4, sticky="e")
        self.value_entry = tk.Entry(add_frame, width=5)
        self.value_entry.grid(row=0, column=5, padx=5)
        self.value_entry.bind("<Return>", lambda e: self.add_item())  # Enter adds item

        self.add_btn = tk.Button(add_frame, text="Add Item", command=self.add_item)
        self.add_btn.grid(row=0, column=6, padx=10)

        # --- Items List Frame ---
        list_frame = tk.LabelFrame(root, text="Items in Your Packing List", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Name", "Weight (kg)", "Usefulness")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Delete button
        self.del_btn = tk.Button(list_frame, text="Delete Selected Item", command=self.delete_item)
        self.del_btn.pack(pady=5)

        # --- Solve Button ---
        self.solve_btn = tk.Button(root, text="Find Optimal Packing", command=self.solve, bg="lightblue", font=("Arial", 10, "bold"))
        self.solve_btn.pack(pady=10)

        # --- Results Frame ---
        result_frame = tk.LabelFrame(root, text="Optimal Packing Result", padx=10, pady=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_text = tk.Text(result_frame, height=8, wrap="word")
        self.result_text.pack(fill="both", expand=True)

    def add_item(self):
        name = self.name_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        value_str = self.value_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Please enter an item name.")
            return
        try:
            weight = float(weight_str)
            value = int(value_str)
            if weight <= 0:
                raise ValueError
            if value < 1 or value > 10:
                messagebox.showerror("Error", "Usefulness must be between 1 and 10.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for weight (positive) and usefulness (1-10).")
            return

        self.items.append((name, weight, value))
        self.tree.insert("", "end", values=(name, f"{weight:.2f}", value))
        # Clear entry fields
        self.name_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.name_entry.focus()  # Ready for next item

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an item to delete.")
            return
        for item in selected:
            values = self.tree.item(item, "values")
            name = values[0]
            for i, (n, w, v) in enumerate(self.items):
                if n == name and f"{w:.2f}" == values[1] and v == int(values[2]):
                    del self.items[i]
                    break
            self.tree.delete(item)

    def solve(self):
        if not self.items:
            messagebox.showinfo("No Items", "Please add some items first.")
            return
        try:
            capacity = float(self.capacity_entry.get().strip())
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a positive weight limit.")
            return

        total_value, chosen_names = knapsack(self.items, capacity)

        total_weight = 0.0
        chosen_details = []
        for name, w, v in self.items:
            if name in chosen_names:
                total_weight += w
                chosen_details.append((name, w, v))

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Total usefulness: {total_value}\n")
        self.result_text.insert(tk.END, f"Total weight: {total_weight:.2f} kg\n")
        self.result_text.insert(tk.END, f"Weight limit: {capacity:.2f} kg\n\n")
        self.result_text.insert(tk.END, "Items to take:\n")
        for name, w, v in chosen_details:
            self.result_text.insert(tk.END, f"  - {name} ({w:.2f} kg, usefulness {v})\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = PackingHelperApp(root)
    root.mainloop()