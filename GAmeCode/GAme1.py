import tkinter as tk
import random

# Game Constants
WIDTH, HEIGHT = 10, 10  # Grid size
CELL_SIZE = 40  # Size of each cell in pixels
DIRECTION_MAP = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}


class WormGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Worm Game")

        self.canvas = tk.Canvas(root, width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, bg="white")
        self.canvas.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.running = False
        self.worm = [(WIDTH // 2, HEIGHT // 2)]  # Start position
        self.direction = "Right"
        self.food = self.place_food()
        self.score = 0

        self.root.bind("<KeyPress>", self.change_direction)

    def start_game(self):
        self.running = True
        self.start_button.destroy()  # Remove start button after clicking
        self.update_game()

    def restart_game(self):
        self.worm = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = "Right"
        self.food = self.place_food()
        self.score = 0
        self.running = True
        self.restart_button.destroy()  # Remove restart button
        self.update_game()

    def place_food(self):
        while True:
            food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if food not in self.worm:
                return food

    def change_direction(self, event):
        if event.keysym in DIRECTION_MAP and self.running:
            self.direction = event.keysym

    def update_game(self):
        if not self.running:
            return

        head_x, head_y = self.worm[0]
        move_x, move_y = DIRECTION_MAP[self.direction]
        new_head = (head_x + move_x, head_y + move_y)

        if new_head in self.worm or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            self.root.title(f"Game Over! Score: {self.score}")
            self.running = False
            self.restart_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
            self.restart_button.pack()
            return

        self.worm.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.place_food()
        else:
            self.worm.pop()

        self.draw_grid()
        self.root.after(200, self.update_game)

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                x1, y1 = x * CELL_SIZE, y * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

        for segment in self.worm:
            x1, y1 = segment[0] * CELL_SIZE, segment[1] * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")

        x1, y1 = self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        self.canvas.create_oval(x1, y1, x2, y2, fill="red")

        self.root.title(f"Worm Game - Score: {self.score}")


# Run the game
root = tk.Tk()
game = WormGame(root)
root.mainloop()
