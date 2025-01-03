from evolution_zut import evolution_step
from tqdm import tqdm 

if __name__ == "__main__":
    NUM_TREES = 100
    NUM_GENERATIONS = 100
    FUNCTION_SET = ["food_left", "food_right", "food_front", "danger_left", "danger_right", "danger_front",
                    "current_up", "current_down", "current_left", "current_right"]
    ACTION_SET = ["left", "right", "front"]
    MAX_DEPTH = 6

    print("Erzeuge die erste Generation...")
    current_generation, _, _, _ = evolution_step(num_trees=NUM_TREES, function_set=FUNCTION_SET, action_set=ACTION_SET, max_depth=MAX_DEPTH)

    best_results = []

    for gen in tqdm(range(1, NUM_GENERATIONS + 1), desc="Generationenfortschritt", unit="Generation"):
        current_generation, best_fitness, best_score, best_tree = evolution_step(
            current_generation=current_generation,
            num_trees=NUM_TREES,
            function_set=FUNCTION_SET,
            action_set=ACTION_SET,
            max_depth=MAX_DEPTH,
            generation=gen
        )

        best_results.append((gen, best_fitness, best_score, best_tree))

    print("\n--- Zusammenfassung der besten Spieler und Scores ---")
    for gen, fitness, score, tree in best_results:
        print(f"Generation {gen}: Bester Score: {score}, Beste Fitness: {fitness}")
