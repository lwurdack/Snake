from game import SnakeGame, UP, DOWN, LEFT, RIGHT
import tkinter as tk
from gp_player import decision_tree

class SnakeGameGUI:
    def __init__(self, game, size, tree):
        self.game = game
        self.size = size
        self.cell_size = size // game.size
        self.tree = tree  # Entscheidungsbaum vom GP-Player

        # Tkinter-Fenster erstellen
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(self.root, width=size, height=size, bg="black")
        self.canvas.pack()

        # Fortschrittsanzeige
        self.progress_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="black", fg="white")
        self.progress_label.pack()

    def draw(self):
        """Zeichnet das aktuelle Spiel auf die Canvas."""
        self.canvas.delete("all")

        # Zeichne die Schlange
        for segment in self.game.snake:
            x1 = segment[1] * self.cell_size
            y1 = segment[0] * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="")

        # Zeichne die Nahrung
        food_x = self.game.food[1] * self.cell_size
        food_y = self.game.food[0] * self.cell_size
        self.canvas.create_oval(food_x, food_y, food_x + self.cell_size, food_y + self.cell_size, fill="red", outline="")

    def update(self, generation=None, game_num=None, total_games=None, step=None):
        """Aktualisiert das Spiel basierend auf den Regeln des Entscheidungsbaums."""
        if not self.game.done:
            # Automatische Bewegung durch GP-Player
            state = self.game.get_state()
            direction = decision_tree(state, self.tree)  # Entscheidungsbaum verwenden
            self.game.move(direction)  # Übergib die Richtung an die move-Methode
            self.draw()

            # Fortschrittstext aktualisieren
            progress_text = f"Generation: {generation}, Spiel: {game_num}/{total_games}"
            if step is not None:
                progress_text += f", Zug: {step}"
            self.progress_label.config(text=progress_text)

            # Update alle 200ms
            self.root.after(200, lambda: self.update(generation, game_num, total_games, step=step + 1 if step else 1))
        else:
            # Spiel beendet: Zeige "Game Over"
            self.canvas.create_text(self.size // 2, self.size // 2, text="Game Over", fill="white", font=("Helvetica", 24))

    def run_single_game(self, generation=None, game_num=None, total_games=None):
        """Startet das Spiel mit der GUI."""
        self.update(generation, game_num, total_games, step=1)
        self.root.mainloop()
