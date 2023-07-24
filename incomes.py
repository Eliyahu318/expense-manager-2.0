import json
from tkinter import Tk, Label, Entry, Button, END, messagebox
import datetime


YELLOW = "#f7f5dd"

root = Tk()
root.title("ניהול חשבון")
root.config(bg=YELLOW, padx=70, pady=70, )


def add_incomes(event=None):
    current_date = datetime.datetime.now()
    current_date_str = current_date.strftime("%d/%m/%y-%H:%M:%S")
    income = float(add_income_entry.get())
    with open("file_spend.json", "r+") as data_fie:
        data = json.load(data_fie)
        data["incomes"][current_date_str] = income
        # with open("file_spend.json", "w") as file:
        data_fie.seek(0)
        data_fie.truncate()
        json.dump(data, data_fie, indent=4)
    update_incomes()


def delete_last_add_income():
    with open("file_spend.json", "r+") as data_file:
        data = json.load(data_file)
        if len(data["incomes"]) > 1:  # 2 and LAST_MONTH not in data or len(data) > 3:
            data["incomes"].popitem()
        else:
            messagebox.showinfo(title="שגיאה", message="אין הכנסות למחוק")
        # with open("file_spend.json", "w") as file:
        data_file.seek(0)
        data_file.truncate()
        json.dump(data, data_file, indent=4)
    update_incomes()


def update_incomes():
    with open("file_spend.json", "r") as data_file:
        data = json.load(data_file)["incomes"].items()
        income = sum([value for key, value in data])
    if income % 1 == 0:
        income = "{:,.0f}".format(income)  # Format spending with commas
    sum_income_label.config(text=income)
    add_income_entry.delete(first=0, last=END)
    balance_calculate()


def balance_calculate():
    with open("file_spend.json", "r") as data:
        data = json.load(data)
        income = sum([value for key, value in data["incomes"].items()])
        spend = sum([value[0] for key, value in data["spends"].items()])
    balance = income - spend
    if balance < 0:
        balance_text_num.config(fg="red")
    else:
        balance_text_num.config(fg="green")
    if balance % 1 == 0:
        balance = "{:,.0f}".format(balance)
    balance_text_num.config(text=balance)
    return balance


FONT = ("Arial", 10, "bold")

# Labels
balance_title = Label(text=":יתרה בסוף החודש", font=("Normal", 11, "bold"), bg=YELLOW)

balance_text_num = Label(font=("Normal", 34, "bold"), bg=YELLOW)

title_income_label = Label(text="הכנסות החודש", font=("Arial", 16, "bold"), bg=YELLOW, fg="black")

sum_income_label = Label(font=("Arial", 24, "bold"), bg=YELLOW, fg="green")

add_income_label = Label(text=":הוסף הכנסה", font=("Arial", 16, "bold"), bg=YELLOW, fg="black")

# Entry
add_income_entry = Entry(width=20, font=FONT)
add_income_entry.focus()

# Button
add_income_button = Button(text="הוסף", font=FONT, command=add_incomes, width=12, bg="gold")

delete_income_button = Button(text="מחק", font=FONT, command=delete_last_add_income, width=12, bg="gold")
