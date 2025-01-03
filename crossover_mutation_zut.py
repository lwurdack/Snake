import random
from decision_tree_zut import generate_random_dt, DecisionTreeNode
from fitness_zut import calculate_fitness  # Fitness-Berechnung importiert

# Funktion zur Erstellung der nächsten Generation basierend auf Vergleich, Mutation und Crossover
def create_next_generation(current_generation, function_set, action_set, max_depth=6):
    """
    Erzeugt die nächste Generation, indem zufällige Paare verglichen, mutiert, gekreuzt und neue Individuen erstellt werden.

    :param current_generation: Liste der aktuellen Generation (Individuen mit Fitness)
    :param function_set: Mögliche Bedingungen für die Bäume
    :param action_set: Mögliche Aktionen für die Blätter
    :param max_depth: Maximale Tiefe für Bäume
    :return: Liste der neuen Generation
    """
    next_generation = []

    # Vergleich in Paaren und Auswahl der Gewinner
    winners = []
    for _ in range(len(current_generation) // 2):
        ind1, ind2 = random.sample(current_generation, 2)  # Zwei Individuen auswählen
        winner = ind1 if ind1[1] > ind2[1] else ind2  # Das bessere Individuum bestimmen
        winners.append(winner)

    # 2/5 der Gewinner zufällig auswählen und mutieren
    num_mutations = len(winners) * 2 // 5
    mutated = [
        (mutate_tree(random.choice(winners)[0], function_set, action_set, max_depth), 0)
        for _ in range(num_mutations)
    ]

    # 2/5 der Gewinner zufällig auswählen für Crossover
    num_crossover = len(winners) * 2 // 5
    crossovered = []
    for _ in range(num_crossover // 2):
        parent1, parent2 = random.sample(winners, 2)
        child1, child2 = crossover_trees(parent1[0], parent2[0], max_depth)
        crossovered.append((child1, 0))
        crossovered.append((child2, 0))

    # Neue Individuen generieren (10% der ursprünglichen Generation)
    num_new = len(current_generation) // 10
    new_individuals = [
        (generate_random_dt(function_set, action_set, max_depth), 0)
        for _ in range(num_new)
    ]

    # Zusammenfügen der neuen Generation
    next_generation = winners + mutated + crossovered + new_individuals

    # Sicherstellen, dass die Größe der nächsten Generation gleich der aktuellen ist
    next_generation = next_generation[:len(current_generation)]

    return next_generation

# Funktion zur Mutation eines Entscheidungsbaums
def mutate_tree(tree, function_set, action_set, max_depth):
    """
    Führt eine Mutation an einem Entscheidungsbaum durch.

    :param tree: Der Entscheidungsbaum
    :param function_set: Mögliche Bedingungen für die Bäume
    :param action_set: Mögliche Aktionen für die Blätter
    :param max_depth: Maximale Tiefe für Bäume
    :return: Der mutierte Entscheidungsbaum
    """
    # Wähle einen zufälligen Knoten und mutiere ihn
    if random.random() < 0.5:
        tree.condition = random.choice(function_set)
    else:
        tree.action = random.choice(action_set)
    return tree

# Funktion zur Kreuzung von Entscheidungsbäumen
def crossover_trees(tree1, tree2, max_depth):
    """
    Führt eine Kreuzung zwischen zwei Entscheidungsbäumen durch.

    :param tree1: Erster Entscheidungsbaum
    :param tree2: Zweiter Entscheidungsbaum
    :param max_depth: Maximale Tiefe für Bäume
    :return: Zwei neue Entscheidungsbäume
    """
    subtree1 = random.choice([tree1.true_branch, tree1.false_branch])
    subtree2 = random.choice([tree2.true_branch, tree2.false_branch])

    subtree1, subtree2 = subtree2, subtree1  # Tauschen der Teilbäume

    return tree1, tree2
