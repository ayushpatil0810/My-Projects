from tkinter import *
from customtkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Checking if the file is empty
                if data_file.readable() and data_file.readline() == "":
                    data = {}
                else:
                    data_file.seek(0)  # Go back to the start of the file after checking
                    # Reading old data
                    data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = CTk()
mode = set_appearance_mode("light")
theme = set_default_color_theme("green")
window.title("Password Manager")
window.config(padx=50, pady=50)

logo_img = PhotoImage(file="lock.png")
canvas = Canvas(height=200, width=200, background="#ebebeb", highlightthickness=0)
canvas.create_image(126, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = CTkLabel(window, text="Website :")
website_label.grid(row=1, column=0)

email_label = CTkLabel(window, text="Email/Username :")
email_label.grid(row=2, column=0)

password_label = CTkLabel(window, text="Password :")
password_label.grid(row=3, column=0)

# Entries
website_entry = CTkEntry(window, width=210)
website_entry.grid(row=1, column=1, padx=5, pady=5)
website_entry.focus()

email_entry = CTkEntry(window, width=350)
email_entry.grid(row=2, column=1, columnspan=2, pady=5, padx=5)
email_entry.insert(0, "your@email.com")

password_entry = CTkEntry(window, width=210)
password_entry.grid(row=3, column=1, pady=5, padx=5)

# Buttons
search_button = CTkButton(window, text="Search", command=find_password)
search_button.grid(row=1, column=2)

generate_password_button = CTkButton(window, text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = CTkButton(window, text="Add", width=360, command=save)
add_button.grid(row=4, column=1, columnspan=2, pady=5)

window.mainloop()
