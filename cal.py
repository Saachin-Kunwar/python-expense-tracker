import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

FILE_NAME = "expenses.csv"


# ================= CALCULATE + SAVE =================
def calculate_and_save():
    try:
        month = month_entry.get().strip()

        rent = int(rent_entry.get())
        food = int(food_entry.get())
        units = int(units_entry.get())
        cost_per_unit = int(cost_entry.get())
        wifi = int(wifi_entry.get())
        water = int(water_entry.get())

        names_input = names_entry.get().strip()
        names = [n.strip() for n in names_input.split(",") if n.strip()]

        if not month:
            messagebox.showerror("Error", "Enter month (e.g., 2026-05)")
            return

        if len(names) == 0:
            messagebox.showerror("Error", "Enter roommate names")
            return

        persons = len(names)

        electricity = units * cost_per_unit
        total = rent + food + electricity + wifi + water
        per_person = total / persons

        # Save to CSV
        file_exists = os.path.isfile(FILE_NAME)

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Month", "Rent", "Food", "Electricity",
                    "WiFi", "Water", "Total", "Persons", "PerPerson", "Names"
                ])

            writer.writerow([
                month, rent, food, electricity,
                wifi, water, total, persons, f"{per_person:.2f}", "|".join(names)
            ])

        # Per-person breakdown
        split_text = "\n👥 Per Person Breakdown:\n"
        for name in names:
            split_text += f"👉 {name}: Rs {per_person:.2f}\n"

        result_label.config(
            text=(
                f"📊 Total Expense: Rs {total}\n"
                f"⚡ Electricity: Rs {electricity}\n\n"
                f"Each Person Pays: Rs {per_person:.2f}\n"
                f"{split_text}"
            )
        )

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers only")


# ================= RESET =================
def reset():
    entries = [
        month_entry, rent_entry, food_entry,
        units_entry, cost_entry, wifi_entry,
        water_entry, names_entry
    ]
    for entry in entries:
        entry.delete(0, tk.END)

    result_label.config(text="")


# ================= HISTORY (TREEVIEW UI) =================
def view_history():
    if not os.path.isfile(FILE_NAME):
        messagebox.showinfo("No Data", "No records found yet")
        return

    history_window = tk.Toplevel(root)
    history_window.title("Expense History")
    history_window.geometry("950x450")

    # Style
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#f9f9f9",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#f9f9f9")

    style.configure("Treeview.Heading",
                    font=("Arial", 10, "bold"))

    frame = tk.Frame(history_window)
    frame.pack(fill="both", expand=True)

    columns = ("Month", "Total", "Per Person", "People", "Names")

    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Headings
    tree.heading("Month", text="Month")
    tree.heading("Total", text="Total (Rs)")
    tree.heading("Per Person", text="Per Person (Rs)")
    tree.heading("People", text="No. of People")
    tree.heading("Names", text="Roommates")

    # Column settings
    tree.column("Month", width=100, anchor="center")
    tree.column("Total", width=120, anchor="center")
    tree.column("Per Person", width=140, anchor="center")
    tree.column("People", width=120, anchor="center")
    tree.column("Names", width=400, anchor="w")

    # Scrollbars
    y_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

    tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # Insert data
    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for i, row in enumerate(reader):
            tag = "evenrow" if i % 2 == 0 else "oddrow"

            tree.insert("", "end", values=(
                row["Month"],
                row["Total"],
                row["PerPerson"],
                row["Persons"],
                row["Names"].replace("|", ", ")
            ), tags=(tag,))

    # Row colors
    tree.tag_configure("evenrow", background="#ffffff")
    tree.tag_configure("oddrow", background="#eeeeee")


# ================= GUI =================
root = tk.Tk()
root.title("Expense Tracker Pro")
root.geometry("520x650")
root.resizable(False, False)

tk.Label(root, text="🏠 Expense Tracker", font=("Arial", 16, "bold")).pack(pady=10)


def create_field(label):
    frame = tk.Frame(root)
    frame.pack(pady=4)
    tk.Label(frame, text=label, width=25, anchor="w").pack(side="left")
    entry = tk.Entry(frame, width=25)
    entry.pack(side="right")
    return entry


# Inputs
month_entry = create_field("Month (YYYY-MM):")
rent_entry = create_field("Room Rent (Rs):")
food_entry = create_field("Food Cost (Rs):")
units_entry = create_field("Electricity Units:")
cost_entry = create_field("Cost per Unit (Rs):")
wifi_entry = create_field("WiFi Bill (Rs):")
water_entry = create_field("Water Bill (Rs):")

tk.Label(root, text="Roommate Names (comma separated):").pack(pady=(10, 0))
names_entry = tk.Entry(root, width=45)
names_entry.pack(pady=5)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Save Expense",
          command=calculate_and_save,
          bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="View History",
          command=view_history,
          bg="#2196F3", fg="white", width=15).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Reset",
          command=reset,
          bg="#f44336", fg="white", width=15).grid(row=1, column=0, columnspan=2, pady=10)

# Result
result_label = tk.Label(root, text="", font=("Arial", 11), justify="left")
result_label.pack(pady=10)

root.mainloop()