from tkinter import Toplevel, Label
from ui_operations import center_window


def show_rules(root):
    rules_window = Toplevel(root)
    rules_window.title("Game Rules")
    # Не центруємо та не задаємо розміри, оскільки це Toplevel
    rules_window.configure(bg="#00008B")

    #Тект в вікні rules

    rules_text = (
        "You will be given starting money which is 100000.\n"
        "You will have to spend the money wisely to earn yourself more money\n"
        "by investing into different areas.\n"
        "You will be shown the money you earn.\n"
        "Good luck and have fun!"
    )

    rules_label = Label(rules_window, text=rules_text, font=("Arial", 14), bg="#00008B", fg="white", justify="left")
    rules_label.pack(padx=20, pady=20)