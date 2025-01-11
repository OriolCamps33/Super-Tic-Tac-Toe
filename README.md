
# Super Tic-Tac-Toe with MCTS

## Overview
Super Tic-Tac-Toe is a strategic variant of traditional Tic-Tac-Toe. This project implements the game mechanics and an AI opponent using Monte Carlo Tree Search (MCTS). Players can face off against the AI or another human player in an interactive graphical interface.

## Features
- **Game Mechanics**:
  - Supports the Super Tic-Tac-Toe rules, including local board constraints for the next move.
  - Detects winners and draws automatically.
- **Artificial Intelligence**:
  - AI uses Monte Carlo Tree Search (MCTS) to calculate optimal moves.
  - Configurable depth of MCTS iterations for balancing performance and difficulty.
- **Graphical Interface**:
  - Built with `Tkinter`, providing an intuitive and interactive game experience.
  - Highlights available moves and enforces valid board rules.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/super-tic-tac-toe.git
   ```
2. Navigate to the project directory:
   ```bash
   cd super-tic-tac-toe
   ```
3. Ensure you have Python 3.8 or higher installed.
4. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the graphical interface:
   ```bash
   python sttt_GUI.py
   ```
2. Play as the `X` player against the AI (`O`) or another human player.
3. Follow the on-screen instructions for making moves.

## Rules
1. The game consists of 9 smaller 3x3 boards arranged into a larger 3x3 grid.
2. Players alternate turns, placing their mark (`X` or `O`) on one of the cells in the smaller boards.
3. The next move is restricted to the small board corresponding to the cell chosen in the previous move.
4. A player wins a small board by forming a line (horizontal, vertical, or diagonal).
5. A player wins the game by winning 3 small boards in a row on the larger board.
6. The game ends in a draw if all boards are full without a winner.

## Project Structure
- **MCTS_sttt.py**: Implements the Monte Carlo Tree Search algorithm and core game logic.
- **sttt_GUI.py**: Contains the graphical interface for the game using Tkinter.

## Customization
- Modify the number of MCTS iterations in `sttt_GUI.py` to adjust the difficulty:
  ```python
  self.mcts(iterations=1000)  # Change 1000 to a higher or lower value
  ```

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

## Acknowledgments
- The MCTS algorithm and its integration into board games were inspired by open-source projects and research papers on AI for games.

## Contact
For questions or feedback, feel free to contact the author via GitHub or open an issue in this repository.
