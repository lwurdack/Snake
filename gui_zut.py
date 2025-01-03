
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def visualize_snake_game(snake_history, food_history, grid_size, speed):
    """
    Visulaisiert Snake über jede Iteration mit einem grid plot

    :param snake_history: Liste von Koordinaten der Schlangenkörpersegmente pro Iteration 
    :param food_history: Liste der Koordinaten vom Essen pro Iteration 
    :param grid_size: Größe des Spielfelds in (Zeile, Spalte) 
    :param speed: Geschwindigkeit der Visualisation in Sekunden pro iteration 
    """
    rows, cols = grid_size

    def update(frame):
        # Create an empty grid
        grid = np.zeros((rows, cols))

        # Place the food on the grid
        food_x, food_y = food_history[frame]
        if 0 <= food_x < rows and 0 <= food_y < cols:
            grid[food_x, food_y] = 0.5  # Represent food with a different intensity

        # Place the snake on the grid
        snake = snake_history[frame]
        for index, (x, y) in enumerate(snake):
            if 0 <= x < rows and 0 <= y < cols:
                grid[x, y] = 1 - (index * 0.1)  # Gradually decrease intensity for snake body

        # Update the plot
        ax.clear()
        ax.imshow(grid, cmap="Greys", origin="upper")
        ax.set_title(f"Iteration {frame + 1}")
        ax.axis("off")

    # Set up the plot
    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, update, frames=len(snake_history), interval=speed * 1000, repeat=False)

    # Show the animation
    plt.show()