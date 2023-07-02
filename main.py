from spends import *
from incomes import *


def expired():
    """
    Function to check if the trial period has expired.
    """
    with open("file_spend.json", "r") as data:
        time_first_use = base64.b64decode(json.load(data)["system_data"]).decode('utf-8')
    time_first_use = datetime.datetime.strptime(time_first_use, "%d/%m/%y")
    current_time = datetime.datetime.now()
    expired_time = time_first_use + datetime.timedelta(days=30)
    if current_time > expired_time:
        messagebox.showinfo(title="פג תוקף תקופת ניסיון", message="!מעכשיו אתה צריך לשלם")
        root.destroy()


column_incomes = 2
column = 0
FONT = ("Arial", 10, "bold")

# Labels
balance_title.grid(row=0, column=1)

balance_text_num.grid(row=1, column=0, columnspan=3)

title_label.grid(row=2, column=column)

sum_spends_label.grid(row=3, column=column, pady=(0, 40))

add_spend_label.grid(row=4, column=column, pady=1)

title_income_label.grid(row=2, column=column_incomes)

sum_income_label.grid(row=3, column=column_incomes, pady=(0, 40))

add_income_label.grid(row=4, column=column_incomes, pady=10)

label_category = Label(text=" :קטגוריה", font=("Normal", 11, "bold"), bg=YELLOW, fg="black")
label_category.grid(row=7, column=0, pady=(10, 20), sticky="e")

# Entry's
add_spend_entry.grid(row=6, column=column)

add_income_entry.grid(row=6, column=column_incomes)

add_category_choose.grid(row=7, column=column, pady=(10, 20))

# Buttons
add_button.grid(row=8, column=column)

delete_button.grid(row=9, column=column)

add_income_button.grid(row=8, column=column_incomes)

delete_income_button.grid(row=9, column=column_incomes)

history_button.grid(row=10, column=1, pady=(50, 5))

reset_button.grid(row=11, column=1, pady=(0, 5))


add_spend_entry.bind("<Return>", add_spend)
add_category_choose.bind("<Return>", add_spend)
add_income_entry.bind("<Return>", add_incomes)


def main():
    update_spending()
    update_incomes()
    expired()
    root.mainloop()


if __name__ == "__main__":
    main()