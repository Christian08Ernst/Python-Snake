import tkinter as tk
import random

# Wichtige Einstellungen
GAME_WIDTH = 700  # Breite des Spielfelds
GAME_HEIGHT = 700  # Höhe des Spielfelds
SPACE_SIZE = 50  # Größe jedes "Kästchens" auf dem Spielfeld
BODY_PARTS = 3  # Startlänge der Schlange
SNAKE_COLOR = "#8B0000"  # Farbe der Schlange (Dunkelrot)
FOOD_COLOR = "#0000FF"  # Farbe des Futters (Blau)
BACKGROUND_COLOR = "#808080"  # Hintergrundfarbe des Spielfelds (Grau)

# Globale Variablen
direction = "down"  # Anfangsrichtung der Schlange
speed = 100  # Anfangsgeschwindigkeit

# Klassen
class Snake:
    def __init__(self, canvas):
        # Initialisiert die Schlange mit einer bestimmten Länge und Farbe
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Erzeugt die Startpositionen der Schlangenteile
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Zeichnet die Schlangenteile auf das Canvas und speichert sie in `squares`
        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        # Initialisiert das Futter auf dem Spielfeld
        self.canvas = canvas
        self.create_food()  # Erstellt das Futter an einer zufälligen Position

    def create_food(self):
        # Generiert zufällige Koordinaten für das Futter
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Hauptspiellogik
def next_turn(snake, food):
    global direction, speed

    # Aktuelle Position des Schlangenkopfs
    x, y = snake.coordinates[0]

    # Aktualisiert die Richtung der Schlange
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Fügt ein neues Segment an den Kopf der Schlange hinzu
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Prüft, ob die Schlange das Futter erreicht hat
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1  # Erhöht den Punktestand
        label.config(text="Score: {}".format(score))  # Aktualisiert das Punktelabel
        canvas.delete("food")  # Entfernt das alte Futter
        food = Food(canvas)  # Erstellt neues Futter

        # Erhöht die Geschwindigkeit der Schlange (mindestens bis zu einem bestimmten Limit)
        if speed > 20:  # Mindestgeschwindigkeit festlegen
            speed -= 5  # Erhöht die Geschwindigkeit, indem das Intervall verringert wird

    else:
        # Entfernt das letzte Segment, falls kein Futter gegessen wurde (Schlange bleibt gleich lang)
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Überprüft, ob die Schlange mit sich selbst oder den Spielfeldgrenzen kollidiert ist
    if check_collisions(snake):
        game_over()  # Beendet das Spiel, falls eine Kollision vorliegt
    else:
        # Setzt den nächsten Zug nach `speed` Millisekunden fort
        window.after(speed, next_turn, snake, food)

# Richtungsänderung der Schlange, um z.B. Richtungswechsel nach links und rechts zu verhindern
def change_direction(new_direction):
    global direction
    # Stellt sicher, dass die Schlange nicht in die entgegengesetzte Richtung wechselt
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# Prüft, ob die Schlange sich selbst oder den Rand getroffen hat
def check_collisions(snake):
    x, y = snake.coordinates[0]  # Position des Schlangenkopfs
    # Prüft, ob der Kopf die Spielfeldgrenzen überschreitet
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    # Prüft, ob der Kopf der Schlange mit ihrem Körper zusammenstößt
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
    return False

# Zeigt eine "GAME OVER"-Nachricht an und löscht das Spielfeld
def game_over():
    canvas.delete("all")  # Löscht alle Elemente auf dem Canvas
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="GAME OVER", font=('consolas', 50), fill="red")

# Fenster erstellen
window = tk.Tk()  # Hauptfenster für das Spiel
window.title("Snake Game")  # Titel des Fensters
window.resizable(False, False)  # Fenstergröße nicht veränderbar

# Canvas für das Spielfeld erstellen
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Punktestand-Label erstellen und initialisieren
score = 0
label = tk.Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

# Fenster zentrieren
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Tastaturereignisse für die Steuerung der Schlange binden
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Schlange und Futter initialisieren
snake = Snake(canvas)
food = Food(canvas)

# Starte das Spiel mit dem ersten Aufruf von `next_turn`
window.after(speed, next_turn, snake, food)

# Haupt-Ereignisschleife starten
window.mainloop()
