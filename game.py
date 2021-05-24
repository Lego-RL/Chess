from board import Board
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Game():

    def __init__(self):

        self.board = Board()
        self.turn = 'White'

        self.assign_moves()


    def print_board_to_console(self):
        '''
        Prints the game board to the console.
        '''
        
        empty = '-'

        for row in self.board.game_board:
            for i in range(8):

                if row[i] is None:
                    print(f'{empty:^10}', end='')

                else:
                    print(f'{row[i].title:^10}', end='')

            print() #get a newline at the end of each row


    def validate_move(self, x, y):
        '''
        See if a move is a valid spot on the board, and if the space is empty.
        '''

        if x < 0 or x > 7:
            return False
        
        if y < 0 or y > 7:
            return False

        #TODO: check if piece is already in spot
        #TODO: check if there is a piece in the way blocking this move

        


    def assign_moves(self):
        '''
        Assign possible moves to each piece on the board.
        '''

        for piece in self.board.white_pieces:

            if isinstance(piece, Pawn):
                # piece.print_position()

                if True:
                    pass
                    #TODO: check for valid pawn moves making use of validate_move()

            #TODO: check for valid moves for all other pieces




game = Game()
game.print_board_to_console()

