from invest_pro_game import InvestProGame
from user_interface import UserInterface

def start_game():

    game = InvestProGame()
    ui = UserInterface(game)
    ui.setup_ui(game)

    ui.root.mainloop()

