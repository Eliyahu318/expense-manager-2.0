import base64
import datetime
import json
from tkinter import Label, Entry, Button, END, Toplevel, messagebox, W
from incomes import root, balance_calculate, update_incomes

DEFAULT_SPENDS = [0, None]
DEFAULT_INCOMES = 0
YELLOW = "#f7f5dd"


def add_spend(event=None):
    current_date = datetime.datetime.now()
    current_date_str = current_date.strftime("%d/%m/%y-%H:%M:%S")
    category = add_category_choose.get() + '#'[1:]
    expense = [int(add_spend_entry.get().split("#")[0]), category]
    with open("file_spend.json", "r+") as file:
        data = json.load(file)
        data["spends"][current_date_str] = expense
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)

    update_spending()


def delete_last_add_spend():
    with open("file_spend.json", "r+") as file:
        data = json.load(file)
        if len(data["spends"]) > 1:
            data["spends"].popitem()
        else:
            messagebox.showinfo(title="שגיאה", message="אין הוצאות למחוק")
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)
    update_spending()


def update_spending():
    try:
        with open("file_spend.json", "r+") as data_file:
            data = json.load(data_file)["spends"].items()
            spend = sum([value[0] for key, value in data])
    except FileNotFoundError:
        with open("file_spend.json", "w") as file:
            time = datetime.datetime.now().strftime("%d/%m/%y")
            SYSTEM_DATA = base64.b64encode(time.encode('utf-8')).decode('utf-8')
            json.dump({"system_data": SYSTEM_DATA, "spends": {"default": DEFAULT_SPENDS},
                       "incomes": {"default": DEFAULT_INCOMES}},
                      file, indent=4)
        with open("file_spend.json", "r") as data_file:
            data = json.load(data_file)["spends"].items()
            spend = sum([value[0] for key, value in data if key != "history"])
    formatted_spend = "{:,.0f}".format(spend)  # Format spending with commas
    sum_spends_label.config(text=formatted_spend)
    add_spend_entry.delete(first=0, last=END)
    add_category_choose.delete(first=0, last=END)
    add_category_choose.insert(END, string="כללי")
    balance_calculate()


def delete_choosing_history_label(title, content, row, column, buttons_list, labels_list):
    """
    Delete a specific entry from the spending history.
    Args:
        title (str): The title of the entry (e.g., "spends", "incomes").
        content (str): The content of the entry to be deleted.
        row (str): The row position of the button and label to be removed.
        column (str): The column position of the button and label to be removed.
        buttons_list (list): A list containing the buttons.
        labels_list (list): A list containing the labels.
    """
    with open("file_spend.json", "r+") as data_file:
        data = json.load(data_file)
        del data[title][content]
        # with open("file_spend.json", "w") as file:
        data_file.seek(0)
        data_file.truncate()
        json.dump(data, data_file, indent=4)

    row = int(row)
    column = int(column)
    button_to_delete = buttons_list[column][row]
    button_to_delete.grid_forget()
    label_to_delete = labels_list[column][row]
    label_to_delete.grid_forget()

    update_spending()
    update_incomes()


new_window = None
label_title_history = None
content_label = None


def history():
    """
    Display the spending and income history in a new window.
    Allows deleting specific entries and generating a pie chart.
    """
    global new_window, label_title_history, content_label
    new_window = Toplevel(root)
    new_window.title("פירוט היסטוריה")
    new_window.config(padx=30, pady=50, bg=YELLOW)

    list_buttons = []
    list_labels = []
    with open("file_spend.json", "r") as data_file:
        data = json.load(data_file)
        del data["system_data"]

        column = 0  # Track the current column
        for key_title in data:
            row = 0
            if column == 0:
                translate_key_title = "הוצאות"
            elif column == 2:
                translate_key_title = "הכנסות"
            else:
                translate_key_title = "היסטוריה"
            label_title_history = Label(new_window, text=f"{translate_key_title}", bg=YELLOW,
                                        font=("Arial", 18, "bold"))
            label_title_history.grid(row=row, column=column, padx=20, pady=20, sticky=W)

            row_buttons = [None]
            row_labels_content = [None]
            for date, money in data[key_title].items():
                row += 1
                if date != "default":
                    try:
                        content_text = f"{date[:8]}: {money[0]} - {money[1]}"
                    except TypeError:
                        content_text = f"{date[:8]}: {money}"
                    content_label = Label(new_window, text=content_text, bg=YELLOW, font=("Arial", 10, "normal"))
                    if key_title == "spends":
                        content_label.config(fg="red")
                    elif key_title == "incomes":
                        content_label.config(fg="green")
                    else:
                        content_text = f"{date}:  {'{:,.0f}'.format(money)}"
                        content_label.config(text=content_text, fg="black", font=("Arial black", 10, "normal"))
                    content_label.grid(row=row, column=column, sticky='s')
                    row_labels_content.append(content_label)

                    if key_title != "history":
                        delete_button_value = Button(new_window, width=3, height=1, text="מחק", bg="red")
                        delete_button_value.grid(row=row, column=column + 1, padx=(0, 20), pady=3, sticky=W)

                        row_index = row - 1
                        column_index = column
                        if column != 0:
                            column_index = 1
                        delete_button_value.configure(
                            command=lambda title=key_title, content=date, r=row_index, c=column_index,
                                           buttons=list_buttons,
                                           labels=list_labels: (
                                delete_choosing_history_label(title, content, r, c, buttons, labels)))
                        row_buttons.append(delete_button_value)

            if len(row_buttons) > 1:
                list_buttons.append(row_buttons)
            if len(row_labels_content) > 1:
                list_labels.append(row_labels_content)
            column += 2

        def create_pie_graph():
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
            """
            Generate a pie chart representing the expense categories.
            """
            list_expenses = [expense for date, expense in data["spends"].items() if date != "default"]
            dict_category_expense = {}
            for expense, category in list_expenses:
                if category in dict_category_expense:
                    dict_category_expense[category] = dict_category_expense[category] + expense
                else:
                    dict_category_expense[category] = expense

            labels_for_pie = [category[::-1] for category, expense in dict_category_expense.items()]
            numbers_for_pie = [expense for category, expense in dict_category_expense.items()]

            if len(labels_for_pie) < 7:
                fig = Figure(figsize=(4, 4), dpi=100)
            else:
                fig = Figure(figsize=(5, 5), dpi=100)
            fig.set_facecolor(YELLOW)
            ax = fig.add_subplot(111)

            labels = labels_for_pie
            sizes = numbers_for_pie

            ax.bar(labels, sizes)

            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.get_tk_widget().grid(row=0, column=5, columnspan=3, rowspan=row_pie_button, sticky='nsew')

            button_out = Button(master=canvas.get_tk_widget(), text="x", font=("Normal", 10, "bold"),
                                highlightthickness=0)
            button_out.configure(compound='center', command=lambda: canvas.get_tk_widget().grid_forget(), bg=YELLOW,
                                 fg="red")
            canvas.get_tk_widget().create_window(450, 30, window=button_out)

        pie_button = Button(new_window, text="גרף ניתוח הוצאות", command=create_pie_graph, bg="gold",
                            font=("Normal", 10, "bold"))
        row_pie_button = [len(x) for x in list_labels][0] + 5
        pie_button.grid(row=row_pie_button, column=1, columnspan=3, pady=30)

        new_window.mainloop()


def reset_all():
    is_ok = messagebox.askokcancel(title="Reset", message="?אתה בטוח שאתה רוצה לאפס הכל")
    if is_ok:
        with open("file_spend.json", "r+") as data_file:
            dict_data = json.load(data_file)
            dict_data["incomes"] = {"default": DEFAULT_INCOMES}
            dict_data["spends"] = {"default": DEFAULT_SPENDS}
            current_month = datetime.datetime.now().strftime("%m/%y")
            dict_data["history"] = {current_month: balance_calculate()}
            data_file.seek(0)
            data_file.truncate()
            json.dump(dict_data, data_file, indent=4)
        update_incomes()
        update_spending()


# Labels
title_label = Label(text=":הוצאות החודש", font=("Normal", 16, "bold"), bg=YELLOW, fg="black")

sum_spends_label = Label(font=("Normal", 24, "bold"), bg=YELLOW, fg="red")

add_spend_label = Label(text=":הוסף הוצאה", font=("Normal", 16, "bold"), bg=YELLOW, fg="black")

# Entry's
add_spend_entry = Entry(width=20, font=("Normal", 10, "bold"))
add_spend_entry.focus()

add_category_choose = Entry(width=13, font=("Normal", 10, "bold"))

# Buttons
add_button = Button(text="הוסף", font=("Normal", 10, "bold"), command=add_spend, width=12, bg="gold")

delete_button = Button(text="מחק", font=("Normal", 10, "bold"), command=delete_last_add_spend, width=12, bg="gold")

reset_button = Button(text="איפוס", font=("Normal", 10, "bold"), command=reset_all, width=7, bg="red")

history_button = Button(text="היסטוריה", font=("Normal", 10, "bold"), command=history, width=7, bg="gray")
