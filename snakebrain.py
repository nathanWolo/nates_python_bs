import random

import copy


def get_all_moves(head):

    return [{
        'x': head['x'],
        'y': head['y'] + 1
    }, {
        'x': head['x'],
        'y': head['y'] - 1
    }, {
        'x': head['x'] + 1,
        'y': head['y']
    }, {
        'x': head['x'] - 1,
        'y': head['y']
    }]


#move testing functions return true if safe, false if unsafe
def get_safe_moves(data, snake):
    moves = get_all_moves(snake["head"])
    safe_moves = []
    return_string_list = []
    head = snake["head"]
    for move in moves:
        #print("move", move)
        # print("avoids walls", avoid_walls(move, data["board"]["width"], data["board"]["height"]))
        # print("avoids snakes", avoid_snakes(data, move))
        if avoid_walls(move, data["board"]["width"],
                       data["board"]["height"]) and avoid_snakes(data, move):
            safe_moves.append(move)
    for move in safe_moves:
        return_string_list.append(move_to_string(move, head))
    return return_string_list


def avoid_walls(future_head, board_width, board_height):
    safe = True
    x = int(future_head["x"])
    y = int(future_head["y"])
    if x < 0 or y < 0 or x >= board_width or y >= board_height:
        safe = False
    return safe


def avoid_snakes(data, future_head):
    for snake in data["board"]["snakes"]:
        if future_head in snake["body"][:-1]:
            return False
    return True


def shouldEat(data, move):
    m = string_to_move(move, data["you"]["head"])
    board = data["board"]
    for snake in board["snakes"]:
        potential = [
            string_to_move(m, snake['body'][0])
            for m in get_safe_moves(data, snake)
        ]
        #print(potential)
        if snake["id"] == data["you"]["id"]:
            continue
        if m in potential:
            if data["you"]["length"] <= snake["length"]:
                print("shouldnt eat", move)
                return -5
            else:
                print("should eat", move)
                return 3
    #print("no eat decision", move)
    return 0


def prune_safe_moves(data, moves):
    board = data["board"]
    food = board["food"]
    random.shuffle(moves)
    safest = 0
    temp = 0
    safest_move = moves[0]
    head = data["you"]["head"]
    # futures = get_possible_futures(data)
    # print(len(futures))
    for move in moves:
        #check enclosure size
        temp = 0
        for snake in board['snakes']:
            temp += distFrom(string_to_move(move, data['you']['body'][0]),
                             snake['body'][0]) / 5
        temp += score_enclosure(data, string_to_move(move, head)) / 5
        if len(board['snakes']) == 2:
            our_index = 0
            if board['snakes'][0]['id'] != data['you']['id']:
                our_index = 1
                other_index = our_index + 1
                other_index = other_index % 2
                try:
                  temp -= score_enclosure(
                    simulate_next_move(
                        data, our_index,
                        string_to_move(move, data['you']['head'])),
                    string_to_move(random.choice(get_safe_moves(data,board['snakes'][other_index])), board['snakes'][other_index]['body'][0])) / 10
                except:
                  pass
        temp += shouldEat(data, move)
        if string_to_move(move, head) in food and temp > 1:
            temp += 2
        try:
            if string_to_move(move, head) in board["hazards"]:
                temp -= 1
        except:
            pass
        if seekFood(data, string_to_move(move,
                                         data["you"]["head"])) and temp > 1:
            temp += 1
        print('move: ', move, 'score: ', temp)
        if temp > safest:
            safest = temp
            safest_move = move
    return safest_move


def simulate_next_move(data, snake_index: int, move):
    '''take in a board state, move and snake. apply the move to the snake and return the new board state '''
    new_data = copy.deepcopy(data)
    new_data['board']['snakes'][snake_index]['body'].insert(0, move)
    if move not in data["board"]["food"]:
        new_data['board']['snakes'][snake_index]['body'].pop()
    return new_data


def get_safe_squares(data, sim_body):
    fake_data = data
    fake_data["you"]["body"] = sim_body[1:]
    fake_data["you"]["head"] = sim_body[0]
    return len(get_safe_moves(fake_data, fake_data["you"]))


def move_to_string(move, coord):
    up = {'x': coord['x'], 'y': coord['y'] + 1}
    down = {'x': coord['x'], 'y': coord['y'] - 1}
    right = {'x': coord['x'] + 1, 'y': coord['y']}
    if move == up:
        return "up"
    elif move == down:
        return "down"
    elif move == right:
        return "right"
    else:
        return "left"


def string_to_move(move, coord):
    if move == "up":
        return {'x': coord['x'], 'y': coord['y'] + 1}
    elif move == "down":
        return {'x': coord['x'], 'y': coord['y'] - 1}
    elif move == "right":
        return {'x': coord['x'] + 1, 'y': coord['y']}
    else:
        return {'x': coord['x'] - 1, 'y': coord['y']}


def prune_food(data, moves, food):
    temp = {}
    rlist = []
    for move in moves:
        temp = string_to_move(move, data["you"]["head"])
        if temp not in food:
            rlist.append(move)
    if (len(rlist) == 0):
        return moves
    return rlist


# def isCorner(data, move):
#   m = string_to_move(move, data["you"]["head"])
#   board = data["board"]
#   return (m["x"] == 0 or m["x"] == board["width"]) and (m["y"] == 0 or m["y"] == board["height"])


def seekFood(data, move):
    foodList = data["board"]["food"]
    head = data["you"]["head"]
    closestFoodDist = 99
    temp = 99
    closestFood = {}
    for food in foodList:
        temp = distFrom(food, head)
        if temp < closestFoodDist:
            closestFoodDist = temp
            closestFood = food
    if distFrom(closestFood, head) > distFrom(move, closestFood):
        return True
    else:
        return False


def distFrom(c1, c2):
    return abs(c1["x"] - c2["x"]) + abs(c1["y"] - c2["y"])


def get_lifetime_of_segment(data, coord):
    for snake in data["board"]["snakes"]:
        if coord in snake["body"]:
            return len(snake["body"]) - snake["body"].index(coord)


def get_neighbors(coord, data):
    '''return a list of all the neighbors of a coordinate'''
    neighbors = []
    board = data["board"]
    for move in ["up", "down", "left", "right"]:
        neighbor = string_to_move(move, coord)
        if avoid_walls(neighbor, board["width"], board["height"]) and (
                avoid_snakes(data, neighbor) or get_lifetime_of_segment(
                    data, neighbor) < distFrom(neighbor, data['you']['head'])
        ) or (neighbor == data['you']['body'][-1]):
            neighbors.append(neighbor)
    return neighbors


def score_enclosure(data, move):
    '''detect if a move will put the snake in an enclosed area (between body segments and walls)
  if so, return the number of moves it will take to fill using the flood fill algorithm'''
    # flood fill algorithm
    # https://en.wikipedia.org/wiki/Flood_fill
    seen_tiles = list()
    queue = [move]
    while queue:
        current = queue.pop(0)
        if current in seen_tiles:
            continue
        seen_tiles.append(current)
        for neighbor in get_neighbors(current, data):
            if neighbor not in seen_tiles:
                queue.append(neighbor)
    print('FLOOD FILL: move: ', move_to_string(move, data['you']['body'][0]),
          "score", len(seen_tiles))
    score = len(seen_tiles)
    if data['you']['body'][-1] in seen_tiles:
        score += len(data['you']['body'])
        for tile in seen_tiles:
            if tile in data['board']['food']:
                score -= 1
    return score


# def get_possible_futures(data):
#     '''return a list of all possible future boards'''
#     futures = []
#     moves_per_snake = []
#     num_futures = 1
#     for snake_index in range(len(data['board']['snakes'])):
#         moves_per_snake.append((snake_index, get_safe_moves(data, data['board']['snakes'][snake_index])))
#         num_futures = num_futures * len(moves_per_snake[snake_index][1])
#     for _ in range(num_futures):
#         possible_future = copy.deepcopy(data)
#         move_indices = list(0 for i in range(len(possible_future['board']['snakes'])))
#         for snake_index in range(len(possible_future['board']['snakes'])):
#             possible_future = simulate_next_move(possible_future, snake_index, moves_per_snake[snake_index][1][move_indices[snake_index]])
#         for i in range(len(possible_future['board']['snakes'])):
#             if move_indices[i] < len(moves_per_snake[i][1]) - 1:
#                 move_indices[i] += 1
#                 break
#             elif move_indices[i] == len(moves_per_snake[i][1]) - 1:
#                 move_indices[i] = 0
#         futures.append(possible_future)
#     return futures
