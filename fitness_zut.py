

def calculate_fitness(score, iterations, score_weight=1.0, time_weight=0.05, interation_weight=0.5):
    """
    Berechnet die Fitness des Spiels basierend auf Score und Überlebenszeit.

    :param score: Die aktuelle Punktzahl des Spiels
    :param iterations: Die Anzahl der Iterationen (Überlebenszeit)
    :param score_weight: Gewichtung für die Punktzahl
    :param time_weight: Gewichtung für die Überlebenszeit
    :param interation_weight: Gewichtung für Punktzahl * Überlebenszeit 
    :return: Fitness-Wert als float
    """
    return score_weight * score + time_weight * iterations + interation_weight * iterations * score
