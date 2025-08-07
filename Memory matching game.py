import tkinter as tk
import random
import time

# Constants
ROWS = 4
COLS = 4
CARD_WIDTH = 6
CARD_HEIGHT = 3
DELAY = 1000  # ms

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Memory Matching Game")
        self.buttons = {}
        self.first = None
        self.second = None
        self.matches_found = 0
        self.create_game()

    def create_game(self):
        values = list("AABBCCDDEEFFGGHH")
        random.shuffle(values)
        self.cards = {}
        for r in range(ROWS):
            for c in range(COLS):
                value = values.pop()
                btn = tk.Button(self.root, text=" ", width=CARD_WIDTH, height=CARD_HEIGHT,
                                command=lambda r=r, c=c: self.reveal_card(r, c))
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[(r, c)] = btn
                self.cards[(r, c)] = value

    def reveal_card(self, r, c):
        if self.buttons[(r, c)]["text"] != " ":
            return  # already revealed or matched

        if self.first and self.second:
            return  # wait for comparison

        self.buttons[(r, c)]["text"] = self.cards[(r, c)]
        self.buttons[(r, c)].update()

        if not self.first:
            self.first = (r, c)
        elif not self.second:
            self.second = (r, c)
            self.root.after(DELAY, self.check_match)

    def check_match(self):
        r1, c1 = self.first
        r2, c2 = self.second

        if self.cards[(r1, c1)] == self.cards[(r2, c2)]:
            self.buttons[(r1, c1)]["state"] = "disabled"
            self.buttons[(r2, c2)]["state"] = "disabled"
            self.matches_found += 1
            if self.matches_found == (ROWS * COLS) // 2:
                self.show_win_message()
        else:
            self.buttons[(r1, c1)]["text"] = " "
            self.buttons[(r2, c2)]["text"] = " "

        self.first = None
        self.second = None

    def show_win_message(self):
        win_label = tk.Label(self.root, text="🎉 You won!", font=("Arial", 16), fg="green")
        win_label.grid(row=ROWS, column=0, columnspan=COLS, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

