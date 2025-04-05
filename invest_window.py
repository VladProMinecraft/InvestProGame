from tkinter import Toplevel, Label, Frame, Entry, StringVar, ttk, Button, END
from stocks_utils import *
from random import randint
from data_operations import save_data
from ui_operations import center_window
# коас який відповідаж за іместування
class InvestLogic:
    def __init__(self, name, info, amount_entry, quantity_label, currency_choice, game, error_label, ui):
        self.name = name
        self.info = info
        self.amount_entry = amount_entry
        self.quantity_label = quantity_label
        self.currency_choice = currency_choice
        self.game = game
        self.error_label = error_label
        self.ui = ui

    def invest_action(self):
        amount_str = self.amount_entry.get()

        if not amount_str.isdigit():
            self.error_label["text"] = "Input numbers"
            return

        amount = int(amount_str)

        if amount > self.game.capital:
            self.error_label["text"] = "Not enough funds"
            return

        symbol = self.info.get("symbol")
        if self.currency_choice and self.currency_choice.get():
            if self.name == "Cryptocurrency" and self.currency_choice.get() == "ETH":
                symbol = "ETH-USD"
            elif self.name == "Currency" and self.currency_choice.get() == "EUR":
                symbol = "EURUSD=X" # Залишаємо EURUSD як базову пару

        if self.info["type"] == "stock" and symbol:
            purchase_price = fetch_stock_price(symbol)     #встановлює ціну з fetch_stock_price
            if purchase_price is None:
                self.error_label["text"] = "Failed to fetch price"
                return
            self.game.investments_data[self.name] = {
                "amount": amount,
                "symbol": symbol,
                "purchase_price": purchase_price,
                "currency": self.currency_choice.get() if self.currency_choice else None
            }
        elif self.info["type"] == "crypto" and symbol:
            purchase_price = fetch_stock_price(symbol)
            if purchase_price is None:
                self.error_label["text"] = "Failed to fetch price"
                return
            self.game.investments_data[self.name] = {
                "amount": amount,
                "symbol": symbol,
                "purchase_price": purchase_price,
                "currency": self.currency_choice.get() if self.currency_choice else None
            }
        else:
            profit = randint(1, 100000)
            self.game.investments_data[self.name] = {
                "amount": amount,
                "profit": profit
            }
        self.game.capital -= amount
        self.ui.update_sum_ui(self.game)
        save_data(self.game.capital, self.game.investments_data)
        self.amount_entry.delete(0, END)
        print(f"Invested in {self.name}: {amount} with details: {self.game.investments_data.get(self.name)}")
#показує кількість
def update_quantity(investment_name, invest_info, amount_str_var, quantity_label, currency_choice, *args):
    amount_str = amount_str_var.get()
    quantity_label.config(text="")
    if amount_str.isdigit():
        amount = int(amount_str)
        symbol = invest_info.get("symbol")
        if currency_choice and currency_choice.get():
            if investment_name == "Cryptocurrency" and currency_choice.get() == "ETH":
                symbol = "ETH-USD"
            elif investment_name == "Currency" and currency_choice.get() == "EUR":
                symbol = "EURUSD=X"

        if invest_info["type"] == "stock" and symbol:
            current_price = fetch_stock_price(symbol)
            if current_price is not None and current_price > 0:
                quantity = amount / current_price
                quantity_label.config(text=f"Quantity: {quantity:.4f}")
            elif current_price is not None and current_price <= 0:
                quantity_label.config(text="Price not available")
            else:
                quantity_label.config(text="Failed to fetch price")
        elif invest_info["type"] == "crypto" and symbol:
            current_price = fetch_stock_price(symbol)
            if current_price is not None and current_price > 0:
                quantity = amount / current_price
                quantity_label.config(text=f"Quantity: {quantity:.8f}")
            elif current_price is not None and current_price <= 0:
                quantity_label.config(text="Price not available")
            else:
                quantity_label.config(text="Failed to fetch price")
        elif invest_info["type"] == "non-stock":
            quantity_label.config(text="Fixed value")
#кнопка інвест
def invest(root, game, ui):
    invest_window = Toplevel(root)
    invest_window.title("Investments")
    invest_window.geometry("700x400")
    invest_window.configure(bg="#00008B")
    invest_window.resizable(False, False)
    center_window(invest_window, 700, 400)

    Label(invest_window, text="Choose an investment sector:", font=("Arial", 16, "bold"),
          bg="#00008B", fg="white").pack(pady=10)
    #вибір інвестицій
    investments = {
        "Cryptocurrency": {"symbol": "BTC-USD", "type": "crypto", "options": ["BTC", "ETH"]},
        "Currency": {"symbol": "EURUSD=X", "type": "stock", "options": ["UAH", "EUR"]},
        "Deposit": {"symbol": None, "type": "non-stock", "options": []},
        "Bonds": {"symbol": None, "type": "non-stock", "options": []},
        "Military Bonds": {"symbol": None, "type": "non-stock", "options": []}
    }

    error_label = Label(invest_window, text="", font=("Arial", 12, "bold"),
                        bg="#00008B", fg="red")
    error_label.pack(pady=5)

    investment_frames = {}
    amount_entries = {}
    quantity_labels = {}
    amount_str_vars = {}
    currency_choices = {}

    for investment_name, info in investments.items():
        frame = Frame(invest_window, bg="#00008B")
        frame.pack(pady=5, fill="x", padx=20)
        investment_frames[investment_name] = frame

        investment_label = Label(frame, text=investment_name, font=("Arial", 14), width=20, bg="#00008B",
                                 fg="white", anchor="w")
        investment_label.pack(side="left", padx=10)

        invest_button = Button(frame, text="Invest", font=("Arial", 14),
                               command=InvestLogic(investment_name, info, None, None, None, game, error_label, ui).invest_action)
        invest_button.pack(side="left", padx=10)

        currency_choice = None
        if info.get("options"):
            currency_choice = StringVar(frame)
            currency_choice.set(info["options"][0])
            currency_choices[investment_name] = currency_choice
            currency_dropdown = ttk.Combobox(frame, textvariable=currency_choice, values=info["options"], width=5)
            currency_dropdown.pack(side="left", padx=10)

        amount_str_var = StringVar()
        amount_entry = Entry(frame, font=("Arial", 14), width=10, textvariable=amount_str_var)
        amount_entries[investment_name] = amount_entry
        amount_entry.bind("<FocusIn>", lambda event: clear_error(error_label))
        amount_str_vars[investment_name] = amount_str_var
        amount_entry.pack(side="left", padx=10)

        quantity_label = Label(frame, text="", font=("Arial", 12), bg="#00008B", fg="yellow", width=15, anchor="w")
        quantity_label.pack(side="left", padx=10)
        quantity_labels[investment_name] = quantity_label

        # Оновлення InvestLogic
        invest_logic = InvestLogic(investment_name, info, amount_entry, quantity_label, currency_choice, game, error_label, ui)
        invest_button.config(command=invest_logic.invest_action)

        # Прив'язка trace_add
        amount_str_var.trace_add("write", lambda *args, name=investment_name, inf=info, var=amount_str_var, q_lbl=quantity_label, c_choice=currency_choice: update_quantity(name, inf, var, q_lbl, c_choice, *args))

def clear_error(error_label):
    error_label["text"] = ""