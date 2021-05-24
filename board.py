from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board():

    def __init__(self):

        self.white_pieces = []
        self.black_pieces = []

        self.game_board = self.generate_default_board()

        



    def generate_default_board(self):
        '''
        Generates a board with default piece positions, instantiating necessary piece objects.
        '''
        board = []
        for i in range(8):
            board.append([None] * 8)

        board[0] = [Rook((0, 0)), Knight((0, 1)), Bishop((0, 2)), Queen((0, 3)),
        King((0, 4)), Bishop((0, 5)), Knight((0, 6)), Rook((0, 7))]

        board[7] = [Rook((7, 0)), Knight((7, 1)), Bishop((7, 2)), Queen((7, 3)),
        King((7, 4)), Bishop((7, 5)), Knight((7, 6)), Rook((7, 7))]

        for i in [1, 6]:
            for j in range(8):
                board[i][j] = Pawn((i, j))
        

        board = self.assign_colors(board)

        return board

    
    def assign_colors(self, board):
        '''
        Assigns color to each piece so it is known who each piece belongs to.
        '''

        for i in [0, 1]:
            for j in range(8):
                board[i][j].color = 'Black'
                self.black_pieces.append(board[i][j])

        for i in [6, 7]:
            for j in range(8):
                board[i][j].color = 'White'
                self.white_pieces.append(board[i][j])

        return board

            




