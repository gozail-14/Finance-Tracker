import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd
import pushbullet
import os

total_amount = 0


def SaveData():
    name = E1.get()
    amount = E2.get()  # Convert to int

    # Save data as CSV file
    with open("data.csv", 'a') as f:
        f.write(f"{name}, {amount}\n")

    E1.delete(0, 'end')
    E2.delete(0, 'end')

    # Update total amount
    global total_amount
    total_amount += amount
    check_budget_increase()

    ShowTable()


def ShowTable():
    try:
        df = pd.read_csv('data.csv', header=None, names=["Names", "Amount"])

        # Clear the existing data in the table
        table.delete(*table.get_children())

        for row in df.itertuples(index=False):
            table.insert('', 'end', values=row)
        # Show the table with data
        table.pack(padx=0, pady=200)

        # Calculate the total amount
        global total_amount
        total_amount = df["Amount"].sum()

        # Display total amount
        table.insert('', 'end', values=["Total", total_amount])

        check_budget_increase()

    except pd.errors.EmptyDataError:
        print('No data found')
        # Show table
        table.pack(padx=0, pady=200)

# Show or hide the table based on the current state
def toggle_table():
    if table.winfo_viewable():
        table.pack_forget()
    else:
        ShowTable()
        table.pack(padx=0, pady=200)


# Function to toggle between dark and white mode
def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        window.configure(bg="#000000")
        mode_button.config(image=dark_mode_img)
        Enter.config(image=enter_img)
        Table.config(image=table_img)
        delete_button.config(image=delete_img)
        # Set other widgets' background and foreground colors for white mode
        L1.config(text="Amount", bg="#000000", fg="#686A6C")  # Label on Amount in white
        E1.config(bg="#000000", fg="#686A6C", bd=1)  # Entry 1 in white
        E2.config(bg="#000000", fg="#686A6C", bd=1)  # Entry 2 in white
        L2.config(text="Name", bg="#000000", fg="#686A6C")  # Label on Name in white
        style.configure("Treeview", background="#3A3B3C", foreground="#686A6C",
                        fieldbackground="#3A3B3C")  # Table style
    else:
        window.configure(bg="#FFFFFF")
        mode_button.config(image=white_mode_img)
        Enter.config(image=enter_img_white)
        Table.config(image=table_img_white)
        delete_button.config(image=delete_img_white)
        # Set other widgets' background and foreground colors for white mode
        L1.config(text="Amount", bg="#ffffff", fg="#000000")  # Label on Amount in white
        E1.config(bg="#ffffff", fg="#000000", bd=1)  # Entry 1 in white
        E2.config(bg="#ffffff", fg="#000000", bd=1)  # Entry 2 in white
        L2.config(text="Name", bg="#ffffff", fg="#000000")  # Label on Name in white
        style.configure("Treeview", background="#ffffff", foreground="#000000",
                        fieldbackground="#ffffff")  # Table style


def send_push_notification(api_key, title, message):
    pb = pushbullet.Pushbullet(api_key)
    push = pb.push_note(title, message)
    return push


def check_budget_increase():
    global total_amount
    if total_amount >= 1000:
        notification_title = "Budget increasing"
        notification_message = f"Your budget exceeding 1000! Current total: {total_amount}"
        send_push_notification(API_KEY, notification_title, notification_message)


if __name__ == "__main__":
    API_KEY = "o.JNJxX3I8cvhrGbkwmg8qCOPautWl83Nr"


def Delete_Table():
    global table
    if os.path.exists("data.csv"):
        os.remove("data.csv")
    else:
        ShowTable()

# Create Window
window = tk.Tk()
window.title("Finance Tracker")
window.geometry("1500x1000")

# Variable to keep track of current mode (True for dark mode, False for white mode)
dark_mode = True

# Load the images for the mode buttons
dark_mode_img = tk.PhotoImage(file="dark mode.png")
white_mode_img = tk.PhotoImage(file="day mode.png")

# Table Image
table_img = tk.PhotoImage(file="table button black edit.png")
table_img_white = tk.PhotoImage(file="table button white.png")

# Enter Image
enter_img = tk.PhotoImage(file="enter button bkack.png")
enter_img_white = tk.PhotoImage(file="enter button white.png")

# Delete Image
delete_img = tk.PhotoImage(file="trash black.png")
delete_img_white = tk.PhotoImage(file="trash white.png")

# Background
window.configure(bg="#000000")

# Amount Label
L1 = Label(window, text="Name", bg="#000000", fg="#686A6C")
L1.pack()
L1.place(x=530, y=20)

# Amount Entry
E1 = Entry(window, bd=1, bg="#000000", fg="#686A6C")
E1.pack()
E1.place(x=500, y=40)

# Name Label
L2 = Label(window, text="Amount", bg="#000000", fg="#686A6C")
L2.pack()
L2.place(x=940, y=20)

# Name Entry
E2 = Entry(window, bd=1, bg="#000000", fg="#686A6C")
E2.pack()
E2.place(x=900, y=40)

# Create a button that enter data in database
basic_enter_img = tk.PhotoImage(file="enter button bkack.png")
Enter = tk.Button(window, image=basic_enter_img, command=SaveData, bd=0)
Enter.config(highlightthickness=0, highlightbackground="black")
Enter.pack()
Enter.place(x=1100, y=50)

# Create a Treeview widget (Table)
style = ttk.Style()
style.theme_use("clam")  # Use the "clam" theme for Treeview
style.configure("Treeview", background="#3A3B3C", foreground="#686A6C", fieldbackground="#3A3B3C")
style.map("Treeview", background=[("selected", "#FF5733")])

# Table labels
table = ttk.Treeview(window, columns=["Name", "Amount"], show='headings')
table.heading("Name", text="Name", anchor=tk.CENTER)  # Set anchor to center
table.heading("Amount", text="Amount", anchor=tk.CENTER)  # Set anchor to center
table.pack(padx=0, pady=200)

table.pack_forget()

# Show Table button
basic_table_img = tk.PhotoImage(file="table button black edit.png")
Table = tk.Button(window, image=basic_table_img, command=toggle_table, bd=0)
Table.config(highlightthickness=0, highlightbackground="black")
Table.pack()
Table.place(x=1100, y=100)

# Create the mode button
mode_button = tk.Button(window, image=dark_mode_img, bd=0, command=toggle_mode)
mode_button.config(highlightthickness=0, highlightbackground="black")
mode_button.pack()
mode_button.place(x=10, y=10)

# Create delete table button
delete_button = tk.Button(window, image=delete_img, bd=0, command=Delete_Table)
delete_button.config(highlightthickness=0, highlightbackground="black")
delete_button.pack()
delete_button.place(x=1100, y=160)


# Table visible
table_visible = False

window.mainloop()
