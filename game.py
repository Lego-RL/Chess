from board import Board
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Game():

    def __init__(self):

        self.board = Board()
        self.board.game_board[1][4] = None
        self.board.game_board[1][3], self.board.game_board[0][3] = None, None

        # self.board.game_board[5][1] = Knight((5, 1), 'Black')

        self.turn = 'White'


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
            


game = Game()

# game.board.game_board[1][0]
moves, attacks = game.board.game_board[0][4].moves(game.board.game_board)
print(f'King @ (0, 4) moves: {moves}\nattacks: {attacks}\n')

game.print_board_to_console()

