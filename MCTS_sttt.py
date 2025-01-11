
import random
from tkinter import NO
import numpy

class Node:
    def __init__(self, state, parent=None):
        self.state = state  # Estado del juego
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.untried_actions = self.get_legal_actions()

    def get_legal_actions(self):
        # Devuelve una lista de movimientos legales desde el estado actual
        if self.state['winner'] or self.state['draw']:
            return []  # No hay movimientos legales si el juego terminó

        legal_actions = []
        if self.state['next_tablero'] is not None:
            # Restricción: movimientos en el tablero activo
            tablero_index = self.state['next_tablero']
            if self.state['sub_tablero'][tablero_index] == ' ':  # Tablero disponible
                for r in range(3):
                    for c in range(3):
                        if self.state['tablero'][tablero_index][r][c] == ' ':
                            legal_actions.append((tablero_index, r, c))
        else:
            # Si no hay un tablero específico (por ejemplo, el destino está resuelto),
            # permitir movimientos en cualquier tablero disponible
            for i in range(9):
                if self.state['sub_tablero'][i] == ' ':  # Tablero disponible
                    for r in range(3):
                        for c in range(3):
                            if self.state['tablero'][i][r][c] == ' ':
                                legal_actions.append((i, r, c))

        return legal_actions


    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, exploration_weight=1.41):
        return max(
            self.children,
            key=lambda child: child.value / (child.visits + 1e-6) + exploration_weight * (2 * numpy.log(self.visits + 1) / (child.visits + 1e-6)) ** 0.5
        )

    def expand(self):
        action = self.untried_actions.pop()
        new_state = self.simulate_action(action)
        child_node = Node(new_state, parent=self)
        self.children.append(child_node)
        return child_node

    def simulate_action(self, action):
        # Copia el estado actual y aplica la acción
        new_state = {
            'tablero': [
                [row.copy() for row in tablero] for tablero in self.state['tablero']
            ],
            'sub_tablero': self.state['sub_tablero'][:],
            'current_player': self.state['current_player'],
            'next_tablero': self.state['next_tablero'],
            'winner': self.state['winner'],
            'draw': self.state['draw']
        }
        tablero_index, row, col = action
        new_state['tablero'][tablero_index][row][col] = self.state['current_player']

        # Actualizar el sub-tablero
        game = SuperTicTacToe()
        game.tablero = new_state['tablero']
        game.sub_tablero = new_state['sub_tablero']
        game.update_sub_tablero()

        new_state['sub_tablero'] = game.sub_tablero
        new_state['winner'] = game.check_winner(new_state['sub_tablero'])
        new_state['draw'] = game.is_draw(new_state['sub_tablero'])
        new_state['current_player'] = 'O' if self.state['current_player'] == 'X' else 'X'

        if new_state['sub_tablero'][row * 3 + col] != ' ':
            new_state['next_tablero'] = None  # Elige cualquier tablero
        else:
            new_state['next_tablero'] = row * 3 + col

        return new_state

    def backpropagate(self, result):
        self.visits += 1
        self.value += result
        if self.parent:
            self.parent.backpropagate(-result)

    def simulate(self):
        # Simula una partida completa desde el estado actual
        new_node = Node(self.state, self)
        while not new_node.state['winner'] and not new_node.state['draw']:
            legal_actions = new_node.get_legal_actions()
            if not legal_actions:
                break
            action = random.choice(legal_actions)
            new_state = new_node.simulate_action(action)
            new_node = Node(new_state, new_node)

        if new_node.state['winner'] != None:
            return 1 if new_node.state['current_player'] == 'O' else -1
        return 0
    
class SuperTicTacToe:
    def __init__(self):
        self.tablero = [[[' ' for _ in range(3)] for _ in range(3)] for _ in range(9)]
        self.sub_tablero = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.next_tablero = None
        self.prev_action = None
        self.ancho = 40

    def check_winner(self, tablero):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for condition in win_conditions:
            if tablero[condition[0]] == tablero[condition[1]] == tablero[condition[2]] != ' ':
                return tablero[condition[0]]
        return None

    def is_draw(self, tablero):
        return all(cell != ' ' for cell in tablero)

    def update_sub_tablero(self):
        for i in range(9):
            flat_tablero = [cell for row in self.tablero[i] for cell in row]
            winner = self.check_winner(flat_tablero)
            if winner:
                self.sub_tablero[i] = winner
            elif self.is_draw(flat_tablero):
                self.sub_tablero[i] = 'D'

    def mcts(self, iterations=1000):
        root = Node({
            'tablero': self.tablero,
            'sub_tablero': self.sub_tablero,
            'current_player': self.current_player,
            'next_tablero': self.next_tablero,
            'winner': None,
            'draw': False
        })
        for _ in range(iterations):
            node = root

            # Selección
            while node.is_fully_expanded() and node.children:
                node = node.best_child()

            # Expansión
            if not node.is_fully_expanded():
                node = node.expand()

            # Simulación
            result = node.simulate()

            # Retropropagación
            node.backpropagate(result)

        return root.best_child(exploration_weight=0).state


    def play_turn(self, tablero_index, row, col, out):
        if self.sub_tablero[tablero_index] != ' ':  # Tablero ya ganado o empatado
            if out: print("Este tablero ya está resuelto. Elige otro movimiento.")
            return False

        if self.tablero[tablero_index][row][col] != ' ':  # Casilla ocupada
            if out: print("Casilla ocupada. Elige otra.")
            return False
        
        if tablero_index != self.next_tablero and self.next_tablero != None:
            if out: print("No puedes jugar en este tablero, el tablero és: ", self.next_tablero)
            return False

        self.tablero[tablero_index][row][col] = self.current_player
        self.update_sub_tablero()

        # Revisar si hay un ganador global
        sub_winner = self.check_winner(self.sub_tablero)
        if sub_winner:
            if out: print(f"\n¡El jugador {sub_winner} ha ganado el juego!")
            return True

        if self.is_draw(self.sub_tablero):
            if out: print("\n¡El juego terminó en empate!")
            return True

        # Actualizar el tablero al que debe ir el siguiente jugador
        self.next_tablero = row * 3 + col
        if self.sub_tablero[self.next_tablero] != ' ':  # Si el siguiente tablero está resuelto, el jugador elige
            self.next_tablero = None

        # Cambiar el turno
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return False
    
    def print_tablero(self):
        print("\nSuper Tic-Tac-Toe tablero:")
        print("-" * self.ancho)
        for i in range(3):  # Filas de tableros
            for j in range(3):  # Filas dentro de cada tablero
                row = [" | ".join(self.tablero[i * 3 + k][j]) for k in range(3)]  # Formatea las filas de 3 tableros
                print("| " + " || ".join(row) + " |")
            if i < 2:  # Línea divisoria entre bloques de 3 tableros
                print("-" * self.ancho)
        print("-" * self.ancho)
    
    def play_against_mcts(self, iterations=1000):
        print("\n¡Bienvenido a Super Tic-Tac-Toe contra MCTS!")
        while True:
            self.print_tablero()
            if self.current_player == 'X':  # Turno del jugador humano
                print(f"\nTurno del jugador {self.current_player}")
                if self.next_tablero is None:
                    tablero_index = int(input("Elige un tablero (0-8): "))
                else:
                    tablero_index = self.next_tablero
                    print(f"Debes jugar en el tablero {tablero_index}")

                row = int(input("Elige la fila (0-2): "))
                col = int(input("Elige la columna (0-2): "))

                if not self.play_turn(tablero_index, row, col, True):
                    print("Movimiento inválido. Intenta de nuevo.")
                    continue
            else:  # Turno de la IA (MCTS)
                print("\nTurno de la IA MCTS...")
                best_state = self.mcts(iterations)
                for i in range(9):
                    for r in range(3):
                        for c in range(3):
                            if self.tablero[i][r][c] != best_state['tablero'][i][r][c]:
                                tablero_index, row, col = i, r, c
                self.play_turn(tablero_index, row, col, True)

            # Verificar si hay un ganador o empate global
            global_winner = self.check_winner(self.sub_tablero)
            if global_winner:
                self.print_tablero()
                print(f"\n¡El jugador {global_winner} ha ganado el juego!")
                break
            elif self.is_draw(self.sub_tablero):
                self.print_tablero()
                print("\n¡El juego terminó en empate!")
                break

if __name__ == "__main__":
    game = SuperTicTacToe()
    game.play_against_mcts(iterations=1000)  # Puedes ajustar el número de iteraciones de MCTS