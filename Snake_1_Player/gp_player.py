import random
from game import UP, DOWN, LEFT, RIGHT, MOVES, SnakeGame

# Generiere einen zufälligen Entscheidungsbaum mit dynamischer Tiefe
def generate_random_tree(depth):
    if depth == 0:
        return random.choice(MOVES)
    condition = random.choice(["state['food_relative']['UP']", 
                                "state['distance_to_wall']['UP'] > 1", 
                                "state['distance_to_wall']['RIGHT'] < 3"])
    return {
        condition: (generate_random_tree(depth - 1), generate_random_tree(depth - 1))
    }

# Evaluiere den Entscheidungsbaum basierend auf dem Zustand
def decision_tree(state, tree):
    if isinstance(tree, dict):
        condition = list(tree.keys())[0]
        if eval(condition):
            return decision_tree(state, tree[condition][0])
        else:
            return decision_tree(state, tree[condition][1])
    else:
        return tree

# Fitness-Funktion für das Snake-Spiel
def fitness_function(game):
    score = game.score * 10
    survival_time = len(game.snake)
    penalty = game.steps_without_food * 0.1
    return score + survival_time - penalty

# Evaluierung der Strategie eines Baums
def evaluate_strategy(tree, game):
    for _ in range(100):
        if game.done:
            break
        state = game.get_state()
        direction = decision_tree(state, tree)
        game.move(direction)
    return fitness_function(game)

# Mutation eines Entscheidungsbaums mit dynamischer Tiefe
def mutate_tree(tree, depth):
    if random.random() < 0.3 or depth == 0:
        return generate_random_tree(depth)
    if isinstance(tree, dict):
        condition = list(tree.keys())[0]
        tree[condition] = (
            mutate_tree(tree[condition][0], depth - 1),
            mutate_tree(tree[condition][1], depth - 1)
        )
    return tree

# Crossover zwischen zwei Entscheidungsbäumen
def crossover_tree(tree1, tree2):
    if random.random() < 0.5 and isinstance(tree1, dict) and isinstance(tree2, dict):
        condition1 = list(tree1.keys())[0]
        condition2 = list(tree2.keys())[0]
        return {
            condition1: (
                crossover_tree(tree1[condition1][0], tree2[condition2][0]),
                crossover_tree(tree1[condition1][1], tree2[condition2][1]),
            )
        }
    return random.choice([tree1, tree2])

# Hauptfunktion für Genetic Programming
def genetic_programming(population_size=20, generations=50, game_size=10):
    max_depth = 3  # Starttiefe
    population = [generate_random_tree(depth=max_depth) for _ in range(population_size)]

    for generation in range(generations):
        max_depth = 3 + generation // 10  # Dynamische Erhöhung der Tiefe
        scores = []

        for tree in population:
            game = SnakeGame(game_size)
            score = evaluate_strategy(tree, game)
            scores.append(score)

        # Sortiere die Population basierend auf den Scores
        sorted_population = [x for _, x in sorted(zip(scores, population), key=lambda pair: pair[0], reverse=True)]

        elite_size = int(0.2 * population_size)
        mutation_size = int(0.6 * population_size)
        new_population = sorted_population[:elite_size]

        # Fülle die Population mit Mutationen und Crossovers
        while len(new_population) < elite_size + mutation_size:
            parent1, parent2 = random.sample(sorted_population[:elite_size], 2)
            child = crossover_tree(parent1, parent2)
            if random.random() < 0.5:
                child = mutate_tree(child, depth=max_depth)
            new_population.append(child)

        # Füge zufällige neue Individuen hinzu
        while len(new_population) < population_size:
            new_population.append(generate_random_tree(depth=max_depth))

        population = new_population

        print(f"Generation {generation + 1}: Best Score = {max(scores)} | Max Depth = {max_depth}")

    return sorted_population[0]
