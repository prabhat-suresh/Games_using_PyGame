import pygame

pygame.init()

SCREEN_WIDTH=600
SCREEN_HEIGHT=700

gap=SCREEN_WIDTH/9

sudoku=[
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        ]

white=pygame.Color(255,255,255)
black=pygame.Color(0,0,0)
red=pygame.Color(255,0,0)
green=pygame.Color(0,255,0)
dark_purple=pygame.Color(135, 31, 120)
yellow=pygame.Color(255,255,0)

screen=pygame.display.set_mode((SCREEN_WIDTH+2,SCREEN_HEIGHT))

pygame.display.set_caption('Sudoku Solver')

font1 = pygame.font.SysFont("calibri", 50)
font2 = pygame.font.SysFont("calibri", 20)

curr_mouse_x=0
curr_mouse_y=0

def is_invalid_puzzle():
    row,col,grid=[],[],[]
    for i in range(9):
        temp1,temp2,temp3=[],[],[]
        for j in range(9):
            temp1.append(False);
            temp2.append(False);
            temp3.append(False);
        row.append(temp1)
        col.append(temp2)
        grid.append(temp3)

    for i in range(9):
        for j in range(9):
            if sudoku[i][j]:
                if row[i][sudoku[i][j]-1]:
                    return True
                else:
                    row[i][sudoku[i][j]-1]=True
                if col[j][sudoku[i][j]-1]:
                    return True
                else:
                    col[j][sudoku[i][j]-1]=True
                if grid[i//3*3+j//3][sudoku[i][j]-1]:
                    return True
                else:
                    grid[i//3*3+j//3][sudoku[i][j]-1]=True
    return False

def is_move_safe(cell_x,cell_y,num):
    for i in range(9):
        if sudoku[cell_x][i]==num:
            return False
        if sudoku[i][cell_y]==num:
            return False

    for i in range((cell_x//3)*3,(cell_x//3)*3+3):
        for j in range((cell_y//3)*3,(cell_y//3)*3+3):
            if sudoku[i][j]==num:
                return False
    return True

def solve(cell_x,cell_y):
    if cell_x==8 and cell_y==9:
        return True
    if cell_y==9:
        cell_y=0
        cell_x+=1
    if sudoku[cell_x][cell_y]:
        return solve(cell_x,cell_y+1)
    for num in range(1,10):
        if is_move_safe(cell_x,cell_y,num):
            sudoku[cell_x][cell_y]=num
            if solve(cell_x,cell_y+1):
                return True
            sudoku[cell_x][cell_y]=0
    return False

def draw_sudoku():
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]:
                pygame.draw.rect(screen,dark_purple,pygame.Rect(i*gap,j*gap,gap+1,gap+1))
                text1=font1.render(str(sudoku[i][j]),True,white)
                screen.blit(text1,(i*gap+18,j*gap+10))

    for i in range(10):
        wide=1
        if i%3==0:
            wide=3
        pygame.draw.line(screen,white,(0,i*gap),(SCREEN_WIDTH,i*gap),width=wide)
        pygame.draw.line(screen,white,(i*gap,0),(i*gap,SCREEN_WIDTH),width=wide)

    pygame.draw.line(screen,yellow,(curr_mouse_x*gap,curr_mouse_y*gap),(curr_mouse_x*gap+gap,curr_mouse_y*gap),width=3)
    pygame.draw.line(screen,yellow,(curr_mouse_x*gap,curr_mouse_y*gap),(curr_mouse_x*gap,curr_mouse_y*gap+gap),width=3)
    pygame.draw.line(screen,yellow,(curr_mouse_x*gap+gap,curr_mouse_y*gap),(curr_mouse_x*gap+gap,curr_mouse_y*gap+gap),width=3)
    pygame.draw.line(screen,yellow,(curr_mouse_x*gap,curr_mouse_y*gap+gap),(curr_mouse_x*gap+gap,curr_mouse_y*gap+gap),width=3)

    text2=font2.render("Press 's' for the solution and 'r' for reset" ,True,green)
    text3=font2.render("Press values 1-9 and backspace for removing a value",True,green)
    screen.blit(text2,(20,610))
    screen.blit(text3,(20,650))

while True:
    screen.fill(black)
    draw_sudoku()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            curr_mouse_x=(int)(pos[0]//gap)
            curr_mouse_y=(int)(pos[1]//gap)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                curr_mouse_x-=1
            if event.key==pygame.K_RIGHT:
                curr_mouse_x+=1
            if event.key==pygame.K_DOWN:
                curr_mouse_y+=1
            if event.key==pygame.K_UP:
                curr_mouse_y-=1
            if event.key==pygame.K_BACKSPACE:
                sudoku[curr_mouse_x][curr_mouse_y]=0
            if event.key==pygame.K_1:
                sudoku[curr_mouse_x][curr_mouse_y]=1
            if event.key==pygame.K_2:
                sudoku[curr_mouse_x][curr_mouse_y]=2
            if event.key==pygame.K_3:
                sudoku[curr_mouse_x][curr_mouse_y]=3
            if event.key==pygame.K_4:
                sudoku[curr_mouse_x][curr_mouse_y]=4
            if event.key==pygame.K_5:
                sudoku[curr_mouse_x][curr_mouse_y]=5
            if event.key==pygame.K_6:
                sudoku[curr_mouse_x][curr_mouse_y]=6
            if event.key==pygame.K_7:
                sudoku[curr_mouse_x][curr_mouse_y]=7
            if event.key==pygame.K_8:
                sudoku[curr_mouse_x][curr_mouse_y]=8
            if event.key==pygame.K_9:
                sudoku[curr_mouse_x][curr_mouse_y]=9
            if event.key==pygame.K_r:
                sudoku=[
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        ]
            if event.key==pygame.K_s:
                if is_invalid_puzzle() or not solve(0,0):
                    pygame.draw.rect(screen,white,pygame.Rect(gap,3*gap,7*gap,3*gap))
                    text4=font1.render("Invalid Puzzle!",True,red)
                    textRect=text4.get_rect()
                    textRect.center=(SCREEN_WIDTH//2,SCREEN_WIDTH//2)
                    screen.blit(text4,textRect)
                    pygame.display.update()
                    pygame.time.delay(2000)

    pygame.display.update()
