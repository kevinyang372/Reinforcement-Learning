import numpy as np
import random

strategy1 = [] #strategy for game player one
strategy2 = [] #strategy for game player two

#check the line
def Check_line(line,player):
    positive_count = 0
    negative_count = 0
    for i in line:
        if i == -1:
            negative_count += 1
        elif i == 1:
            positive_count += 1
    if player == 1:
        if positive_count == 2 and negative_count == 0:
            return True
    else:
        if negative_count == 2 and positive_count == 0:
            return True
    return False

#check the game condition
def Game_end(board, player):
    for i in board:
        if Check_line(i,player):
            return True

    for k in range(len(board)):
        sum = []
        for i in board:
            sum.append(i[k])
        if Check_line(sum,player):
            return True

    if Check_line([board[0][0], board[1][1], board[2][2]], player):
        return True
    elif Check_line([board[0][2], board[1][1], board[2][0]], player):
        return True

    return False

#check whether the board is filled
def Filled(board):
    haszero = False
    for i in board:
        for k in i:
            if i[k] == 0:
                haszero = True
                break
    if not haszero:
        return True
    return False

#initialize an empty board
def Start_Game():
    board = []
    for i in range(3):
        board.append([0,0,0])
    return board

#decide the next step
def Strategy(strategy_now,current_board):
    selection = []
    #get the previous strategies
    for i in range(len(strategy_now)):
        if strategy_now[i][0] == current_board:
            selection.append([strategy_now[i][1],strategy_now[i][2]])
    #get all the available options
    current_options = available_options(current_board)
    #update the likelihood of choosing specific options
    for i in current_options:
        for t in selection:
            if i[0] == t[0]:
                i[1] += t[1]
    #determine the next step
    selected = randomization(current_options)
    return current_options[selected][0]

#update board with the specific move
def Update_board(player, move, current_board):
    if player == 1:
        current_board[move[0]][move[1]] = 1
    else:
        current_board[move[0]][move[1]] = -1
    return current_board

#create the clone of a list
def duplicate_list(lists):
    temp = []
    for i in lists:
        temp.append(list(i))
    return temp

#main function
def Play_Game():
    #initialization
    board = Start_Game()
    winner = 0
    current_strategy1 = []
    current_strategy2 = []

    #loop until the game ends
    while True:
        #check end game
        if Game_end(board, 1) or Filled(board):
            if Game_end(board, 1):
                winner = 1
            break;
        #select move for player one
        action = Strategy(strategy1,board)
        this_board = duplicate_list(board)
        #append the current move to the strategy for this game
        current_strategy1.append([this_board,action])
        board = Update_board(1,action,board)
        #output game status
        present_board(board)
        if Game_end(board, -1) or Filled(board):
            if Game_end(board, -1):
                winner = -1
            break;
        #select move for player two
        action = Strategy(strategy2,board)
        this_board2 = duplicate_list(board)
        #append the current move to the strategy for this game
        current_strategy2.append([this_board2,action])
        board = Update_board(-1,action,board)
        #output game status
        present_board(board)

    #award winners and punish losers
    if winner == 1:
        update_strategy(strategy1,current_strategy1,10)
        update_strategy(strategy2,current_strategy2,-10)
    elif winner == -1:
        update_strategy(strategy1,current_strategy1,-10)
        update_strategy(strategy2,current_strategy2,10)

#update the strategy with the last game
def update_strategy(strategy_to_update,new_strategy,reward):
    for t in new_strategy:
        updated = False
        for i in strategy_to_update:
            if i[0] == t[0] and i[1] == t[1]:
                i[2] += reward
                updated = True
                break
        if not updated:
            strategy_to_update.append([t[0],t[1],reward*10])

#check all the available_options
def available_options(current_board):
    options = []
    for i in range(len(current_board)):
        for k in range(len(current_board)):
            if current_board[i][k] == 0:
                options.append([[i,k],100])
    return options

#randomize the strategy selection
def randomization(current_options):
    num = []
    for i in current_options:
        num.append(i[1])
    minimum = np.min(num)
    if np.sum(num) < 0:
        for i in range(len(num)):
            num[i] -= minimum
    interval = [num[0]]
    for t in range(1,len(num)):
        interval.append(num[t] + interval[t-1])
    if np.sum(num) < 0:
        print(num)
    pick = random.randint(0,np.sum(num))
    for t in range(0,len(interval)):
        if interval[t] >= pick:
            return t
    return "Error"

#output board
def present_board(board):
    print("================")
    for i in board:
        print(i[0],'| ',i[1],'| ',i[2])
    print("================")

for i in range(10000):
    Play_Game()

while True:
    print("New Game?")
    determine = input()
    if determine.lower() == "no":
        break
    print("===================")
    winner = 0
    board = Start_Game()
    while True:
        if Game_end(board, 1) or Filled(board):
            if Game_end(board, 1):
                winner = 1
            break;
        #select move for player one
        print("Please enter your next move")
        move = input()
        action = [int(move.split(',')[0]), int(move.split(',')[1])]
        board = Update_board(1,action,board)
        #output game status
        present_board(board)
        if Game_end(board, -1) or Filled(board):
            if Game_end(board, -1):
                winner = -1
            break;
        #select move for player two
        action = Strategy(strategy2,board)
        board = Update_board(-1,action,board)
        #output game status
        present_board(board)

    print("Winner is ",winner)
