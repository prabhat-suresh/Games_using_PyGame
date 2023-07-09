def is_adjacent(coord1,coord2):
    if coord1[0]==coord2[0] and (coord1[1]==coord2[1]+10 or coord1[1]==coord2[1]-10):
            return True

    elif coord1[1]==coord2[1] and (coord1[0]==coord2[0]+10 or coord1[0]==coord2[0]-10):
            return True

    return False

def is_safe(direction,snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
    next_position=[0,0]
    if direction=="UP":
        next_position=[snake_position[0],snake_position[1]-10]

        if snake_position[1]==0:
            return False

    elif direction=="DOWN":
        next_position=[snake_position[0],snake_position[1]+10]

        if snake_position[1]==window_y-10:
            return False

    elif direction=="LEFT":
        next_position=[snake_position[0]-10,snake_position[1]]

        if snake_position[0]==0:
            return False

    else:
        next_position=[snake_position[0]+10,snake_position[1]]

        if snake_position[0]==window_x-10:
            return False

    for block in snake_1_body:
        if block==next_position:
            return False

    if is_adjacent(snake_1_body[0],next_position):
        return False

    for block in snake_2_body:
        if block==next_position:
            return False

    if is_adjacent(snake_2_body[0],next_position):
        return False

    for block in snake_3_body:
        if block==next_position:
            return False

    if is_adjacent(snake_3_body[0],next_position):
        return False

    return True

def safe_manhattan(direction,snake_position,fruit_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
    if direction=="UP":
        available_moves=["RIGHT","LEFT","UP"]

        if is_safe("UP",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[1]>fruit_position[1]:
                return "UP"
        else:
            available_moves.remove("UP")

        if is_safe("RIGHT",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[0]<fruit_position[0]:
                return "RIGHT"
        else:
            available_moves.remove("RIGHT")

        if is_safe("LEFT",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[0]>fruit_position[0]:
                return "LEFT"
        else:
            available_moves.remove("LEFT")

        if available_moves:
            return available_moves[0]
        else:
            return direction

    elif direction=="DOWN":
        available_moves=["RIGHT","LEFT","DOWN"]

        if is_safe("DOWN",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[1]<fruit_position[1]:
                return "DOWN"
        else:
            available_moves.remove("DOWN")

        if is_safe("RIGHT",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[0]<fruit_position[0]:
                return "RIGHT"
        else:
            available_moves.remove("RIGHT")

        if is_safe("LEFT",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[0]>fruit_position[0]:
                return "LEFT"
        else:
            available_moves.remove("LEFT")

        if available_moves:
            return available_moves[0]
        else:
            return direction

    elif direction=="LEFT":
        
        available_moves=["DOWN","UP","LEFT"]

        if is_safe("LEFT",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[0]>fruit_position[0]:
                return "LEFT"
        else:
            available_moves.remove("LEFT")

        if is_safe("DOWN",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[1]<fruit_position[1]:
                return "DOWN"
        else:
            available_moves.remove("DOWN")

        if is_safe("UP",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[1]>fruit_position[1]:
                return "UP"
        else:
            available_moves.remove("UP")

        if available_moves:
            return available_moves[0]
        else:
            return direction

    else:
        available_moves=["DOWN","UP","RIGHT"]

        if is_safe("RIGHT",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[0]<fruit_position[0]:
                return "RIGHT"
        else:
            available_moves.remove("RIGHT")

        if is_safe("DOWN",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[1]<fruit_position[1]:
                return "DOWN"
        else:
            available_moves.remove("DOWN")

        if is_safe("UP",snake_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y):
            if snake_position[1]>fruit_position[1]:
                return "UP"
        else:
            available_moves.remove("UP")

        if available_moves:
            return available_moves[0]
        else:
            return direction
