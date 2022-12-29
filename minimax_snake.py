from snakebrain import get_all_moves, simulate_next_move
import random

#our evaluation function for how "good" a move is in the minimax tree for a given board state and snake
#will use the average result of many random playouts
def random_playout(data, you, initial_move):
    dead = False
    turns_elapsed = 0
    sim_data = apply_move_to_board(data, you, initial_move)
    while not dead:
        turns_elapsed += 1
        for snake in board["snakes"]:
            snakes_move = random.choice(get_all_moves(snake["head"]))
            sim_data = apply_move_to_board(sim_data, snake, snakes_move)
        
        
        for snake in sim_data["snakes"]:
            if killed(snake):
                sim_data["snakes"].remove(snake)
                if snake["id"] == you["id"]:
                    dead = True
                    break



#function takes a board state, an agent and an action
#returns the new board state
def apply_move_to_board(data, snake, move):
    new_board = data
    new_board["snakes"][snake["id"]]["body"] = simulate_next_move(snake, move)
    new_board["snakes"][snake["id"]]["head"] = new_board["snakes"][snake["id"]]["body"][0]
    return new_board


#function checks if a snake is dead given current board state
#e.g its head is in the same position as a snakes body
#returns a boolean
def killed(board, snake):
    head = snake["head"]
    