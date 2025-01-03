
from game_zut import snake, UP, DOWN, LEFT, RIGHT
import decision_tree_zut
import gui_zut 
import random
from fitness_zut import calculate_fitness
from crossover_mutation_zut import create_next_generation


def run_game_with_tree(tree, visualize=False, size=20, max_moves=1000):
    game = snake(size)
    variables = {}
    move_count = 0

    if visualize:
        snake_history = []
        food_history = []

    while not game.end:
        if visualize:
            s = game.snake
            f = game.food
            snake_history.append(tuple(s))
            food_history.append(tuple(f))

        game.move(game.direction)
        if move_count >= max_moves:
            break

        state = game.state()
        directions = ["front", "left", "right"]
        for direction in directions:
            variables[f"food_{direction}"] = state[direction] == 'food'
            variables[f"danger_{direction}"] = state[direction] == 'obstacle'

        variables["current_up"] = game.direction == UP
        variables["current_down"] = game.direction == DOWN
        variables["current_left"] = game.direction == LEFT
        variables["current_right"] = game.direction == RIGHT

        action = tree.return_action(variables)

        relative_directions = {
            UP: {"left": LEFT, "right": RIGHT, "front": UP},
            DOWN: {"left": RIGHT, "right": LEFT, "front": DOWN},
            LEFT: {"left": DOWN, "right": UP, "front": LEFT},
            RIGHT: {"left": UP, "right": DOWN, "front": RIGHT}
        }

        new_direction = relative_directions[game.direction][action]
        game.direction = new_direction
        move_count += 1

    final_fitness = calculate_fitness(game.score, move_count, score_weight=1.0, time_weight=0.5)
    return final_fitness, game.score



def tournament_selection(population):
    if len(population) == 0:
        raise ValueError("Die Population ist leer. Überprüfe die vorherigen Schritte.")
    if len(population) % 2 != 0:
        raise ValueError("Die Population muss eine gerade Anzahl an Individuen enthalten.")

    winners = []

    # Shuffle the population to randomize pairings
    random.shuffle(population)

    # Conduct 1v1 tournaments
    for i in range(0, len(population), 2):
        pair = population[i:i + 2]  # Take two individuals
        if len(pair) == 2:
            # Determine the winner of this match
            winner = max(pair, key=lambda x: x[1])
            winners.append(winner)

    return winners


def evolution_step(current_generation=None, num_trees=100, function_set=None, action_set=None, max_depth=6, generation=0):
    if current_generation is None:
        current_generation = [
            (decision_tree_zut.generate_random_dt(function_set, action_set, max_depth=max_depth), 0)
            for _ in range(num_trees)
        ]


        

    print("Current Generation", current_generation)
    tree_fitness = []
    for tree_data in current_generation:
        if isinstance(tree_data, tuple):
            try:
                fitness, score = run_game_with_tree(tree_data[0])  # Verwende nur den Baum
                tree_fitness.append((tree_data[0], fitness, score))
            except Exception as e:
                print(f"Fehler beim Ausführen von run_game_with_tree: {e}, Baum: {tree_data[0]}")
        else:
            fitness, score = run_game_with_tree(tree_data)
            tree_fitness.append((tree_data, fitness, score))

    print("Tree Fitness Generation", tree_fitness)


    print(len(tree_fitness))
    best_fitness = -1
    best_tree = -1
    best_score = -1
    for tree, fitness, score in tree_fitness:
        #print(tree)
        if fitness > best_fitness:
            best_tree = tree
            best_fitness = fitness
            best_score = score

    
    print(f"Generation {generation}: Bester Score: {best_score}, Beste Fitness: {best_fitness}")
    winners = tournament_selection(tree_fitness)
    print(len(winners))
    current_generation = create_next_generation(winners, function_set, action_set, max_depth)
    return current_generation, best_fitness, best_score, best_tree
