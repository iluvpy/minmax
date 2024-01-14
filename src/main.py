import random

# constants
PL_CIRCLE = 0
PL_CROSS = 1 
NODE_DRAW = 3
LEFT = 1
RIGHT = 2

def is_draw(board):
    numbers = 0
    for n in board:
        if type(n) == int:
            numbers += 1
    if not numbers:
        return True
    
def won(board):
    for i in range(3): # horizontals
        if board[0 + i * 3] == board[1 + i * 3] and board[1 + i * 3] == board[2 + i * 3]:
            return True
    
    for i in range(3): # verticals
        if board[0 + i] == board[3 + i] and board[3 + i] == board[6 + i]:
            return True
    
    # diagonals
    if board[0] == board[4] and board[4] == board[8]:
        return True
    if board[2] == board[4] and board[4] == board[6]:
        return True
    
    return False

def player_sign(turn):
    return "X" if turn == PL_CROSS else "O"

def free_locations(board):
    free_locations = []
    for i, n in enumerate(board):
        if type(n) == int:
            free_locations.append(i)
    return free_locations

class Node:
    def __init__(self) -> None:
        self.right = None
        self.left = None
        self.won = None
        self.draw = False

    def calculate(self, board: list, turn):
        print(f"calculate function was called by {self}!")
        if won(board):
            print("won in calculate function")
            self.won = not turn
            return
        
        locations = free_locations(board)

        if len(locations) <= 0:
            self.draw = True
            print("draw in calculate function")
            return
    
        left_choice = random.choice(locations)
        locations.remove(left_choice)

        if len(locations) <= 0:
            self.draw = True
            return
        
        right_choice = random.choice(locations)

        left_board = board.copy()
        left_board[left_choice] = player_sign(turn)
        self.left = Node()
        self.left.calculate(left_board, not turn)

        right_board = board.copy()
        right_board[right_choice] = player_sign(turn)
        self.right = Node()
        self.right.calculate(right_board, not turn)


class MinMaxTree:
    def __init__(self, board, turn) -> None:
        self.head = Node()
        self.head.calculate(board, turn)


def parse_mm_tree(node: Node, turn, turns=[]) -> tuple:

    if node.won is not None:
        return Node, node == turn, turns
    
    if node.draw:
        return Node, 3, turns
    
    result_r = parse_mm_tree(node.right, turn, [RIGHT] + turns)
    if result_r[1] == True:
        return result_r
    
    return parse_mm_tree(node.left, turn, [LEFT] + turns)

def minmax(board, turn) -> int:
    min_max_tree = MinMaxTree(board, turn)

    winning_node = parse_mm_tree(min_max_tree.head, turn)
    print(winning_node)
    print(f"minmax winning node: {['LEFT' if i == LEFT else 'RIGHT' for i in winning_node[2]]}") 
    


def main():
    print("Tic Tac Toe, play against the computer!")
    player = input("X or O? ")
    turn = PL_CROSS if player == "X" else PL_CIRCLE
    first = turn
    board = [i + 1 for i in range(9)]

    while True:
        print(f"|{board[0]}|{board[1]}|{board[2]}|") 
        print("-------") 
        print(f"|{board[3]}|{board[4]}|{board[5]}|")  
        print("-------") 
        print(f"|{board[6]}|{board[7]}|{board[8]}|")  

        if is_draw(board):
            print("\nIts a draw!")
            break
        if won(board):
            print(f"\n{player_sign(turn)} has won!")
            break

        if first == turn: # players turn
            print("its your turn!")
            index = int(input("where do you want to place? ")) - 1
            board[index] = player_sign(turn)
        else:
            print("start minmax")
            minmax(board, turn)
            print("done calculations!")
            break

        turn = not turn
        
        print("")
        print("")
        print("")


if __name__ == "__main__":
    main()