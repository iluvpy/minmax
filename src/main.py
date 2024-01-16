import random

# constants
PL_CIRCLE = 0
PL_CROSS = 1 
WON = 1


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

# Min Max Node
class MM_Node:
    def __init__(self) -> None:
        self.draw = False
        self.child_nodes = []
        self.choices = []
        self.val = 0
        self.initial_turn = 0
        self.is_child = False

    def calculate(self, board: list, turn):
        if won(board):
            self.val = 10 if not turn == self.initial_turn else -10
            return 
        
        locations = free_locations(board)
        if len(locations) <= 0:
            self.val = 0
            return
        for free_loc in locations:
            child_node = MM_Node()
            self.child_nodes.append(child_node)
            self.choices.append(free_loc)
            new_board = board.copy()
            new_board[free_loc] = player_sign(turn)
            child_node.initial_turn = self.initial_turn
            child_node.is_child = True
            child_node.calculate(new_board, not turn)

        # if any node (besides the first node) has children with losing options, its a bad move
        if -10 in [child_node.val for child_node in self.child_nodes] and self.is_child: 
            self.val = -10
            return
        self.val = 0
        for child_node in self.child_nodes:
            if child_node.val > self.val:
                self.val = child_node.val


    
def minmax(board, turn) -> int:
    initial_node = MM_Node()
    initial_node.initial_turn = turn
    initial_node.calculate(board, turn)

    child_nodes = initial_node.child_nodes
    print([n.val for n in child_nodes])
    print([n.is_child for n in child_nodes])
    print(initial_node.is_child)
    for i, node in enumerate(child_nodes):
        if node.val == 10:
            return node.choices[i]
    # draw
    for i, node in enumerate(child_nodes):
        if node.val == 0:
            return node.choices[i]
    


def main():
    print("Tic Tac Toe, play against the computer!")
    player = input("X or O? ")
    turn = PL_CROSS if player == "X" else PL_CIRCLE
    first = turn
    board = [i + 1 for i in range(9)]

    while True:
        if is_draw(board):
            print("\nIts a draw!")
            break
        if won(board):
            print(f"\n{player_sign(not turn)} has won!")
            break

        if first == turn: # players turn
            print(f"|{board[0]}|{board[1]}|{board[2]}|") 
            print("-------") 
            print(f"|{board[3]}|{board[4]}|{board[5]}|")  
            print("-------") 
            print(f"|{board[6]}|{board[7]}|{board[8]}|")  
            print("its your turn!")
            index = int(input("where do you want to place? ")) - 1
            board[index] = player_sign(turn)
            print("\n"*5) 
        else:
            board[minmax(board, turn)] = player_sign(turn)

        turn = not turn
        


if __name__ == "__main__":
    main()