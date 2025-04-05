from tkinter import Toplevel, Label, Button
from ui_operations import center_window
from stocks_utils import *
from data_operations import save_data

def show_statistics(game, ui):
    stats_window = Toplevel(ui.root)
    stats_window.title("Investment Statistics")
    stats_window.geometry("600x500")
    stats_window.configure(bg="#00008B")
    stats_window.resizable(False, False)
    center_window(stats_window, 600, 500)

    Label(stats_window, text="Investment Performance:", font=("Arial", 16, "bold"),
          bg="#00008B", fg="white").pack(pady=10)

    for inv_name, data in game.investments_data.items():
        if "symbol" in data:
            current_price = fetch_stock_price(data["symbol"])
            purchase_price = data.get("purchase_price", 0)
            if current_price is None:
                trend = "N/A"
            elif current_price > purchase_price:
                trend = "↑"
            elif current_price < purchase_price:
                trend = "↓"
            else:
                trend = ""
            Label(stats_window,
                  text=f"{inv_name}: Invested {data['amount']}, Purchase Price: {purchase_price:.2f}, "
                       f"Current Price: {current_price:.2f} {trend}",
                  font=("Arial", 12), bg="#00008B", fg="white").pack(pady=5)
        else:
            profit = data.get("profit", 0)
            Label(stats_window, text=f"{inv_name}: Invested {data['amount']}, Profit: {profit}",
                  font=("Arial", 12), bg="#00008B", fg="white").pack(pady=5)

    Button(stats_window, text="Withdraw Money", font=("Arial", 14), command=lambda: cash_out(game, ui, stats_window)).pack(pady=10)


def cash_out(game, ui, stats_window):
    total_profit = 0

    for inv_name in list(game.investments_data.keys()):
        data = game.investments_data[inv_name]
        if "symbol" in data:
            current_price = fetch_stock_price(data["symbol"])
            purchase_price = data.get("purchase_price", 0)
            if current_price is not None and purchase_price > 0:
                profit = (current_price - purchase_price) * (data["amount"] / purchase_price)
                total_profit += profit + data["amount"]  # Додаємо інвестовану суму назад
        else:
            total_profit += data.get("profit", 0) + data["amount"]  # Включаємо початкову інвестицію

        del game.investments_data[inv_name]  # Видаляємо інвестицію

    game.capital += total_profit  # Додаємо загальний прибуток до капіталу
    ui.update_sum_ui(game)
    save_data(game.capital, game.investments_data)
    print(f"Money withdrawn: {total_profit:.2f}, New capital: {game.capital:.2f}")
    stats_window.destroy()