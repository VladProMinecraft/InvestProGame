from tkinter import Frame, Button, Label, Tk
from rules_window import show_rules
from invest_window import invest
from statistics_window import show_statistics
from ui_operations import center_window

class UserInterface:
    def __init__(self, game):
        self.root = Tk()
        self.label_sum = Label(self.root, text=f"Sum: {game.capital}", font=("Arial", 20, "bold"),
                          bg="#00008B", fg="white")
        self.game = game

    def setup_ui(self, game):
        self.root.title("InvestProMinecraft")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.configure(bg="#00008B")

        top_frame = Frame(self.root, bg="#0000FF", width=screen_width, height=100)
        top_frame.place(x=0, y=0)

        Label(top_frame, text="InvestProMinecraft", font=("Arial", 24, "bold"),
              bg="#0000FF", fg="white").place(relx=0.5, rely=0.5, anchor="center")

        self.label_sum.place(x=10, y=120, anchor="w")

        def show_rules_command():
            show_rules(self.root)

        def invest_command():
            invest(self.root, game, self)

        def show_statistics_command():
            show_statistics(game, self)

        def restart_game_command():
            self.game.restart_game(self)

        Button(self.root, text="Rules", font=("Arial", 18), width=10, height=2, command=show_rules_command) \
            .place(x=10, rely=1.0, anchor="sw", y=-10)
        Button(self.root, text="Invest", font=("Arial", 18), width=10, height=2, command=invest_command) \
            .place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        Button(self.root, text="Statistics", font=("Arial", 18), width=10, height=2, command=show_statistics_command) \
            .place(relx=1.0, x=-10, y=120, anchor="ne")
        Button(self.root, text="Restart", font=("Arial", 18), width=15, height=2, command=restart_game_command) \
            .place(relx=0.5, rely=1.0, anchor="s", y=-10)

    def update_sum_ui(self, game):
        self.label_sum.config(text=f"Sum: {game.capital}")