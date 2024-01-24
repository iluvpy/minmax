import random

# constants
PL_CIRCLE = 0
PL_CROSS = 1 
WON = 1

emoji_map = {
    1: "1️⃣", 
    2: "2️⃣", 
    3: "3️⃣", 
    4: "4️⃣", 
    5: "5️⃣", 
    6: "6️⃣", 
    7: "7️⃣", 
    8: "8️⃣", 
    9: "9️⃣"
}

def print_board(board):
    emoji_board = []
    for n in board:
        if n in emoji_map:
            emoji_board.append(str(emoji_map[n]))
        else:
            emoji_board.append(n)
    print(f"{emoji_board[0]} {emoji_board[1]} {emoji_board[2]}") 
    print(f"{emoji_board[3]} {emoji_board[4]} {emoji_board[5]}")  
    print(f"{emoji_board[6]} {emoji_board[7]} {emoji_board[8]}")  

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
    return "🇽" if turn == PL_CROSS else "🇴"

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
        self.val = 0 # 10 = win, 0 = draw, -10 = losing
        self.initial_turn = 0 # the starting turn

    def calculate(self, board: list, turn):

        locations = free_locations(board)
        if len(locations) <= 0:
            self.val = 0
            return
        
        if won(board):
            # "not turn == ..." because the parent node gave the child "not turn"
            self.val = 10 if (not turn) == self.initial_turn else -10
            return 
        

        for free_loc in locations:
            child_node = MM_Node()
            self.child_nodes.append(child_node)
            self.choices.append(free_loc)
            new_board = board.copy()
            new_board[free_loc] = player_sign(turn)
            child_node.initial_turn = self.initial_turn
            child_node.calculate(new_board, not turn)

        # summing all values will lead to the best node
        value_sum = 0
        for child_node in self.child_nodes:
            value_sum += child_node.val
        self.val = value_sum

    

def minmax(board, turn) -> int:
    initial_node = MM_Node()
    initial_node.initial_turn = turn
    initial_node.calculate(board, turn)

    child_nodes = initial_node.child_nodes
    
    #print([n.val for n in child_nodes])

    max_val = max([n.val for n in child_nodes])
    for i, node in enumerate(child_nodes):
        if node.val == max_val:
            return initial_node.choices[i]



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
            print(f"\n{player_sign(not turn)}  has won!")
            break

        if first == turn: # players turn
            print("\n"*20) 
            print("its your turn!")
            print_board(board)
            index = int(input("where do you want to place? ")) - 1
            board[index] = player_sign(turn)
        else:
            board[minmax(board, turn)] = player_sign(turn)



        turn = not turn

    print("\nfinal board:")
    print_board(board)

if __name__ == "__main__":
    main()