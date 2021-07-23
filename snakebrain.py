import random

width = 0
height = 0
Gboard = {}
Gbody = {}
Gfood = {}
Gdata = {}
def get_next_move(data):
  global width
  global height
  global Gboard
  global Gbody
  global Gfood
  global Gdata
  Gdata = data
  Gbody = data["you"]["body"]
  width = data["board"]["width"]
  height = data["board"]["height"]
  Gboard = data["board"]
  Gfood = Gboard["food"]
  coord = Gdata["you"]["head"]
  moves = get_all_moves(coord)
  safe_moves = []
  return_string_list = []
  for move in moves:
    if avoid_walls(move, width, height) and avoid_self(Gbody, move) and avoid_others(data, move):
      safe_moves.append(move)
  for move in safe_moves:
    return_string_list.append(move_to_string(move, coord))
  return return_string_list

def get_all_moves(head):

  return [{'x': head['x'], 'y': head['y'] + 1}, {'x': head['x'], 'y': head['y'] - 1}, {'x': head['x'] + 1, 'y': head['y']}, {'x': head['x'] - 1, 'y': head['y']}]

#move testing functions return true if safe, false if unsafe

def avoid_walls(future_head, board_width, board_height):
  safe = True
  x = int(future_head["x"])
  y = int(future_head["y"])
  if x < 0 or y < 0 or x >= board_width or y >= board_height:
    safe = False
  return safe

def avoid_self(body, future_head):
  segments = []
  b = simulate_next_move(Gdata, future_head)
  for segment in b[1:]:
    segments.append([int(segment["x"]), int(segment["y"])])
  head_x = int(future_head["x"])
  head_y = int(future_head["y"])
  fut_pos = [head_x, head_y]
  safe = True
  if fut_pos in segments :
    safe = False
  return safe

def avoid_others(data, future_head):
  for snake in data["board"]["snakes"]:
    if future_head in snake["body"][:-1]:
      return False

  return True
def shouldEat(move):
  m = string_to_move(move, Gdata["you"]["head"])
  for snake in Gboard["snakes"]:
    potential = get_all_moves(snake["head"])
    if snake["id"] == Gdata["you"]["id"]:
      continue
    if m in potential:
      if Gdata["you"]["length"] <= snake["length"]:
        print(move + " UNSAFE")
        return -2
      else:
        return 2
  print(move + " safe")
  return 0
def prune_safe_moves(body, moves):
  random.shuffle(moves)
  safest = 0
  temp = 0
  safest_move = moves[0]
  head = Gdata["you"]["head"]
  for move in moves:
    temp = get_safe_squares(simulate_next_move(body, string_to_move(move, head)))
    if isCorner(move):
      temp -= 1
    temp += shouldEat(move)
    if string_to_move(move, head) in Gfood and temp > 1:
      temp += 2
    try:
      if string_to_move(move, head) in Gboard["hazards"]:
        temp -= 1
    except:
      pass
    if Gdata["you"]["health"] < 30 and seekFood(string_to_move(move, Gdata["you"]["head"])) and temp > 1:
      temp += 2
    if temp > safest:
      safest = temp
      safest_move = move
  return safest_move
def simulate_next_move(data, move):
  sim_body = Gbody
  for i in range(len(sim_body) - 1, 0):
    sim_body[i] = sim_body[i - 1]
  sim_body[0] = move
  return sim_body
def get_safe_squares(sim_body):
    fake_data = Gdata
    fake_data["you"]["body"] = sim_body[1:]
    fake_data["you"]["head"] = sim_body[0]
    return len(get_next_move(fake_data))

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

def prune_food(moves, food):
  temp = {}
  rlist = []
  for move in moves:
    temp = string_to_move(move, Gdata["you"]["head"])
    if temp not in food:
      rlist.append(move)
  if(len(rlist) == 0):
    return moves
  return rlist

def isCorner(move):
  m = string_to_move(move, Gdata["you"]["head"])
  return (m["x"] == 0 or m["x"] == width) and (m["y"] == 0 or m["y"] == height)

def seekFood(move):
  foodList = Gdata["board"]["food"]
  head = Gdata["you"]["head"]
  closestFoodDist = 99
  temp = 99
  closestFood = {}
  for food in foodList:
      temp  = distFrom(food, head)
      if temp < closestFoodDist:
          closestFoodDist = temp
          closestFood = food
  if distFrom(closestFood, head) > distFrom(move, closestFood):
      return True
  else:
      return False
def distFrom(c1, c2):
    return abs(c1["x"] - c2["x"]) + abs(c1["y"] - c2["y"])
