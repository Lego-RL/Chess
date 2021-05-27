
from abc import ABC, abstractmethod

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


    def generate_all_horizontal_moves(self, row, column):
        '''
        Returns a tuple containing two tuples, one for each horizontal
        direction. The first represents all potential moves left of the piece,
        and the second represents all potential moves right of the piece.

        The list of possible moves left the piece is reversed, to make
        the points begin next to the piece instead of at the top of the board.
        The 'right' moves already naturally start right below the piece.
        '''

        potential_left_moves = []
        potential_right_moves = []
        
        for i in range(0, column):
            potential_left_moves.append((row, i))


        for i in range(column + 1, 8): #0-7 is the range of the board, so stop at 8 exclusive
            potential_right_moves.append((row, i))


        potential_left_moves.reverse()

        return (tuple(potential_left_moves), tuple(potential_right_moves))



    def generate_all_vertical_moves(self, row, column):
        '''
        Returns a tuple containing two tuples, one for each vertical
        direction. The first represents all potential moves above the piece,
        and the second represents all potential moves below the piece.

        The list of possible moves "above" the piece is reversed, to make
        the points begin next to the piece instead of at the top of the board.
        The below moves already naturally start right below the piece.
        '''

        potential_above_moves = []
        potential_below_moves = []

        for i in range(0, row):
            potential_above_moves.append((i, column))

        
        for i in range(row + 1, 8): #0-7 is the range of the board, so stop at 8 exclusive
            potential_below_moves.append((i, column))


        potential_above_moves.reverse()

        return (tuple(potential_above_moves), tuple(potential_below_moves))



    def generate_all_diagonal_moves(self, row, column):
        '''
        Returns a tuple containing four tuples, one for each diagonal direction.
        The first represents the top left diagonal, the second represents the top right,
        the third represents the bottom left diagonal, and the fourth represents the bottom
        right diagonal.
        '''

        original_row = row
        original_column = column
        
        potential_top_left_moves = []
        potential_top_right_moves = []
        potential_bottom_left_moves = []
        potential_bottom_right_moves = []



        while row > 0 and column > 0:
            row -= 1
            column -= 1

            potential_top_left_moves.append((row, column))


        #reset vars
        row = original_row
        column = original_column

        while row > 0 and column < 7:
            row -= 1
            column += 1

            potential_top_right_moves.append((row, column))


        #reset vars
        row = original_row
        column = original_column

        while row < 7 and column > 0:
            row += 1
            column -= 1

            potential_bottom_left_moves.append((row, column))

        
        #reset vars
        row = original_row
        column = original_column

        while row < 7 and column < 7:
            row += 1
            column += 1

            potential_bottom_right_moves.append((row, column))


        return (tuple(potential_top_left_moves), tuple(potential_top_right_moves),
                tuple(potential_bottom_left_moves), tuple(potential_bottom_right_moves)) 


    def parse_all_possible_moves(self, all_moves, board):
        '''
        Takes all_moves and decides which moves are valid moves
        and possible attacks. I believe this only works on normalized lines, 
        like horizontal, vertical and diagonal lines. (Rook, Bishop, Queen)
        '''

        possible_moves, possible_attacks = [], []

        for potential_moves in all_moves:
            for move in potential_moves:
                if board[move[0]][move[1]] is None:
                    possible_moves.append(move)

                elif board[move[0]][move[1]].color != self.color:
                    possible_attacks.append(move)
                    break #can't move or attack behind a piece

                else:
                    break #can't move or attack behind your own piece

        return (tuple(possible_moves), tuple(possible_attacks))





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
        possible coordinates the piece can move to excluding attacking
        moves, and the second list represents solely attacking moves.

        Starts with lists of all possible moves & all possible attacks, and 
        removes all invalid moves.
        '''
        
        
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

            if board[forward[0]][forward[1]] is not None:
                possible_moves.clear() #pawn also can't move 2 spaces forward because another piece is in the way

            elif board[forward_two[0]][forward_two[1]] is not None:
                del possible_moves[1] #can move forward 1 space, but forward two is occupied by another piece


        possible_attacks[:] = [move for move in possible_attacks if board[move[0]][move[1]] is not None]
        possible_attacks[:] = [move for move in possible_attacks if board[move[0]][move[1]].color != self.color]

        return (possible_moves, possible_attacks)
                


class Rook(Piece):

    title = 'Rook'



    def moves(self, board):
        '''
        Return tuple made of two lists. The first list represents
        possible coordinates the piece can move to excluding attacking
        moves, and the second list represents solely attacking moves.

        Starts with lists of all possible moves & all possible attacks, and 
        removes all invalid moves.
        '''

        horizontal_moves = list(self.generate_all_horizontal_moves(self.row, self.column))
        vertical_moves = list(self.generate_all_vertical_moves(self.row, self.column))

        all_move_tuples = tuple(horizontal_moves + vertical_moves)

        return self.parse_all_possible_moves(all_move_tuples, board)



class Knight(Piece):

    title = 'Knight'


    def generate_all_moves_attacks(self):
        '''
        Finds all possible moves as if the board is empty,
        and finds all possible attacks as if each enemy piece 
        is alone on the board (as in, a piece behind another in view
        of an enemy queen will be accepted).
        '''

        #a knight's possible moves are the same as its possible attacks
        #starting with up two, right one tile move & moving clockwise
        possible_moves_attacks = [(self.row - 2, self.column + 1), (self.row - 1, self.column + 2), 
                                (self.row + 1, self.column + 2), (self.row + 2, self.column + 1), 
                                (self.row + 2, self.column - 1), (self.row + 1, self.column - 2),
                                (self.row - 1, self.column - 2), (self.row - 2, self.column - 1)]

        #[:] makes list comprehension delete bad elements in place instead of generating entire new list
        # make sure the moves aren't off the board with validate_move()
        # print(f'before list comp: {possible_moves_attacks}')
        possible_moves_attacks[:] = [move for move in possible_moves_attacks if self.validate_move(move[0], move[1])]
        # print(f'after list comp: {possible_moves_attacks}')



        return (possible_moves_attacks, tuple()) #for format to match, both moves and attacks (which are the same) are passed


    def moves(self, board):
        '''
        Return tuple made of two lists. The first list represents
        possible coordinates the piece can move to excluding attacking
        moves, and the second list represents solely attacking moves.

        Starts with lists of all possible moves & all possible attacks, and 
        removes all invalid moves.
        '''
        
        #moves and attacks are the same so possible attacks can be discarded in the case of the knight
        all_move_tuples, _ = self.generate_all_moves_attacks()

        possible_moves, possible_attacks = [], []

        for move in all_move_tuples:
            if board[move[0]][move[1]] is None:
                    possible_moves.append(move)

            elif board[move[0]][move[1]].color != self.color:
                possible_attacks.append(move)
                continue #can't move or attack behind a piece

            else:
                continue #can't move or attack behind your own piece

        return (tuple(possible_moves), tuple(possible_attacks))



class Bishop(Piece):

    title = 'Bishop'


    def moves(self, board):
        '''
        Return tuple made of two lists. The first list represents
        possible coordinates the piece can move to excluding attacking
        moves, and the second list represents solely attacking moves.

        Starts with lists of all possible moves & all possible attacks, and 
        removes all invalid moves.
        '''

        # potential_top_left_moves, potential_top_right_moves, \
        # potential_bottom_left_moves, potential_bottom_right_moves = self.generate_all_diagonal_moves(self.row, self.column)

        # all_move_tuples = (potential_top_left_moves, potential_top_right_moves, potential_bottom_left_moves, potential_bottom_right_moves)

        all_move_tuples = tuple(self.generate_all_diagonal_moves(self.row, self.column))

        return self.parse_all_possible_moves(all_move_tuples, board)



class Queen(Piece):

    title = 'Queen'


    def moves(self, board):
        '''
        Return tuple made of two lists. The first list represents
        possible coordinates the piece can move to excluding attacking
        moves, and the second list represents solely attacking moves.

        Starts with lists of all possible moves & all possible attacks, and 
        removes all invalid moves.
        '''

        horizontal_moves = list(self.generate_all_horizontal_moves(self.row, self.column))
        vertical_moves = list(self.generate_all_vertical_moves(self.row, self.column))

        diagonal_moves = list(self.generate_all_diagonal_moves(self.row, self.column))

        all_move_tuples = tuple(horizontal_moves + vertical_moves + diagonal_moves)

        return self.parse_all_possible_moves(all_move_tuples, board)



class King(Piece):

    title = 'King'

    def generate_all_moves_attacks(self):
        '''
        Finds all possible moves as if the board is empty,
        and finds all possible attacks as if each enemy piece 
        is alone on the board (as in, a piece behind another in view
        of an enemy queen will be accepted).
        '''

        #starts with move directly above king and goes clockwise
        #everywhere the king can move, he can attack, so moves & attacks are the same
        possible_moves_attacks = [(self.row - 1, self.column), (self.row - 1, self.column + 1),
                                (self.row, self.column + 1), (self.row + 1, self.column + 1),
                                (self.row + 1, self.column), (self.row + 1, self.column - 1),
                                (self.row, self.column - 1), (self.row - 1, self.column - 1)]


        possible_moves_attacks[:] = [move for move in possible_moves_attacks if self.validate_move(move[0], move[1])]

        return (possible_moves_attacks, tuple()) #for format to match, both moves and attacks (which are the same) are passed



    def moves(self, board):
        '''
        Return tuple made of two lists. The first list represents
        possible coordinates the piece can move to excluding attacking
        moves, and the second list represents solely attacking moves.

        Starts with lists of all possible moves & all possible attacks, and 
        removes all invalid moves.
        '''
        
        #moves and attacks are the same so possible attacks can be discarded in the case of the knight
        all_move_tuples, _ = self.generate_all_moves_attacks()

        possible_moves, possible_attacks = [], []

        for move in all_move_tuples:
            if board[move[0]][move[1]] is None:
                    possible_moves.append(move)

            elif board[move[0]][move[1]].color != self.color:
                possible_attacks.append(move)
                continue #can't move or attack behind a piece

            else:
                continue #can't move or attack behind your own piece

        return (tuple(possible_moves), tuple(possible_attacks))