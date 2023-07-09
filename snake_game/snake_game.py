import pygame
import time
import random
import agent
import adversaries
 
snake_speed = 15
 
# Window size
window_x = 720 # 1440
window_y = 480 # 960
 
# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
 
# Initialising pygame
pygame.init()
 
# Initialise game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))
 
# FPS (frames per second) controller
fps = pygame.time.Clock()
 
# defining snake's starting position
snake_position = [100, 50]
 
# defining first 4 blocks of snake's body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

# defining adversary snakes' starting positions similarly
snake_1_position = [window_x-100, 50]
 
snake_1_body = [[window_x-100, 50],
              [window_x-90, 50],
              [window_x-80, 50],
              [window_x-70, 50]
              ]

snake_2_position = [window_x-100, window_y-50]
 
snake_2_body = [[window_x-100, window_y-50],
              [window_x-90, window_y-50],
              [window_x-80, window_y-50],
              [window_x-70, window_y-50]
              ]

snake_3_position = [100, window_y-50]
 
snake_3_body = [[100, window_y-50],
              [90, window_y-50],
              [80, window_y-50],
              [70, window_y-50]
              ]

# fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10]
 
fruit_spawn = True
 
# setting default snake direction towards
# right
direction = 'RIGHT'
# change_to = direction

# similarly for adversaries
direction1 = 'LEFT'
# change_to1 = direction

direction2 = 'LEFT'
# change_to2 = direction
 
direction3 = 'RIGHT'
# change_to3 = direction

# initial score
score = 0
 
# displaying Score function
def show_score(choice, color, font, size):
   
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)
     
    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)
     
    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()
     
    # displaying text
    game_window.blit(score_surface, score_rect)
 
# game over function
def game_over():
   
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
     
    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
     
    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()
     
    # setting position of the text
    game_over_rect.midtop = (window_x/2, window_y/4)
     
    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
     
    # after 2 seconds we will quit the program
    time.sleep(2)
     
    # deactivating pygame library
    pygame.quit()
     
    # quit the program
    quit()

# adversaries must respawn at a place not occupied by other snakes
def respawn(snake_1_position,snake_1_body,snake_body,snake_2_body,snake_3_body,num):
    inc=0
    if num==3:
        global direction3
        direction3="RIGHT"

    elif num==1:
        global direction1
        direction1="LEFT"

    else:
        global direction2
        direction2="LEFT"

    flag=True
    while flag:
        snake_1_position.clear()
        snake_1_position.extend([window_x-100, 50+inc]);
         
        snake_1_body.clear()
        snake_1_body.extend([[window_x-100, 50+inc],
                      [window_x-90, 50+inc],
                      [window_x-80, 50+inc],
                      [window_x-70, 50+inc]
                      ])

        inc+=50

        flag=False

        for block in snake_body:
            for own_block in snake_1_body:
                if own_block==block:
                    flag=True

        if flag:
            continue

        for block in snake_2_body:
            for own_block in snake_1_body:
                if own_block==block:
                    flag=True

        if flag:
            continue

        for block in snake_3_body:
            for own_block in snake_1_body:
                if own_block==block:
                    flag=True

# Main Function
while True:
    direction1=agent.safe_manhattan(direction1,snake_1_position,fruit_position,snake_body,snake_2_body,snake_3_body,window_x,window_y) 
    direction2=agent.safe_manhattan(direction2,snake_2_position,fruit_position,snake_body,snake_1_body,snake_3_body,window_x,window_y) 
    direction3=agent.safe_manhattan(direction3,snake_3_position,fruit_position,snake_body,snake_2_body,snake_1_body,window_x,window_y) 

    # handling key events
    # for event in pygame.event.get():
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_UP:
    #             change_to = 'UP'
    #         if event.key == pygame.K_DOWN:
    #             change_to = 'DOWN'
    #         if event.key == pygame.K_LEFT:
    #             change_to = 'LEFT'
    #         if event.key == pygame.K_RIGHT:
    #             change_to = 'RIGHT'
 
    direction=agent.safe_manhattan(direction,snake_position,fruit_position,snake_1_body,snake_2_body,snake_3_body,window_x,window_y)
    # If two keys pressed simultaneously
    # we don't want snake to move into two
    # directions simultaneously
    # if change_to == 'UP' and direction != 'DOWN':
    #     direction = 'UP'
    # if change_to == 'DOWN' and direction != 'UP':
    #     direction = 'DOWN'
    # if change_to == 'LEFT' and direction != 'RIGHT':
    #     direction = 'LEFT'
    # if change_to == 'RIGHT' and direction != 'LEFT':
    #     direction = 'RIGHT'
 
    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
 
    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()
         
    # similarly moving the adversaries 
    # if change_to1 == 'UP' and direction != 'DOWN':
    #     direction1 = 'UP'
    # if change_to1 == 'DOWN' and direction != 'UP':
    #     direction1 = 'DOWN'
    # if change_to1 == 'LEFT' and direction != 'RIGHT':
    #     direction1 = 'LEFT'
    # if change_to1 == 'RIGHT' and direction != 'LEFT':
    #     direction1 = 'RIGHT'

    if direction1 == 'UP':
        snake_1_position[1] -= 10
    if direction1 == 'DOWN':
        snake_1_position[1] += 10
    if direction1 == 'LEFT':
        snake_1_position[0] -= 10
    if direction1 == 'RIGHT':
        snake_1_position[0] += 10
 
    snake_1_body.insert(0, list(snake_1_position))
    if snake_1_position[0] == fruit_position[0] and snake_1_position[1] == fruit_position[1]:
        fruit_spawn = False
    else:
        snake_1_body.pop()
         
    # if change_to2 == 'UP' and direction != 'DOWN':
    #     direction2 = 'UP'
    # if change_to2 == 'DOWN' and direction != 'UP':
    #     direction2 = 'DOWN'
    # if change_to2 == 'LEFT' and direction != 'RIGHT':
    #     direction2 = 'LEFT'
    # if change_to2 == 'RIGHT' and direction != 'LEFT':
    #     direction2 = 'RIGHT'

    if direction2 == 'UP':
        snake_2_position[1] -= 10
    if direction2 == 'DOWN':
        snake_2_position[1] += 10
    if direction2 == 'LEFT':
        snake_2_position[0] -= 10
    if direction2 == 'RIGHT':
        snake_2_position[0] += 10
 
    snake_2_body.insert(0, list(snake_2_position))
    if snake_2_position[0] == fruit_position[0] and snake_2_position[1] == fruit_position[1]:
        fruit_spawn = False
    else:
        snake_2_body.pop()
         
    # if change_to3 == 'UP' and direction != 'DOWN':
    #     direction3 = 'UP'
    # if change_to3 == 'DOWN' and direction != 'UP':
    #     direction3 = 'DOWN'
    # if change_to3 == 'LEFT' and direction != 'RIGHT':
    #     direction3 = 'LEFT'
    # if change_to3 == 'RIGHT' and direction != 'LEFT':
    #     direction3 = 'RIGHT'

    if direction3 == 'UP':
        snake_3_position[1] -= 10
    if direction3 == 'DOWN':
        snake_3_position[1] += 10
    if direction3 == 'LEFT':
        snake_3_position[0] -= 10
    if direction3 == 'RIGHT':
        snake_3_position[0] += 10
 
    snake_3_body.insert(0, list(snake_3_position))
    if snake_3_position[0] == fruit_position[0] and snake_3_position[1] == fruit_position[1]:
        fruit_spawn = False
    else:
        snake_3_body.pop()
         
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10]
         
    fruit_spawn = True
    game_window.fill(black)
     
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))
 
    for pos in snake_1_body:
        pygame.draw.rect(game_window, blue,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    for pos in snake_2_body:
        pygame.draw.rect(game_window, red,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    for pos in snake_3_body:
        pygame.draw.rect(game_window, white,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()
 
    # similarly conditions for respawn for adversaries
    if snake_1_position[0] < 0 or snake_1_position[0] > window_x-10:
        respawn(snake_1_position,snake_1_body,snake_body,snake_2_body,snake_3_body,1)
    if snake_1_position[1] < 0 or snake_1_position[1] > window_y-10:
        respawn(snake_1_position,snake_1_body,snake_body,snake_2_body,snake_3_body,1)

    if snake_2_position[0] < 0 or snake_2_position[0] > window_x-10:
        respawn(snake_2_position,snake_2_body,snake_body,snake_1_body,snake_3_body,2)
    if snake_2_position[1] < 0 or snake_2_position[1] > window_y-10:
        respawn(snake_2_position,snake_2_body,snake_body,snake_1_body,snake_3_body,2)

    if snake_3_position[0] < 0 or snake_3_position[0] > window_x-10:
        respawn(snake_3_position,snake_3_body,snake_body,snake_2_body,snake_1_body,3)
    if snake_3_position[1] < 0 or snake_3_position[1] > window_y-10:
        respawn(snake_3_position,snake_3_body,snake_body,snake_2_body,snake_1_body,3)

    # omitting this part as this will be a multi-player game
    # Touching the snake body
    # for block in snake_body[1:]:
    #     if snake_position[0] == block[0] and snake_position[1] == block[1]:
    #         game_over()
 
    # if snake hits against an adversary's body then the game is over
    for block in snake_1_body:
         if snake_position[0] == block[0] and snake_position[1] == block[1]:
             game_over()

    for block in snake_2_body:
         if snake_position[0] == block[0] and snake_position[1] == block[1]:
             game_over()

    for block in snake_3_body:
         if snake_position[0] == block[0] and snake_position[1] == block[1]:
             game_over()

    # similarly for the adversary snakes as well. But the adversaries respawn with the initial length
    for block in snake_body:
         if snake_1_position[0] == block[0] and snake_1_position[1] == block[1]:
             respawn(snake_1_position,snake_1_body,snake_body,snake_2_body,snake_3_body,1)

    for block in snake_2_body:
         if snake_1_position[0] == block[0] and snake_1_position[1] == block[1]:
             respawn(snake_1_position,snake_1_body,snake_body,snake_2_body,snake_3_body,1)

    for block in snake_3_body:
         if snake_1_position[0] == block[0] and snake_1_position[1] == block[1]:
             respawn(snake_1_position,snake_1_body,snake_body,snake_2_body,snake_3_body,1)

    for block in snake_1_body:
         if snake_2_position[0] == block[0] and snake_2_position[1] == block[1]:
             respawn(snake_2_position,snake_2_body,snake_body,snake_1_body,snake_3_body,2)

    for block in snake_body:
         if snake_2_position[0] == block[0] and snake_2_position[1] == block[1]:
             respawn(snake_2_position,snake_2_body,snake_body,snake_1_body,snake_3_body,2)

    for block in snake_3_body:
         if snake_2_position[0] == block[0] and snake_2_position[1] == block[1]:
             respawn(snake_2_position,snake_2_body,snake_body,snake_1_body,snake_3_body,2)

    for block in snake_1_body:
         if snake_3_position[0] == block[0] and snake_3_position[1] == block[1]:
             respawn(snake_3_position,snake_3_body,snake_body,snake_2_body,snake_1_body,3)

    for block in snake_2_body:
         if snake_3_position[0] == block[0] and snake_3_position[1] == block[1]:
             respawn(snake_3_position,snake_3_body,snake_body,snake_2_body,snake_1_body,3)

    for block in snake_body:
         if snake_3_position[0] == block[0] and snake_3_position[1] == block[1]:
             respawn(snake_3_position,snake_3_body,snake_body,snake_2_body,snake_1_body,3)

    # displaying score continuously
    show_score(1, white, 'times new roman', 20)
 
    # Refresh game screen
    pygame.display.update()
 
    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
