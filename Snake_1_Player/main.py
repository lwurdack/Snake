from gp_player import decision_tree, genetic_programming
from gui import SnakeGameGUI
from game import SnakeGame

if __name__ == "__main__":
    game_size = 20  # Spielfeldgröße
    population_size = 20  # Anzahl der Spieler pro Generation
    generations = 10000  # Anzahl der Generationen

    print("Optimizing GP Player...")
    best_tree = genetic_programming(population_size=population_size, generations=generations, game_size=game_size)
    print("Best Strategy:", best_tree)

    # GUI: Spiel mit dem besten Entscheidungsbaum anzeigen
    def play_with_gui():
        game = SnakeGame(game_size)  # Neues Spiel starten
        gui = SnakeGameGUI(game, size=400, tree=best_tree)  # GUI erstellen

        # Entscheidungsbaum verwenden, um Bewegungen zu steuern
        def play_step():
            if not game.done:
                state = game.get_state()
                action = decision_tree(state, best_tree)  # Bewegung aus Entscheidungsbaum
                game.move(action)
                gui.draw()
                gui.root.after(200, play_step)  # Nächster Schritt nach 200ms
            else:
                print(f"Game Over. Score: {game.score}")

        # Spiel starten
        play_step()
        gui.root.mainloop()

    # Spiel mit GUI starten
    play_with_gui()
