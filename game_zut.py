import random

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
MOVES = [UP, DOWN, LEFT, RIGHT]

class snake:
    def __init__(self, size):
        self.size = size # Größe Spielfeld muss noch außerhalb definiert werden
        self.snake = [(size // 2, size // 2 - i) for i in range(3)] # das ist die Schlange, die dem Spiel am Anfang mitgegebne wird mit Länge 3
        self.food = self.generate_food()
        self.direction = LEFT # das ist die Anfangsrichtung in der die Schalnge sich zu Beginn bewegt, hierbei lege ich auf Default RIGHT fest, aber Grundsätzlich kann aus MOVES eine Richtung gezogen werden
        self.end = False # das Spiel ist zu Beginn auf nicht Endend gesetzt
        self.score = 0 # der Score ist am Anfang des Spieles bei 0
        self.steps_without_food = 0 # die Schritte ohne Essen gegessen zu haben ist am Anfang 0
        self.repeat_count = 0  # Zähler für wiederholte Zyklen
        self.head_positions = []  # Liste der Kopfpositionen
        self.max_history = 200  # Maximale Länge der Historie
        

    #Funktion, die immer neues Essen spanen lässt
    def generate_food(self):
        # Create an independent RNG with a fixed seed
        food_rng = random.Random(42)  # Fixed seed for deterministic food generation

        while True:
            # Use the independent RNG for generating food position
            food_position = (
                food_rng.randint(0, self.size - 1),
                food_rng.randint(0, self.size - 1)
            )

            # Ensure the food does not spawn on the snake
            if food_position not in self.snake:
                #print(food_position)
                return food_position


    # definiere die Bewegungsfunktion der Schlaneg
    def move(self, direction):
        """
        Bewegungsfunktion der Schlange 

        :param self:  
        :param direction: 
    
        """

        # Überprüfung ob Game beendet wurde
        if self.end:
            #print("Game already ended. No move possible.")
            return
        
        # nun muss die Bewegung implementiert werden
        # definiere zunächst den Kopf der Schlange als das letzte Element der Liste von der Schlange
        head_x, head_y = self.snake[-1]

        # der neue Kopf wird errechnet anhand der Bewegungsrichtung die aktuell gegeben ist
        # Rechne das letzte Element der Liste plus die Bewegungsrichtung
        new_head = (head_x + direction[0], head_y + direction[1])

        #check ob der neue Kopf in die Wand oder eigenen Körper gecrasht ist
        if (new_head[0] < 0 or new_head[1] < 0 or 
            new_head[0] >= self.size or new_head[1] >= self.size):
            self.end = True 
            #print(f"Collision with wall at {new_head}")
            return
        
        if new_head in self.snake:
            self.end = True 
            #print(f"Collision with self at {new_head}")
            return

        
        # wenn Schlange nicht gecrasht ist, dann füge neuen Kopf zur Liste hinzu
        self.snake.append(new_head)

        # Beachten ob Bewegung in Essen oder leeres Feld
        # Schlange bewegt sich in Essen, dann neues Essen spanen lassen
        if new_head == self.food:
            # rufe Funktion für Essen generieren auf
            self.food = self.generate_food()

            # Score muss auch hier erhöht werden
            self.score += 1

            # Anzahl Schritte ohne das gegessen wird muss jetzt wieder auf 0 gesetzt werden
            self.steps_without_food = 0

        # Schlange bewegt sich in ein leeres Feld voran
        else:
            self.snake.pop(0) 

        # Kopfposition aktualisieren
        self.head_positions.append(list(new_head))
        if len(self.head_positions) > self.max_history:
            self.head_positions.pop(0)

        # Zyklusprüfung
        if self.has_repeating_cycle():
            self.repeat_count += 1
            #print(f"Cycle detected. Repeat count: {self.repeat_count}")
            if self.repeat_count >= 3:
                self.end = True
                #print("Snake repeated the same cycle 3 times. Game Over!")
        else:
            self.repeat_count = 0  # Zähler zurücksetzen
            #print("No cycle detected. Repeat count reset.")

    def has_repeating_cycle(self):
        """Prüft, ob die Kopfpositionen zyklisch wiederholt werden."""
        length = len(self.head_positions)

        # Prüfen auf Zyklen in der Liste der Kopfpositionen
        for cycle_length in range(2, length // 2 + 1):
            if self.head_positions[-cycle_length:] == self.head_positions[-2 * cycle_length : -cycle_length]:
                #print(f"Repeating cycle detected: {self.head_positions[-cycle_length:]}")
                return True
        return False
    
    # Funktion um die Umgebung abzufragen links, rechts und vor dem Kopf
    def state(self):
        # Kopf der Schlange
        head_x, head_y = self.snake[-1]

        # Richtungskoordinaten für "vor", "links" und "rechts"
        offsets = {
                "front": self.direction,
                "left": (-self.direction[1], self.direction[0]),    # 90° nach links
                "right": (self.direction[1], -self.direction[0])    # 90° nach rechts
                }

        # check für jede richtungskoordinate, waas genau im Umfeld liegt
        def check_field(offset):
            x, y = head_x + offset[0], head_y + offset[1]
            if x < 0 or x >= self.size or y < 0 or y >= self.size:
                return "obstacle"
            if (x, y) in self.snake:
                return "obstacle"
            if (x, y) == self.food:
                return "food"
            return "empty"

        # erstelle Wörterbuch für die Abfrage der Umgebung
        results = {}
        # für pos (front, left und right) sowie dem offset (Richtungskoordinate) soll die function check_field durchgeführt werden und die Ergebnisse in results gespeichert werden
        for pos, offset in offsets.items():
            results[pos] = check_field(offset)
        return results
    
    def game_iteration(self, direction):
        self.move(direction)
        return self.state()






