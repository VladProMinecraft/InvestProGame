from data_operations import *



class InvestProGame:
    def __init__(self):
        self.capital, self.investments_data = load_data()

    def restart_game(self, ui):
        self.capital = INITIAL_CAPITAL
        self.investments_data.clear()
        ui.update_sum_ui(self)
        save_data(self.capital, self.investments_data)
        print("Game Restarted!")
