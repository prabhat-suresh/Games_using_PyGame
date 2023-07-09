def manhattan(direction,snake_position,fruit_position):
    if direction=="UP":
        if snake_position[1]>fruit_position[1]:
            return "UP"
        if snake_position[0]<=fruit_position[0]:
            return "RIGHT"
        return "LEFT"

    elif direction=="DOWN":
        if snake_position[1]<fruit_position[1]:
            return "DOWN"
        if snake_position[0]<=fruit_position[0]:
            return "RIGHT"
        return "LEFT"

    elif direction=="LEFT":
        if snake_position[0]>fruit_position[0]:
            return "LEFT"
        if snake_position[1]<=fruit_position[1]:
            return "DOWN"
        return "UP"

    else:
        if snake_position[0]<fruit_position[0]:
            return "RIGHT"
        if snake_position[1]<=fruit_position[1]:
            return "DOWN"
        return "UP"
