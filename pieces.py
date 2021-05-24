
from abc import ABC, abstractmethod

class Piece(ABC):

    def __init__(self, position, color=None):
        
        self.position = position
        self.x = position[0]
        self.y = position[1]

        self.color = color

        super().__init__()



    def print_position(self):
        print(f'{self.title} located @ ({self.x}, {self.y})')

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