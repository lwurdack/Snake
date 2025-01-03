import random
import matplotlib.pyplot as plt
import networkx as nx

# Erzeuge Knoten im Entscheidungsbaum
class DecisionTreeNode:

    # Initilaisierung eines Kontens, jeder Knoten hat entweder eine Bedingung oder eine Aktion
    def __init__(self, condition=None, action=None):
        self.condition = condition  # Bedingung z.b. food_front
        self.action = action  # Aktion z.b. move_left
        self.true_branch = None  # Verweis auf nächsten Knoten abhängig von Ergebnis der Bedingung
        self.false_branch = None  

    # Prüfe ob Knoten ein Terminal ist
    def is_leaf(self):
        return self.action is not None
    
    # Durchlauf des Entscheidungsbaums , am ende Aktion wiederzugeben (Rekursiver Prozess)
    def return_action(self, variables):
        """

        Gibt wieder die passende Aktion zu basierend auf den Variablen

        :param variables: Wörterbuch von Zustand der Bedingungen (True/False)
        
        return: Aktion als string

        """

        # Wenn Knoten ein Terminal ist, dann gebe Aktion wieder
        if self.is_leaf():
            return self.action

        # Falls Knoten Bedingung hat, dann überprüfen ob diese True oder False ist und denn Zweig folgen zum nächsten Knoten
        if variables.get(self.condition, False):

            # Wenn die Bedinung wahr ist, ruft die Methode return_action erneut auf und Prüfe nächsten Knoten
            return self.true_branch.return_action(variables)
        else:
            return self.false_branch.return_action(variables)
        
    def __str__(self, level=0):
        """

        Rekursive Darstellung des Entscheidungsbaums

        """
        indent = "  " * level  # Einrückung für lesbare Baumstruktur
        if self.is_leaf():
            return f"{indent}Leaf(Action: {self.action})\n"
        result = f"{indent}Node(Condition: {self.condition})\n"
        if self.true_branch:
            result += self.true_branch.__str__(level + 1)  # Rekursion für true_branch
        if self.false_branch:
            result += self.false_branch.__str__(level + 1)  # Rekursion für false_branch
        return result


# erstelle zufälligen Entscheidungsbaum
def generate_random_dt(function_set, action_set, max_depth=6, current_depth=1, stop_probability=0.2, full_method=False):
    """
    Generiere einen zufälligen Entscheidungsbaum mit der Option für Full- oder Grow-Methode.
    Die Grow-Methode generiert mindestens eine Bedingung vor einem Terminal.

    :param function_set: Liste von Konditionen.
    :param action_set: Liste von Aktionen.
    :param max_depth: Maximale Tiefe der Bäume.
    :param current_depth: Aktuelle Tiefe während der Rekursiven Erstellung des Baums.
    :param stop_probability: Wahrscheinlichkeit für Grow-Methode, dass der Baumwachstum stoppt.
    :param full_method: Wenn True, wird die Full-Methode genutzt (kein frühzeitiges Stoppen).
    :return: Ein zufälliger Knoten des Entscheidungsbaums.
    """
    if full_method:
        # Full-Methode: Stoppe nur, wenn die maximale Tiefe erreicht ist
        if current_depth > max_depth:
            return DecisionTreeNode(action=random.choice(action_set))
    else:
        # Grow-Methode: Wenn Tiefe 1, generiere mindestens eine Bedingung
        if current_depth > max_depth or (current_depth > 1 and random.random() < stop_probability):
            return DecisionTreeNode(action=random.choice(action_set))

    # Generiere einen Knoten mit einer Bedingung
    condition = random.choice(function_set)
    node = DecisionTreeNode(condition=condition)

    # Erstelle rekursiv Zweige
    node.true_branch = generate_random_dt(function_set, action_set, max_depth, current_depth + 1, stop_probability, full_method)
    node.false_branch = generate_random_dt(function_set, action_set, max_depth, current_depth + 1, stop_probability, full_method)

    return node



def visualize_decision_tree(node):
    """
    Visualize the decision tree using NetworkX and Matplotlib, structured as a tree.

    :param node: The root node of the decision tree.
    """
    def add_edges(graph, node, parent_id=None, is_true_branch=None, depth=0):
        if node is None:
            return

        node_id = id(node)
        label = node.action if node.is_leaf() else node.condition
        graph.add_node(node_id, label=label, depth=depth)

        if parent_id is not None:
            edge_label = "True" if is_true_branch else "False"
            graph.add_edge(parent_id, node_id, label=edge_label)

        if not node.is_leaf():
            add_edges(graph, node.true_branch, node_id, is_true_branch=True, depth=depth + 1)
            add_edges(graph, node.false_branch, node_id, is_true_branch=False, depth=depth + 1)


    graph = nx.DiGraph()
    add_edges(graph, node)

    # Use a hierarchical layout to represent the tree structure
    pos = nx.multipartite_layout(graph, subset_key="depth")
    labels = nx.get_node_attributes(graph, 'label')
    edge_labels = nx.get_edge_attributes(graph, 'label')

    plt.figure(figsize=(16, 12))  # Increase figure size for better visualization
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=4000, node_color="lightblue", font_size=12, font_weight="bold")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)
    plt.title("Decision Tree Visualization", fontsize=16)
    #plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.show()
