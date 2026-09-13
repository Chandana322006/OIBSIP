import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# ============================================================
# VARIABLES
# ============================================================

password_history = []


# ============================================================
# GENERATE PASSWORD
# ============================================================

def generate_password():
    try:
        length = int(length_spinbox.get())

        # Check minimum length
        if length < 8:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )
            return

        # Get selected character types
        selected_sets = []

        if uppercase_var.get():
            selected_sets.append(
                string.ascii_uppercase
            )

        if lowercase_var.get():
            selected_sets.append(
                string.ascii_lowercase
            )

        if numbers_var.get():
            selected_sets.append(
                string.digits
            )

        if symbols_var.get():
            selected_sets.append(
                string.punctuation
            )

        # At least 2 character types
        if len(selected_sets) < 2:
            messagebox.showerror(
                "Character Types",
                "Please select at least 2 character types."
            )
            return

        # Ambiguous characters
        ambiguous = "0Ol1"

        # Remove ambiguous characters if selected
        if exclude_ambiguous_var.get():

            new_sets = []

            for character_set in selected_sets:
                filtered_set = ""

                for character in character_set:
                    if character not in ambiguous:
                        filtered_set += character

                new_sets.append(filtered_set)

            selected_sets = new_sets

        # Check that selected sets are not empty
        for character_set in selected_sets:
            if len(character_set) == 0:
                messagebox.showerror(
                    "Error",
                    "A selected character type has no usable characters."
                )
                return

        # ----------------------------------------------------
        # GUARANTEE ONE CHARACTER FROM EACH SELECTED TYPE
        # ----------------------------------------------------

        password_characters = []

        for character_set in selected_sets:
            password_characters.append(
                secrets.choice(character_set)
            )

        # Combine all selected character sets
        all_characters = "".join(selected_sets)

        # Fill remaining positions
        while len(password_characters) < length:
            password_characters.append(
                secrets.choice(all_characters)
            )

        # Securely shuffle
        secrets.SystemRandom().shuffle(
            password_characters
        )

        password = "".join(password_characters)

        # Display password
        password_entry.delete(
            0,
            tk.END
        )

        password_entry.insert(
            0,
            password
        )

        # Calculate strength
        strength = calculate_strength(
            length,
            len(selected_sets)
        )

        strength_label.config(
            text=f"Strength: {strength}"
        )

        # Change strength color
        if strength == "Weak":
            strength_label.config(
                fg="red"
            )

        elif strength == "Medium":
            strength_label.config(
                fg="orange"
            )

        else:
            strength_label.config(
                fg="green"
            )

        # Automatically copy password
        try:
            pyperclip.copy(password)
            clipboard_label.config(
                text="Password copied to clipboard!"
            )

        except Exception:
            clipboard_label.config(
                text="Password generated."
            )

        # ----------------------------------------------------
        # GENERATION HISTORY
        # ----------------------------------------------------

        password_history.insert(
            0,
            password
        )

        # Keep only last 5 passwords
        if len(password_history) > 5:
            password_history.pop()

        update_history()

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid password length."
        )


# ============================================================
# PASSWORD STRENGTH
# ============================================================

def calculate_strength(length, character_types):

    if length >= 16 and character_types >= 4:
        return "Strong"

    elif length >= 12 and character_types >= 3:
        return "Strong"

    elif length >= 10 and character_types >= 2:
        return "Medium"

    else:
        return "Weak"


# ============================================================
# COPY PASSWORD
# ============================================================

def copy_password():

    password = password_entry.get()

    if password == "":
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    try:

        pyperclip.copy(password)

        clipboard_label.config(
            text="Password copied to clipboard!"
        )

    except Exception:

        messagebox.showerror(
            "Clipboard Error",
            "Unable to copy the password."
        )


# ============================================================
# UPDATE HISTORY
# ============================================================

def update_history():

    history_text.config(
        state="normal"
    )

    history_text.delete(
        "1.0",
        tk.END
    )

    for i, password in enumerate(
        password_history,
        start=1
    ):

        history_text.insert(
            tk.END,
            f"{i}. {password}\n"
        )

    history_text.config(
        state="disabled"
    )


# ============================================================
# CLEAR HISTORY
# ============================================================

def clear_history():

    password_history.clear()

    update_history()

    clipboard_label.config(
        text=""
    )


# ============================================================
# CREATE WINDOW
# ============================================================

window = tk.Tk()

window.title(
    "Random Password Generator"
)

window.geometry(
    "600x700"
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
    text="Random Password Generator",
    font=("Arial", 22, "bold")
)

title_label.pack(
    pady=20
)


# ============================================================
# PASSWORD LENGTH
# ============================================================

length_label = tk.Label(
    window,
    text="Password Length",
    font=("Arial", 12)
)

length_label.pack(
    pady=5
)


length_spinbox = tk.Spinbox(
    window,
    from_=8,
    to=100,
    width=10,
    font=("Arial", 12)
)

length_spinbox.pack(
    pady=5
)


# ============================================================
# CHARACTER TYPE CHECKBOXES
# ============================================================

types_label = tk.Label(
    window,
    text="Select Character Types",
    font=("Arial", 12, "bold")
)

types_label.pack(
    pady=15
)


uppercase_var = tk.BooleanVar(
    value=True
)

lowercase_var = tk.BooleanVar(
    value=True
)

numbers_var = tk.BooleanVar(
    value=True
)

symbols_var = tk.BooleanVar(
    value=True
)


uppercase_check = tk.Checkbutton(
    window,
    text="Uppercase Letters (A-Z)",
    variable=uppercase_var,
    font=("Arial", 11)
)

uppercase_check.pack(
    anchor="w",
    padx=180
)


lowercase_check = tk.Checkbutton(
    window,
    text="Lowercase Letters (a-z)",
    variable=lowercase_var,
    font=("Arial", 11)
)

lowercase_check.pack(
    anchor="w",
    padx=180
)


numbers_check = tk.Checkbutton(
    window,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Arial", 11)
)

numbers_check.pack(
    anchor="w",
    padx=180
)


symbols_check = tk.Checkbutton(
    window,
    text="Symbols",
    variable=symbols_var,
    font=("Arial", 11)
)

symbols_check.pack(
    anchor="w",
    padx=180
)


# ============================================================
# AMBIGUOUS CHARACTERS
# ============================================================

exclude_ambiguous_var = tk.BooleanVar(
    value=False
)

ambiguous_check = tk.Checkbutton(
    window,
    text="Exclude ambiguous characters (0, O, l, 1)",
    variable=exclude_ambiguous_var,
    font=("Arial", 11)
)

ambiguous_check.pack(
    pady=15
)


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = tk.Button(
    window,
    text="Generate Password",
    command=generate_password,
    width=25,
    font=("Arial", 12, "bold")
)

generate_button.pack(
    pady=10
)


# ============================================================
# PASSWORD DISPLAY
# ============================================================

password_label = tk.Label(
    window,
    text="Generated Password",
    font=("Arial", 12, "bold")
)

password_label.pack(
    pady=5
)


password_entry = tk.Entry(
    window,
    width=45,
    font=("Arial", 13),
    justify="center"
)

password_entry.pack(
    pady=5
)


# ============================================================
# COPY BUTTON
# ============================================================

copy_button = tk.Button(
    window,
    text="Copy to Clipboard",
    command=copy_password,
    width=25,
    font=("Arial", 11)
)

copy_button.pack(
    pady=8
)


# ============================================================
# CLIPBOARD STATUS
# ============================================================

clipboard_label = tk.Label(
    window,
    text="",
    font=("Arial", 10)
)

clipboard_label.pack(
    pady=3
)


# ============================================================
# STRENGTH
# ============================================================

strength_label = tk.Label(
    window,
    text="Strength: --",
    font=("Arial", 13, "bold")
)

strength_label.pack(
    pady=10
)


# ============================================================
# HISTORY
# ============================================================

history_heading = tk.Label(
    window,
    text="Last 5 Generated Passwords",
    font=("Arial", 12, "bold")
)

history_heading.pack(
    pady=5
)


history_text = tk.Text(
    window,
    width=55,
    height=7,
    font=("Arial", 10)
)

history_text.pack(
    pady=5
)

history_text.config(
    state="disabled"
)


# ============================================================
# CLEAR HISTORY BUTTON
# ============================================================

clear_button = tk.Button(
    window,
    text="Clear History",
    command=clear_history,
    width=20,
    font=("Arial", 10)
)

clear_button.pack(
    pady=8
)


# ============================================================
# START APPLICATION
# ============================================================

window.mainloop()