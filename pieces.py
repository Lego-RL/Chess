
from abc import ABC, abstractmethod
# from board import Board
# import board

class Piece(ABC):

    def __init__(self, position, color=None):
        
        self.position = position
        self.row = position[0]
        self.column = position[1]

        self.color = color

        super().__init__()



    def print_position(self):
        print(f'{self.title} located @ ({self.row}, {self.column})')


    def position_str(self):
        return f'{self.title} located @ ({self.row}, {self.column})'


    def validate_move(self, row, column):
        '''
        See if a move is a valid spot on the board.
        '''

        if row < 0 or row > 7:
            return False
        
        if column < 0 or column > 7:
            return False

        return True


    # @abstractmethod
    # def moves(self):
    #     '''Returns possible moves the piece can take.'''
    #     pass




class Pawn(Piece):

    title = 'Pawn'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        #keep track of whether pawn has moved yet to know if it can move two spaces or not
        self.moved = False

    
    def generate_all_moves_attacks(self):
        '''
        Finds all possible moves as if the board is empty,
        and finds all possible attacks as if each enemy piece 
        is alone on the board (as in, a piece behind another in view
        of an enemy queen will be accepted).
        '''


        possible_moves = []
        possible_attacks = []

        if self.color == 'White':
            #figure out all possible moves for white

            possible_moves.append((self.row - 1, self.column))

            #can move 2 spaces forward if pawn hasn't moved yet
            if not self.moved:
                possible_moves.append((self.row - 2, self.column))


            #figure out all possible attacks for white
            forward_left = (self.row - 1, self.column - 1)
            forward_right = (self.row - 1, self.column + 1)

            if self.validate_move(forward_left[0], forward_left[1]):
                possible_attacks.append((forward_left[0], forward_left[1]))

            if self.validate_move(forward_right[0], forward_right[1]):
                possible_attacks.append((forward_right[0], forward_right[1]))

        #when pawn is black
        else:

            possible_moves.append((self.row + 1, self.column))

            if not self.moved:
                possible_moves.append((self.row + 2, self.column))

            forward_left = (self.row + 1, self.column - 1)
            forward_right = (self.row + 1, self.column + 1)

            if self.validate_move(forward_left[0], forward_left[1]):
                possible_attacks.append((forward_left[0], forward_left[1]))

            if self.validate_move(forward_right[0], forward_right[1]):
                possible_attacks.append((forward_right[0], forward_right[1]))

        return (possible_moves, possible_attacks)

    
    def moves(self, board):
        '''
        Return tuple made of two lists. The first list represents
        possible coordinates the piece can move to erowcluding attacking
        moves, and the second list represents solely attacking moves.

        Starts with lists of all possible moves & all possible attacks, and 
        removes all invalid moves.
        '''
        
        #all possible moves & all possible attacks, 
        possible_moves, possible_attacks = self.generate_all_moves_attacks()

        #pawn only has potential to move forward 1 square
        if len(possible_moves) == 1:
            forward = possible_moves[0] #stores position of 1 square in front of pawn

            #if there is a piece in this position, pawn can't move
            if board[forward.row][forward.column] is not None:
                del possible_moves[0]


        if len(possible_moves) == 2:
            forward = possible_moves[0]
            forward_two = possible_moves[1]

            # print(f'forward 0: {forward[0]}, forward 1: {forward[1]}')
            if board[forward[0]][forward[1]] is not None:
                possible_moves.clear() #pawn also can't move 2 spaces forward because another piece is in the way

            elif board[forward_two[0]][forward_two[1]] is not None:
                del possible_moves[1] #can move forward 1 space, but forward two is occupied by another piece


        possible_attacks[:] = [row for row in possible_attacks if board[row[0]][row[1]] is not None]
        possible_attacks[:] = [row for row in possible_attacks if board[row[0]][row[1]].color != self.color]

        return (possible_moves, possible_attacks)
                





class Rook(Piece):

    title = 'Rook'



class Knight(Piece):

    title = 'Knight'



class Bishop(Piece):

    title = 'Bishop'



class Queen(Piece):

    title = 'Queen'



class King(Piece):

    title = 'King'

