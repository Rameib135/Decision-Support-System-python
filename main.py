import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np


def create_db():
    conn = sqlite3.connect('patient_data1.db')
    c = conn.cursor()
    # יצירת טבלאות חדשות אם הן לא קיימות
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            identity_number TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            protein_levels REAL,
            ast_levels REAL,
            alt_levels REAL,
            bmi REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT,
            full_name TEXT,
            phone TEXT,
            identity_number TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database checked and initialized successfully.")


def register_user():
    email = reg_email_entry.get()
    password = reg_password_entry.get()
    full_name = reg_full_name_entry.get()
    phone = reg_phone_entry.get()
    identity_number = reg_identity_entry.get()

    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (email, password, full_name, phone, identity_number) VALUES (?, ?, ?, ?, ?)',
              (email, password, full_name, phone, identity_number))
    conn.commit()
    conn.close()
    reg_status_label.config(text="Registration successful!", fg="green")


def login_user():
    email = login_email_entry.get()
    password = login_password_entry.get()

    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        login_status_label.config(text="Login successful!", fg="green")
        login_window.destroy()

        open_main_window()
    else:
        login_status_label.config(text="Login failed. Check your email and password.", fg="red")


def open_register_window():
    global reg_email_entry, reg_password_entry, reg_full_name_entry, reg_phone_entry, reg_identity_entry, reg_status_label
    register_window = tk.Toplevel(root)
    register_window.title("Register")

    tk.Label(register_window, text="Email:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    reg_email_entry = tk.Entry(register_window, font=("Arial", 12))
    reg_email_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(register_window, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    reg_password_entry = tk.Entry(register_window, font=("Arial", 12), show="*")
    reg_password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(register_window, text="Full Name:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    reg_full_name_entry = tk.Entry(register_window, font=("Arial", 12))
    reg_full_name_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(register_window, text="Phone:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    reg_phone_entry = tk.Entry(register_window, font=("Arial", 12))
    reg_phone_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(register_window, text="Identity Number:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
    reg_identity_entry = tk.Entry(register_window, font=("Arial", 12))
    reg_identity_entry.grid(row=4, column=1, padx=10, pady=5)

    reg_button = tk.Button(register_window, text="Register", font=("Arial", 12), command=register_user, bg="#4CAF50",
                           fg="white")
    reg_button.grid(row=5, column=0, columnspan=2, pady=10)

    reg_status_label = tk.Label(register_window, text="", font=("Arial", 12))
    reg_status_label.grid(row=6, column=0, columnspan=2, pady=10)


def open_login_window():
    global login_email_entry, login_password_entry, login_status_label, login_window
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Email:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    login_email_entry = tk.Entry(login_window, font=("Arial", 12))
    login_email_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(login_window, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    login_password_entry = tk.Entry(login_window, font=("Arial", 12), show="*")
    login_password_entry.grid(row=1, column=1, padx=10, pady=5)

    login_button = tk.Button(login_window, text="Login", font=("Arial", 12), command=login_user, bg="#4CAF50", fg="white")
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    login_status_label = tk.Label(login_window, text="", font=("Arial", 12))
    login_status_label.grid(row=3, column=0, columnspan=2, pady=10)


def submit_data():
    try:
        identity_number = id_entry.get()
        name = name_entry.get()
        age = int(age_entry.get())
        protein = float(protein_entry.get())
        ast = float(ast_entry.get())
        alt = float(alt_entry.get())
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = weight / (height / 100) ** 2

        conn = sqlite3.connect('patient_data.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO patients (identity_number, name, age, protein_levels, ast_levels, alt_levels, bmi) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (identity_number, name, age, protein, ast, alt, bmi))
        conn.commit()
        conn.close()
        print("Patient data saved successfully!")
        status_label.config(text="Data saved successfully!", fg="green")
        update_patient_list()  # Update the patient list after adding a new patient
    except Exception as e:
        print(f"Error: {e}")
        status_label.config(text=f"Error: {e}", fg="red")


def display_data():
    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients')
    rows = c.fetchall()
    conn.close()

    for i in tree.get_children():
        tree.delete(i)

    for row in rows:
        tree.insert('', 'end', values=row)


def plot_levels(level_type):
    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute(f'SELECT identity_number, {level_type} FROM patients')
    data = c.fetchall()
    conn.close()

    ids = [x[0] for x in data]
    levels = [x[1] for x in data]

    plt.figure(figsize=(10, 5))
    plt.bar(ids, levels, color='blue')
    plt.xlabel('Identity Number')
    plt.ylabel(f'{level_type.replace("_", " ").title()}')
    plt.title(f'{level_type.replace("_", " ").title()} of Patients')
    plt.show()


def analyze_data():
    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute('SELECT identity_number, name, age, protein_levels, ast_levels, alt_levels, bmi FROM patients')
    rows = c.fetchall()
    conn.close()

    recommendations = []
    for row in rows:
        identity_number, name, age, protein, ast, alt, bmi = row
        if ast > 40 or alt > 40:
            recommendations.append(f'Patient {name} ({identity_number}) needs further liver function tests.')
        elif protein < 6.0:
            recommendations.append(
                f'Patient {name} ({identity_number}) may need dietary adjustments to increase protein intake.')
        else:
            recommendations.append(f'Patient {name} ({identity_number}) is within normal parameters.')

    result_text.delete(1.0, tk.END)
    for recommendation in recommendations:
        result_text.insert(tk.END, recommendation + "\n")


def plot_distribution():
    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute('SELECT age, protein_levels, ast_levels, alt_levels, bmi FROM patients')
    data = c.fetchall()
    conn.close()

    ages = [x[0] for x in data]
    proteins = [x[1] for x in data]
    ast_levels = [x[2] for x in data]
    alt_levels = [x[3] for x in data]
    bmi = [x[4] for x in data]

    plt.figure(figsize=(14, 7))

    plt.subplot(2, 2, 1)
    plt.hist(ages, bins=10, color='blue', alpha=0.7)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Frequency')

    plt.subplot(2, 2, 2)
    plt.hist(proteins, bins=10, color='green', alpha=0.7)
    plt.title('Protein Levels Distribution')
    plt.xlabel('Protein Levels (g/dL)')
    plt.ylabel('Frequency')

    plt.subplot(2, 2, 3)
    plt.hist(ast_levels, bins=10, color='red', alpha=0.7)
    plt.title('AST Levels Distribution')
    plt.xlabel('AST Levels (U/L)')
    plt.ylabel('Frequency')

    plt.subplot(2, 2, 4)
    plt.hist(alt_levels, bins=10, color='orange', alpha=0.7)
    plt.title('ALT Levels Distribution')
    plt.xlabel('ALT Levels (U/L)')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()


def edit_patient():
    selected_item = tree.selection()
    if not selected_item:
        status_label.config(text="Please select a patient to edit.", fg="red")
        return

    item = tree.item(selected_item)
    patient = item['values']

    edit_window = tk.Toplevel(window)
    edit_window.title("Edit Patient Data")

    tk.Label(edit_window, text="Identity Number:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    edit_id_entry = tk.Entry(edit_window)
    edit_id_entry.grid(row=0, column=1, padx=10, pady=5)
    edit_id_entry.insert(0, patient[0])
    edit_id_entry.config(state='readonly')

    tk.Label(edit_window, text="Patient Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    edit_name_entry = tk.Entry(edit_window)
    edit_name_entry.grid(row=1, column=1, padx=10, pady=5)
    edit_name_entry.insert(0, patient[1])

    tk.Label(edit_window, text="Patient Age:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    edit_age_entry = tk.Entry(edit_window)
    edit_age_entry.grid(row=2, column=1, padx=10, pady=5)
    edit_age_entry.insert(0, patient[2])

    tk.Label(edit_window, text="Protein Levels (g/dL):", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    edit_protein_entry = tk.Entry(edit_window)
    edit_protein_entry.grid(row=3, column=1, padx=10, pady=5)
    edit_protein_entry.insert(0, patient[3])

    tk.Label(edit_window, text="AST Levels (U/L):", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
    edit_ast_entry = tk.Entry(edit_window)
    edit_ast_entry.grid(row=4, column=1, padx=10, pady=5)
    edit_ast_entry.insert(0, patient[4])

    tk.Label(edit_window, text="ALT Levels (U/L):", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5)
    edit_alt_entry = tk.Entry(edit_window)
    edit_alt_entry.grid(row=5, column=1, padx=10, pady=5)
    edit_alt_entry.insert(0, patient[5])

    tk.Label(edit_window, text="BMI:", font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=5)
    edit_bmi_entry = tk.Entry(edit_window)
    edit_bmi_entry.grid(row=6, column=1, padx=10, pady=5)
    edit_bmi_entry.insert(0, patient[6])

    def save_changes():
        new_name = edit_name_entry.get()
        new_age = int(edit_age_entry.get())
        new_protein = float(edit_protein_entry.get())
        new_ast = float(edit_ast_entry.get())
        new_alt = float(edit_alt_entry.get())
        new_bmi = float(edit_bmi_entry.get())

        conn = sqlite3.connect('patient_data.db')
        c = conn.cursor()
        c.execute('''
            UPDATE patients 
            SET name = ?, age = ?, protein_levels = ?, ast_levels = ?, alt_levels = ?, bmi = ? 
            WHERE identity_number = ?
        ''', (new_name, new_age, new_protein, new_ast, new_alt, new_bmi, patient[0]))
        conn.commit()
        conn.close()

        display_data()
        edit_window.destroy()
        status_label.config(text="Patient data updated successfully!", fg="green")

    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes, bg="#4CAF50", fg="white")
    save_button.grid(row=7, column=0, columnspan=2, pady=10)


def delete_patient():
    selected_item = tree.selection()
    if not selected_item:
        status_label.config(text="Please select a patient to delete.", fg="red")
        return

    item = tree.item(selected_item)
    patient = item['values']

    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute('DELETE FROM patients WHERE identity_number = ?', (patient[0],))
    conn.commit()
    conn.close()

    display_data()
    update_patient_list()
    status_label.config(text="Patient data deleted successfully!", fg="green")


def update_patient_list():
    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute('SELECT identity_number, name FROM patients')
    patients = c.fetchall()
    conn.close()

    for i in tree.get_children():
        tree.delete(i)

    for patient in patients:
        tree.insert('', 'end', values=patient)


def open_bmr_bmi_calculator():
    def open_bmr_calculator():
        bmr_window = tk.Toplevel(window)
        bmr_window.title("BMR Calculator")

        tk.Label(bmr_window, text="Weight (kg):", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        weight_entry = tk.Entry(bmr_window)
        weight_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(bmr_window, text="Height (cm):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        height_entry = tk.Entry(bmr_window)
        height_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(bmr_window, text="Age:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
        age_entry = tk.Entry(bmr_window)
        age_entry.grid(row=2, column=1, padx=10, pady=5)

        gender_var = tk.StringVar(value="Male")
        tk.Label(bmr_window, text="Gender:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
        tk.Radiobutton(bmr_window, text="Male", variable=gender_var, value="Male").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        tk.Radiobutton(bmr_window, text="Female", variable=gender_var, value="Female").grid(row=3, column=1, padx=10, pady=5, sticky="e")

        def calculate_bmr():
            weight = float(weight_entry.get())
            height = float(height_entry.get())
            age = int(age_entry.get())
            gender = gender_var.get()

            if gender == "Male":
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

            result_label.config(text=f"BMR: {bmr:.2f} calories/day")

        calculate_button = tk.Button(bmr_window, text="Calculate BMR", command=calculate_bmr, bg="#4CAF50", fg="white", padx=10, pady=5)
        calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

        result_label = tk.Label(bmr_window, text="", font=("Arial", 12))
        result_label.grid(row=5, column=0, columnspan=2, pady=10)

    def open_bmi_calculator():
        bmi_window = tk.Toplevel(window)
        bmi_window.title("BMI Calculator")

        tk.Label(bmi_window, text="Weight (kg):", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        weight_entry = tk.Entry(bmi_window)
        weight_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(bmi_window, text="Height (cm):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        height_entry = tk.Entry(bmi_window)
        height_entry.grid(row=1, column=1, padx=10, pady=5)

        def calculate_bmi():
            weight = float(weight_entry.get())
            height = float(height_entry.get())
            bmi = weight / (height / 100) ** 2
            result_label.config(text=f"BMI: {bmi:.2f}")

        calculate_button = tk.Button(bmi_window, text="Calculate BMI", command=calculate_bmi, bg="#4CAF50", fg="white", padx=10, pady=5)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        result_label = tk.Label(bmi_window, text="", font=("Arial", 12))
        result_label.grid(row=3, column=0, columnspan=2, pady=10)

    menu = tk.Menu(window)
    window.config(menu=menu)

    bmr_bmi_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="BMR/BMI Calculator", menu=bmr_bmi_menu)
    bmr_bmi_menu.add_command(label="BMR Calculator", command=open_bmr_calculator)
    bmr_bmi_menu.add_command(label="BMI Calculator", command=open_bmi_calculator)



def main_window():
    global id_entry, name_entry, age_entry, protein_entry, ast_entry, alt_entry, weight_entry, height_entry, status_label, tree, result_text, window
    window = tk.Tk()
    window.title("Liver Cirrhosis Decision Support System")

    window.geometry("900x700")
    window.configure(bg="#f0f0f0")

    title_label = tk.Label(window, text="Welcome to the Liver Cirrhosis DSS", font=("Arial", 20, "bold"), bg="#f0f0f0")
    title_label.pack(pady=20)

    form_frame = tk.Frame(window, bg="#f0f0f0")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Identity Number:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    id_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Patient Name:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=2, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    name_entry.grid(row=0, column=3, padx=10, pady=5)

    tk.Label(form_frame, text="Patient Age:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    age_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    age_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Protein Levels (g/dL):", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=2, padx=10, pady=5, sticky="w")
    protein_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    protein_entry.grid(row=1, column=3, padx=10, pady=5)

    tk.Label(form_frame, text="AST Levels (U/L):", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    ast_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    ast_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="ALT Levels (U/L):", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=2, padx=10, pady=5, sticky="w")
    alt_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    alt_entry.grid(row=2, column=3, padx=10, pady=5)

    tk.Label(form_frame, text="Weight (kg):", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    weight_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    weight_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Height (cm):", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=2, padx=10, pady=5, sticky="w")
    height_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    height_entry.grid(row=3, column=3, padx=10, pady=5)

    submit_button = tk.Button(form_frame, text="Submit", font=("Arial", 12), command=submit_data, bg="#4CAF50", fg="white", padx=10, pady=5)
    submit_button.grid(row=4, column=0, columnspan=4, pady=10)

    button_frame = tk.Frame(window, bg="#f0f0f0")
    button_frame.pack(pady=20)

    display_button = tk.Button(button_frame, text="Display Data", font=("Arial", 12), command=display_data,
                               bg="#2196F3", fg="white", padx=10, pady=5)
    display_button.grid(row=0, column=0, padx=10)

    plot_protein_button = tk.Button(button_frame, text="Plot Protein Levels", font=("Arial", 12),
                                    command=lambda: plot_levels('protein_levels'), bg="#FF9800", fg="white", padx=10, pady=5)
    plot_protein_button.grid(row=0, column=1, padx=10)

    plot_ast_button = tk.Button(button_frame, text="Plot AST Levels", font=("Arial", 12),
                                command=lambda: plot_levels('ast_levels'), bg="#FF9800", fg="white", padx=10, pady=5)
    plot_ast_button.grid(row=0, column=2, padx=10)

    plot_alt_button = tk.Button(button_frame, text="Plot ALT Levels", font=("Arial", 12),
                                command=lambda: plot_levels('alt_levels'), bg="#FF9800", fg="white", padx=10, pady=5)
    plot_alt_button.grid(row=0, column=3, padx=10)

    analyze_button = tk.Button(button_frame, text="Analyze Data", font=("Arial", 12), command=analyze_data,
                               bg="#9C27B0", fg="white", padx=10, pady=5)
    analyze_button.grid(row=0, column=4, padx=10)

    edit_button = tk.Button(button_frame, text="Edit Patient", font=("Arial", 12), command=edit_patient, bg="#FFC107",
                            fg="white", padx=10, pady=5)
    edit_button.grid(row=0, column=5, padx=10)

    delete_button = tk.Button(button_frame, text="Delete Patient", font=("Arial", 12), command=delete_patient,
                              bg="#f44336", fg="white", padx=10, pady=5)
    delete_button.grid(row=0, column=6, padx=10)

    dist_button = tk.Button(button_frame, text="Distribution Plots", font=("Arial", 12), command=plot_distribution,
                            bg="#673AB7", fg="white", padx=10, pady=5)
    dist_button.grid(row=0, column=7, padx=10)

    report_button = tk.Button(button_frame, text="Generate Report", font=("Arial", 12), command=analyze_data,
                              bg="#009688", fg="white", padx=10, pady=5)
    report_button.grid(row=0, column=8, padx=10)

    open_bmr_bmi_calculator()

    status_label = tk.Label(window, text="", font=("Arial", 12), bg="#f0f0f0")
    status_label.pack(pady=10)

    tree_frame = tk.Frame(window, bg="#f0f0f0")
    tree_frame.pack(pady=20, fill='x')

    tree = ttk.Treeview(tree_frame,
                        columns=('identity_number', 'name', 'age', 'protein_levels', 'ast_levels', 'alt_levels', 'bmi'),
                        show='headings', height=10)
    tree.heading('identity_number', text='Identity Number')
    tree.heading('name', text='Name')
    tree.heading('age', text='Age')
    tree.heading('protein_levels', text='Protein Levels')
    tree.heading('ast_levels', text='AST Levels')
    tree.heading('alt_levels', text='ALT Levels')
    tree.heading('bmi', text='BMI')
    tree.pack(fill='x')

    result_text = tk.Text(window, height=10, width=100, font=("Arial", 12))
    result_text.pack(pady=10)

    create_db()  # Create the database and table when the application starts
    window.mainloop()


def open_main_window():
    main_window()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login/Register")

    tk.Label(root, text="Liver Cirrhosis DSS", font=("Arial", 20, "bold")).pack(pady=20)

    login_button = tk.Button(root, text="Login", font=("Arial", 12), command=open_login_window, bg="#4CAF50", fg="white", padx=10, pady=5)
    login_button.pack(pady=10)

    register_button = tk.Button(root, text="Register", font=("Arial", 12), command=open_register_window, bg="#2196F3", fg="white", padx=10, pady=5)
    register_button.pack(pady=10)

    create_db()  # Make sure to create the database and tables when the application starts

    root.mainloop()
