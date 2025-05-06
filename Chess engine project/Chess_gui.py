import chess
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import io
from math import inf

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Chess Engine")
        
        # Initialize chess engine
        self.engine = SimpleChessEngine()
        
        # Create GUI elements
        self.create_widgets()
        
        # Variables for move selection
        self.selected_square = None
        self.highlighted_squares = []
        
        # Load piece images
        self.piece_images = self.load_piece_images()
        
        # Draw initial board
        self.update_board()
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_square_clicked)

    def load_piece_images(self):
        """Create simple piece images using Pillow"""
        pieces = {}
        colors = {"w": "white", "b": "black"}
        piece_types = {
            "p": "pawn", "n": "knight", "b": "bishop",
            "r": "rook", "q": "queen", "k": "king"
        }
        
        for color_prefix, color_name in colors.items():
            for piece_prefix, piece_name in piece_types.items():
                key = color_prefix + piece_prefix
                img = Image.new("RGBA", (45, 45), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                
                # Draw circle background
                draw.ellipse([(5, 5), (40, 40)], fill=color_name)
                
                # Draw piece letter
                text = piece_prefix.upper() if color_prefix == "w" else piece_prefix.lower()
                draw.text((15, 10), text, fill="black" if color_prefix == "w" else "white")
                
                pieces[key] = ImageTk.PhotoImage(img)
        
        return pieces

    def create_widgets(self):
        # Main frame
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Canvas for chess board
        self.canvas = Canvas(self.main_frame, width=400, height=400, bg="white")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Control panel
        self.control_frame = Frame(self.main_frame, width=150)
        self.control_frame.pack(side=RIGHT, fill=Y, padx=5, pady=5)
        
        # Game info label
        self.info_label = Label(self.control_frame, text="White's turn", font=('Arial', 12))
        self.info_label.pack(pady=10)
        
        # Reset button
        self.reset_button = Button(self.control_frame, text="New Game", command=self.reset_game)
        self.reset_button.pack(fill=X, pady=5)
        
        # Undo button
        self.undo_button = Button(self.control_frame, text="Undo Move", command=self.undo_move)
        self.undo_button.pack(fill=X, pady=5)
        
        # Move list
        self.move_list = Listbox(self.control_frame, height=20, width=20)
        self.move_list.pack(fill=BOTH, expand=True, pady=5)

    def update_board(self):
        """Draw the chess board with pieces"""
        self.canvas.delete("all")
        
        # Draw chess board
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                
                # Alternate square colors
                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#f0d9b5", outline="")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#b58863", outline="")
                
                # Draw pieces
                square = chess.square(col, 7 - row)
                piece = self.engine.board.piece_at(square)
                if piece:
                    piece_key = ("w" if piece.color == chess.WHITE else "b") + piece.symbol().lower()
                    self.canvas.create_image(x1 + 25, y1 + 25, image=self.piece_images[piece_key])
        
        # Highlight selected square and possible moves
        self.draw_highlights()
        
        # Update game status
        self.update_game_status()

    def draw_highlights(self):
        """Highlight selected square and possible moves"""
        if self.selected_square:
            col = chess.square_file(self.selected_square)
            row = 7 - chess.square_rank(self.selected_square)
            x1 = col * 50
            y1 = row * 50
            x2 = x1 + 50
            y2 = y1 + 50
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=3)
        
        for square in self.highlighted_squares:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            x1 = col * 50
            y1 = row * 50
            x2 = x1 + 50
            y2 = y1 + 50
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=2)

    def update_game_status(self):
        """Update turn indicator and game over status"""
        turn = "White" if self.engine.board.turn == chess.WHITE else "Black"
        self.info_label.config(text=f"{turn}'s turn")
        
        if self.engine.board.is_game_over():
            result = self.engine.board.result()
            self.info_label.config(text=f"Game Over: {result}")

    def on_square_clicked(self, event):
        """Handle mouse clicks on the board"""
        if self.engine.board.is_game_over():
            return
            
        # Convert click to square
        col = min(max(event.x // 50, 0), 7)
        row = min(max(event.y // 50, 0), 7)
        square = chess.square(col, 7 - row)
        
        # Human player's turn (White)
        if self.engine.board.turn == chess.WHITE:
            if self.selected_square is None:
                # Select a piece
                piece = self.engine.board.piece_at(square)
                if piece and piece.color == chess.WHITE:
                    self.selected_square = square
                    self.highlighted_squares = [
                        move.to_square 
                        for move in self.engine.board.legal_moves 
                        if move.from_square == square
                    ]
                    self.update_board()
            else:
                # Try to make a move
                move = chess.Move(self.selected_square, square)
                
                # Check for pawn promotion
                if (self.engine.board.piece_at(self.selected_square).piece_type == chess.PAWN and 
                    (chess.square_rank(square) == 7 or chess.square_rank(square) == 0)):
                    move = chess.Move(self.selected_square, square, chess.QUEEN)
                
                if move in self.engine.board.legal_moves:
                    self.make_move(move)
                    # AI makes a move
                    if not self.engine.board.is_game_over() and self.engine.board.turn == chess.BLACK:
                        self.root.after(100, self.ai_move)
                else:
                    # Select different piece or cancel
                    piece = self.engine.board.piece_at(square)
                    if piece and piece.color == chess.WHITE:
                        self.selected_square = square
                        self.highlighted_squares = [
                            move.to_square 
                            for move in self.engine.board.legal_moves 
                            if move.from_square == square
                        ]
                    else:
                        self.selected_square = None
                        self.highlighted_squares = []
                    self.update_board()

    def make_move(self, move):
        """Execute a move and update the display"""
        self.engine.board.push(move)
        self.add_move_to_list(move)
        self.selected_square = None
        self.highlighted_squares = []
        self.update_board()

    def ai_move(self):
        """AI makes a move"""
        ai_move = self.engine.find_best_move(depth=3)
        if ai_move:
            self.make_move(ai_move)

    def add_move_to_list(self, move):
        """Add move to the move history list"""
        move_number = len(self.engine.board.move_stack)
        if move_number % 2 == 1:
            # White's move
            self.move_list.insert(END, f"{move_number//2 + 1}. {move.uci()}")
        else:
            # Black's move
            last_item = self.move_list.get(END)
            self.move_list.delete(END)
            self.move_list.insert(END, f"{last_item}  {move.uci()}")
        self.move_list.see(END)

    def reset_game(self):
        """Start a new game"""
        self.engine.reset_board()
        self.selected_square = None
        self.highlighted_squares = []
        self.move_list.delete(0, END)
        self.update_board()

    def undo_move(self):
        """Undo the last move"""
        if len(self.engine.board.move_stack) > 0:
            self.engine.board.pop()
            self.move_list.delete(END)
            self.selected_square = None
            self.highlighted_squares = []
            self.update_board()


class SimpleChessEngine:
    def __init__(self):
        self.board = chess.Board()
        
    def reset_board(self):
        self.board.reset()
        
    def find_best_move(self, depth):
        best_move = None
        best_value = -inf
        alpha = -inf
        beta = inf
        
        for move in self.board.legal_moves:
            self.board.push(move)
            move_value = self.negamax(depth-1, -beta, -alpha, False)
            self.board.pop()
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
                
            alpha = max(alpha, move_value)
        
        return best_move
    
    def negamax(self, depth, alpha, beta, is_maximizing):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()
        
        max_value = -inf
        for move in self.board.legal_moves:
            self.board.push(move)
            value = -self.negamax(depth-1, -beta, -alpha, not is_maximizing)
            self.board.pop()
            
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            
            if alpha >= beta:
                break  # Beta cutoff
                
        return max_value
    
    def evaluate_board(self):
        if self.board.is_checkmate():
            if self.board.turn:  # Black just delivered checkmate
                return -9999
            else:  # White just delivered checkmate
                return 9999
                
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves():
            return 0
            
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value
        
        # Add some positional evaluation
        if self.board.turn == chess.WHITE:
            score += self.evaluate_position()
        else:
            score -= self.evaluate_position()
            
        return score
    
    def evaluate_position(self):
        score = 0
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                # Reward center control
                if square in center_squares:
                    if piece.color == chess.WHITE:
                        score += 10
                    else:
                        score -= 10
                
                # Reward mobility
                if piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
                    mobility = len(list(self.board.legal_moves))
                    if piece.color == chess.WHITE:
                        score += mobility * 0.1
                    else:
                        score -= mobility * 0.1
        
        return score


if __name__ == "__main__":
    root = Tk()
    gui = ChessGUI(root)
    root.mainloop()