
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

# Hardcoded sample stock prices (USD per share)
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 170.00,
    "MSFT": 420.00,
    "AMZN": 190.00
}

portfolio = []

# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("Stock Portfolio Tracker")
root.geometry("800x620")
root.minsize(700, 560)
root.configure(bg="#f2f5fa")

# ---------------- HEADER ----------------

header = tk.Frame(root, bg="#172b4d", pady=18)
header.pack(fill="x")

tk.Label(
    header,
    text="STOCK PORTFOLIO TRACKER",
    font=("Arial", 22, "bold"),
    bg="#172b4d",
    fg="white"
).pack()

tk.Label(
    header,
    text="Manage your investments in one place",
    font=("Arial", 11),
    bg="#172b4d",
    fg="#dbeafe"
).pack(pady=4)

# ---------------- INPUT AREA ----------------

input_frame = tk.LabelFrame(
    root,
    text=" Add Stock Investment ",
    font=("Arial", 12, "bold"),
    bg="#f2f5fa",
    fg="#172b4d",
    padx=15,
    pady=12
)
input_frame.pack(fill="x", padx=20, pady=15)

tk.Label(
    input_frame, text="Stock Symbol:",
    font=("Arial", 11), bg="#f2f5fa"
).grid(row=0, column=0, padx=8, pady=8, sticky="w")

stock_var = tk.StringVar()

stock_combo = ttk.Combobox(
    input_frame,
    textvariable=stock_var,
    values=list(STOCK_PRICES.keys()),
    state="readonly",
    width=15,
    font=("Arial", 11)
)
stock_combo.grid(row=0, column=1, padx=8, pady=8)
stock_combo.current(0)

tk.Label(
    input_frame, text="Quantity:",
    font=("Arial", 11), bg="#f2f5fa"
).grid(row=0, column=2, padx=8, pady=8)

quantity_entry = tk.Entry(
    input_frame, width=12, font=("Arial", 11)
)
quantity_entry.grid(row=0, column=3, padx=8, pady=8)

# ---------------- PORTFOLIO TABLE ----------------

table_frame = tk.LabelFrame(
    root,
    text=" Your Investments ",
    font=("Arial", 12, "bold"),
    bg="#f2f5fa",
    fg="#172b4d",
    padx=10,
    pady=10
)
table_frame.pack(fill="both", expand=True, padx=20, pady=5)

columns = ("symbol", "price", "quantity", "total")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=9
)

tree.heading("symbol", text="Stock")
tree.heading("price", text="Price / Share ($)")
tree.heading("quantity", text="Quantity")
tree.heading("total", text="Investment Value ($)")

tree.column("symbol", width=100, anchor="center")
tree.column("price", width=150, anchor="center")
tree.column("quantity", width=100, anchor="center")
tree.column("total", width=190, anchor="center")

tree.pack(fill="both", expand=True)

# ---------------- TOTAL VALUE ----------------

total_label = tk.Label(
    root,
    text="Total Investment: $0.00",
    font=("Arial", 17, "bold"),
    bg="#f2f5fa",
    fg="#198754"
)
total_label.pack(pady=12)

# ---------------- FUNCTIONS ----------------

def update_total():
    total = sum(item["total"] for item in portfolio)
    total_label.config(text=f"Total Investment: ${total:,.2f}")


def add_stock():
    symbol = stock_var.get()

    try:
        quantity = int(quantity_entry.get().strip())

        if quantity <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a positive whole number for quantity."
        )
        return

    price = STOCK_PRICES[symbol]
    investment = price * quantity

    portfolio.append({
        "symbol": symbol,
        "price": price,
        "quantity": quantity,
        "total": investment
    })

    tree.insert(
        "",
        "end",
        values=(
            symbol,
            f"${price:,.2f}",
            quantity,
            f"${investment:,.2f}"
        )
    )

    quantity_entry.delete(0, tk.END)
    update_total()


def remove_stock():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select an investment to remove."
        )
        return

    for row_id in selected:
        index = tree.index(row_id)
        tree.delete(row_id)
        portfolio.pop(index)

    update_total()


def save_portfolio():
    if not portfolio:
        messagebox.showwarning(
            "Empty Portfolio",
            "Add at least one investment before saving."
        )
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="stock_portfolio.csv"
    )

    if not filename:
        return

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Stock Symbol",
                "Price Per Share (USD)",
                "Quantity",
                "Investment Value (USD)"
            ])

            for item in portfolio:
                writer.writerow([
                    item["symbol"],
                    item["price"],
                    item["quantity"],
                    item["total"]
                ])

            writer.writerow([])
            writer.writerow(["Total Investment", "", "",
                             sum(item["total"] for item in portfolio)])

        messagebox.showinfo(
            "Success",
            "Portfolio saved successfully!"
        )

    except OSError as error:
        messagebox.showerror("Save Error", str(error))


def clear_portfolio():
    if not portfolio:
        return

    if messagebox.askyesno(
        "Clear Portfolio",
        "Are you sure you want to remove all investments?"
    ):
        portfolio.clear()

        for row_id in tree.get_children():
            tree.delete(row_id)

        update_total()


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root, bg="#f2f5fa")
button_frame.pack(pady=10)

tk.Button(
    input_frame,
    text="Add Investment",
    command=add_stock,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10
).grid(row=1, column=1, padx=8, pady=10)

tk.Button(
    button_frame,
    text="Remove Selected",
    command=remove_stock,
    bg="#dc3545",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=6
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Save CSV",
    command=save_portfolio,
    bg="#198754",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=6
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Clear All",
    command=clear_portfolio,
    bg="#64748b",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=6
).grid(row=0, column=2, padx=5)

root.mainloop()
