import random
import tkinter as tk

BOARD_SIZE   = 10
CELL         = 50
MARGIN       = 20
WINDOW_W     = BOARD_SIZE*CELL + 2*MARGIN
WINDOW_H     = WINDOW_W + 90

SNAKES  = {16:6,  47:26, 49:11, 56:53, 62:19, 64:60,
           87:24, 93:73, 95:75, 98:78}
LADDERS = {1:38, 4:14, 9:31, 21:42, 28:84, 36:44,
           51:67, 71:91, 80:100}

class SnakesAndLadders(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snakes & Ladders – 2 Players")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=WINDOW_W, height=WINDOW_W, bg="white")
        self.canvas.pack()
        self.status = tk.Label(self, text="Player 1 to roll", font=("Helvetica", 16))
        self.status.pack()

        tk.Button(self, text="Roll", font=("Helvetica", 18), command=self.roll).pack(pady=5)

        self.players = [1, 1]
        self.turn    = 0              
        self.colors  = ["red", "blue"]
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        for num in range(1, BOARD_SIZE*BOARD_SIZE + 1):
            x, y = self._square_coords(num)
            color = "lightblue" if (num//BOARD_SIZE + num) % 2 else "lightgreen"
            self.canvas.create_rectangle(x, y, x+CELL, y+CELL,
                                         fill=color, outline="black")
            self.canvas.create_text(x+CELL//2, y+CELL//2, text=str(num),
                                    font=("Helvetica", 10, "bold"))

        for start, end in SNAKES.items():
            self._draw_arrow(start, end, "red", "S")
        for start, end in LADDERS.items():
            self._draw_arrow(start, end, "green", "L")

    def _square_coords(self, num):
        row, col = divmod(num-1, BOARD_SIZE)
        if row % 2 == 0:
            x = col
        else:
            x = BOARD_SIZE - 1 - col
        y = BOARD_SIZE - 1 - row
        return MARGIN + x*CELL, MARGIN + y*CELL

    def _square_center(self, num):
        x, y = self._square_coords(num)
        return x + CELL//2, y + CELL//2

    def _draw_arrow(self, start, end, color, label):
        x1, y1 = self._square_center(start)
        x2, y2 = self._square_center(end)
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill=color, width=4)
        midx, midy = (x1+x2)//2, (y1+y2)//2
        self.canvas.create_text(midx, midy, text=label, fill=color,
                                font=("Helvetica", 14, "bold"))
    def draw_pieces(self):
        self.canvas.delete("piece")
        for p, pos in enumerate(self.players):
            x, y = self._square_center(pos)
            radius = 15
            offset = 8 if p == 0 else -8
            self.canvas.create_oval(x+offset-radius, y-radius,
                                    x+offset+radius, y+radius,
                                    fill=self.colors[p], width=2,
                                    tags="piece")

    def roll(self):
        step = random.randint(1, 6)
        p = self.turn
        new_pos = self.players[p] + step

        if new_pos > 100:
            new_pos = self.players[p]       
        elif new_pos == 100:
            self.players[p] = 100
            self.draw_pieces()
            self.status.config(text=f"Player {p+1} rolled {step} and WINS!")
            return

        self.players[p] = new_pos
        self.draw_pieces()
        self.update_idletasks()
        self.after(300, lambda: self.check_snake_ladder(p, step))

    def check_snake_ladder(self, player, roll):
        pos = self.players[player]
        moved = False
        if pos in SNAKES:
            self.players[player] = SNAKES[pos]
            moved = True
        elif pos in LADDERS:
            self.players[player] = LADDERS[pos]
            moved = True

        if moved:
            self.draw_pieces()
            self.update_idletasks()
            self.after(300, lambda: self.check_snake_ladder(player, roll))
        else:
            self.turn = 1 - player
            self.status.config(text=f"Player {self.turn+1} to roll")

if __name__ == "__main__":
    SnakesAndLadders().mainloop()