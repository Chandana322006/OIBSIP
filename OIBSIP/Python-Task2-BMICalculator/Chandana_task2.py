import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ============================================================
# DATABASE SETUP
# ============================================================

try:
    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        bmi REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    )
    """)

    conn.commit()

except sqlite3.Error:
    messagebox.showerror(
        "Database Error",
        "Unable to connect to the database."
    )


# ============================================================
# CALCULATE BMI
# ============================================================

def calculate_bmi():

    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        # Check name
        if name == "":
            messagebox.showerror(
                "Error",
                "Please enter your name."
            )
            return

        # Check positive values
        if weight <= 0 or height_cm <= 0:
            messagebox.showerror(
                "Error",
                "Weight and height must be greater than 0."
            )
            return

        # Check realistic values
        if weight > 300:
            messagebox.showerror(
                "Error",
                "Please enter a realistic weight."
            )
            return

        if height_cm < 50 or height_cm > 250:
            messagebox.showerror(
                "Error",
                "Please enter a height between 50 cm and 250 cm."
            )
            return

        # Convert height from cm to meters
        height_m = height_cm / 100

        # BMI formula
        bmi = weight / (height_m ** 2)

        # ====================================================
        # BMI CATEGORY
        # ====================================================

        if bmi < 18.5:
            category = "Underweight"
            result_color = "orange"

        elif bmi < 25:
            category = "Normal"
            result_color = "green"

        elif bmi < 30:
            category = "Overweight"
            result_color = "orange"

        else:
            category = "Obese"
            result_color = "red"

        # ====================================================
        # DISPLAY RESULT
        # ====================================================

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}",
            fg=result_color
        )

        # ====================================================
        # SAVE TO DATABASE
        # ====================================================

        date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
        INSERT INTO bmi_records
        (name, weight, height, bmi, category, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            weight,
            height_cm,
            bmi,
            category,
            date
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "BMI calculated and saved successfully!"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter numbers for weight and height."
        )

    except sqlite3.Error:
        messagebox.showerror(
            "Database Error",
            "Unable to save the BMI record."
        )


# ============================================================
# VIEW HISTORY
# ============================================================

def view_history():

    name = name_entry.get().strip()

    if name == "":
        messagebox.showerror(
            "Error",
            "Please enter a name."
        )
        return

    try:

        cursor.execute("""
        SELECT weight, height, bmi, category, date
        FROM bmi_records
        WHERE name = ?
        ORDER BY date DESC
        """, (name,))

        records = cursor.fetchall()

        if not records:
            messagebox.showinfo(
                "History",
                f"No records found for {name}."
            )
            return

        # Create history window
        history_window = tk.Toplevel(window)
        history_window.title(
            f"BMI History - {name}"
        )
        history_window.geometry("650x450")

        # Heading
        tk.Label(
            history_window,
            text=f"BMI History for {name}",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        # Text box
        history_text = tk.Text(
            history_window,
            width=75,
            height=20,
            font=("Arial", 10)
        )

        history_text.pack(
            padx=10,
            pady=10
        )

        # Display records
        for record in records:

            weight, height, bmi, category, date = record

            history_text.insert(
                tk.END,
                f"Date: {date}\n"
                f"Weight: {weight:.2f} kg\n"
                f"Height: {height:.2f} cm\n"
                f"BMI: {bmi:.2f}\n"
                f"Category: {category}\n"
                f"{'-' * 60}\n"
            )

        # Prevent editing
        history_text.config(
            state="disabled"
        )

    except sqlite3.Error:

        messagebox.showerror(
            "Database Error",
            "Unable to read BMI history."
        )


# ============================================================
# VIEW BMI TREND
# ============================================================

def view_trend():

    name = name_entry.get().strip()

    if name == "":
        messagebox.showerror(
            "Error",
            "Please enter a name."
        )
        return

    try:

        cursor.execute("""
        SELECT bmi, date
        FROM bmi_records
        WHERE name = ?
        ORDER BY date ASC
        """, (name,))

        records = cursor.fetchall()

        if not records:
            messagebox.showinfo(
                "BMI Trend",
                f"No records found for {name}."
            )
            return

        bmi_values = []
        dates = []

        # Get BMI and dates
        for bmi, date in records:

            bmi_values.append(bmi)

            date_object = datetime.strptime(
                date,
                "%Y-%m-%d %H:%M:%S"
            )

            dates.append(
                date_object.strftime("%d-%m-%Y")
            )

        # ====================================================
        # CREATE GRAPH
        # ====================================================

        plt.figure(figsize=(10, 6))

        plt.plot(
            dates,
            bmi_values,
            marker="o",
            linewidth=2
        )

        # Display BMI value above each point
        for i, bmi in enumerate(bmi_values):

            plt.annotate(
                f"{bmi:.2f}",
                (dates[i], bmi),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center"
            )

        # BMI category reference lines
        plt.axhline(
            y=18.5,
            linestyle="--",
            label="Underweight limit"
        )

        plt.axhline(
            y=25,
            linestyle="--",
            label="Normal limit"
        )

        plt.axhline(
            y=30,
            linestyle="--",
            label="Obese limit"
        )

        plt.title(
            f"BMI Trend - {name}",
            fontsize=16
        )

        plt.xlabel("Date")
        plt.ylabel("BMI")

        plt.xticks(
            rotation=45
        )

        plt.grid(True)

        plt.legend()

        plt.tight_layout()

        plt.show()

    except sqlite3.Error:

        messagebox.showerror(
            "Database Error",
            "Unable to read BMI records."
        )

    except ValueError:

        messagebox.showerror(
            "Date Error",
            "Unable to process saved dates."
        )


# ============================================================
# CLEAR INPUTS
# ============================================================

def clear_fields():

    name_entry.delete(
        0,
        tk.END
    )

    weight_entry.delete(
        0,
        tk.END
    )

    height_entry.delete(
        0,
        tk.END
    )

    result_label.config(
        text="BMI: --\nCategory: --",
        fg="black"
    )


# ============================================================
# CLOSE APPLICATION
# ============================================================

def close_application():

    try:
        conn.close()
    except sqlite3.Error:
        pass

    window.destroy()


# ============================================================
# CREATE MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title(
    "BMI Calculator"
)

window.geometry(
    "450x550"
)

window.resizable(
    False,
    False
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    window,
    text="BMI Calculator",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=25
)


# ============================================================
# NAME
# ============================================================

tk.Label(
    window,
    text="Name",
    font=("Arial", 12)
).pack()

name_entry = tk.Entry(
    window,
    width=30,
    font=("Arial", 12)
)

name_entry.pack(
    pady=8
)


# ============================================================
# WEIGHT
# ============================================================

tk.Label(
    window,
    text="Weight (kg)",
    font=("Arial", 12)
).pack()

weight_entry = tk.Entry(
    window,
    width=30,
    font=("Arial", 12)
)

weight_entry.pack(
    pady=8
)


# ============================================================
# HEIGHT
# ============================================================

tk.Label(
    window,
    text="Height (cm)",
    font=("Arial", 12)
).pack()

height_entry = tk.Entry(
    window,
    width=30,
    font=("Arial", 12)
)

height_entry.pack(
    pady=8
)


# ============================================================
# CALCULATE BUTTON
# ============================================================

calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    command=calculate_bmi,
    width=20,
    font=("Arial", 11, "bold")
)

calculate_button.pack(
    pady=15
)


# ============================================================
# VIEW HISTORY BUTTON
# ============================================================

history_button = tk.Button(
    window,
    text="View History",
    command=view_history,
    width=20,
    font=("Arial", 11)
)

history_button.pack(
    pady=5
)


# ============================================================
# TREND BUTTON
# ============================================================

trend_button = tk.Button(
    window,
    text="View BMI Trend",
    command=view_trend,
    width=20,
    font=("Arial", 11)
)

trend_button.pack(
    pady=5
)


# ============================================================
# CLEAR BUTTON
# ============================================================

clear_button = tk.Button(
    window,
    text="Clear",
    command=clear_fields,
    width=20,
    font=("Arial", 11)
)

clear_button.pack(
    pady=5
)


# ============================================================
# RESULT
# ============================================================

result_label = tk.Label(
    window,
    text="BMI: --\nCategory: --",
    font=("Arial", 16, "bold")
)

result_label.pack(
    pady=20
)


# ============================================================
# CLOSE EVENT
# ============================================================

window.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


# ============================================================
# START APPLICATION
# ============================================================

window.mainloop()