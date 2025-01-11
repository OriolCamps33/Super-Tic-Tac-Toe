import tkinter as tk
from tkinter import messagebox
import threading
from MCTS_sttt import SuperTicTacToe

class SuperTicTacToeGUI(SuperTicTacToe):
    def __init__(self, iterations):
        super().__init__()
        self.root = tk.Tk()
        self.iterations = iterations
        self.root.title("Super Tic-Tac-Toe")
        self.buttons = [[tk.Button() for _ in range(9)] for _ in range(9)]  # Botones para las celdas
        self.create_board()

    def create_board(self):
        # Crear una cuadrícula 3x3 de tableros
        for board_row in range(3):
            for board_col in range(3):
                frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=2)
                frame.grid(row=board_row, column=board_col, padx=5, pady=5)

                # Crear una cuadrícula 3x3 de botones dentro de cada tablero
                board_index = board_row * 3 + board_col
                for cell_row in range(3):
                    for cell_col in range(3):
                        button = tk.Button(
                            frame,
                            text=" ",
                            font=("Arial", 14),
                            height=2,
                            width=5,
                            command=lambda br=board_index, cr=cell_row, cc=cell_col: self.on_click(br, cr, cc)
                        )
                        button.grid(row=cell_row, column=cell_col)

                        self.buttons[board_index][cell_row * 3 + cell_col] = button

    def play_ai(self):
        # Ejecutar MCTS en un hilo separado
        def ai_move():
            best_state = self.mcts(iterations=self.iterations)
            for i in range(9):
                for r in range(3):
                    for c in range(3):
                        if self.tablero[i][r][c] != best_state['tablero'][i][r][c]:
                            self.play_turn(i, r, c, False)
                            break
            self.update_buttons()

        threading.Thread(target=ai_move).start()    

    def update_buttons(self):
        # Actualizar botones según el estado actual del tablero
        for board_index in range(9):
            for cell_index in range(9):
                row, col = divmod(cell_index, 3)
                text = self.tablero[board_index][row][col]
                button = self.buttons[board_index][cell_index]
                button.config(text=text)

                # Deshabilitar botones ocupados
                if text != " ":
                    button.config(state=tk.DISABLED)
                else:
                    # Habilitar solo botones en el tablero correcto o en cualquier tablero si es necesario
                    if self.next_tablero is None or self.next_tablero == board_index:
                        button.config(state=tk.NORMAL)
                    else:
                        button.config(state=tk.DISABLED)

    def on_click(self, board_index, row, col):
        # Manejar el clic del jugador humano
        if self.current_player == 'X':  # Turno del jugador humano
            if self.next_tablero is not None and board_index != self.next_tablero:
                messagebox.showinfo("Movimiento inválido", f"Debes jugar en el tablero {self.next_tablero}.")
                return
            if self.play_turn(board_index, row, col, True):
                self.update_buttons()
                return
            self.update_buttons()
            # Turno de la IA
            self.root.after(500, self.play_ai)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = SuperTicTacToeGUI(5000)
    game.run()