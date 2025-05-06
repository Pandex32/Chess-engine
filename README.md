# Chess Engine with GUI

## Description
A Python chess engine with graphical interface that allows you to play against an AI opponent. The engine features:
- Complete chess rules implementation
- AI with adjustable difficulty
- Move history tracking
- Undo functionality
- Simple graphical interface

## Features
- Play against computer AI
- Visual board with piece movement
- Move list showing game history
- New game and undo move functionality
- Game over detection (checkmate, stalemate, etc.)

## Installation

### Requirements
- Python 3.6+
- Required packages: `python-chess`, `Pillow`

### Installation Steps
1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install python-chess pillow
   ```

## How to Run
Execute the program with:
```bash
python chess_gui.py
```

## How to Play
1. **White (Human) moves first**
   - Click on a white piece to select it (will highlight yellow)
   - Possible moves will be highlighted in blue
   - Click on a destination square to move

2. **Black (AI) moves automatically** after your move

3. **Special moves**:
   - Pawns automatically promote to queens
   - Castling is supported
   - En passant is supported

4. **Controls**:
   - "New Game" button to restart
   - "Undo Move" button to take back last move

## AI Difficulty
The AI difficulty can be adjusted by changing the `depth` parameter in the `find_best_move()` method (line ~350). Higher values make the AI stronger but slower.

## Troubleshooting
If you encounter any issues:
1. Ensure all dependencies are installed:
   ```bash
   pip install python-chess pillow
   ```
2. If you get display issues, try running on a different Python version

## Future Improvements
- Add difficulty levels
- Implement a clock/timer
- Add opening book support
- Improve piece graphics
- Add save/load game functionality

