import random
from decision_tree_zut import generate_random_dt, DecisionTreeNode
from fitness_zut import calculate_fitness  # Fitness-Berechnung importiert
import copy


# Funktion zur Erstellung der nächsten Generation basierend auf Vergleich, Mutation und Crossover
def create_next_generation(winners, function_set, action_set, max_depth=6):
    total = len(winners) * 2

    # 2/5 of winners for mutation
    num_mutations = int(total * (2 / 10))
    mutated = [
        (mutate_tree(copy.deepcopy(random.choice(winners)[0]), function_set, action_set, max_depth), 0)
        for _ in range(num_mutations)
    ]

    # 2/5 of winners for crossover
    num_crossover = int(total * (2 / 10))
    crossovered = []
    for _ in range(num_crossover // 2):
        parent1, parent2 = random.sample(winners, 2)
        child1, child2 = crossover_trees(
            copy.deepcopy(parent1[0]), copy.deepcopy(parent2[0]), max_depth
        )
        crossovered.append((child1, 0))
        crossovered.append((child2, 0))

    # Generate new individuals (10% of original population)
    num_new = int(total * (1 / 10))
    new_individuals = [
        (generate_random_dt(function_set, action_set, max_depth), 0)
        for _ in range(num_new)
    ]

    #print(len(winners), len(mutated), len(crossovered), len(new_individuals))
    # Combine all individuals
    next_generation = winners + mutated + crossovered + new_individuals

    return next_generation

def mutate_tree(tree, function_set, action_set, max_depth):
    """
    Performs a mutation on a copy of a decision tree.
    """
    if random.random() < 0.5:
        tree.condition = random.choice(function_set)
    else:
        tree.action = random.choice(action_set)
    return tree

def crossover_trees(tree1, tree2, max_depth):
    """
    Performs a crossover between two copies of decision trees.
    """
    subtree1 = random.choice([tree1.true_branch, tree1.false_branch])
    subtree2 = random.choice([tree2.true_branch, tree2.false_branch])

    # Swap the subtrees
    subtree1, subtree2 = subtree2, subtree1

    return tree1, tree2
