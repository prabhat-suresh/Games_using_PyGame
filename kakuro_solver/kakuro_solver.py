import pygame

pygame.init()
num_rows=int(input("Enter no. of rows"))
num_cols=int(input("Enter no. of columns"))

class cell:
    def __init__(self):
        self.vertical_sum=0
        self.horizontal_sum=0
        self.val=0
        self.to_fill_vertical_sum=False

kakuro=[]
for i in range(num_rows+1):
    temp=[]
    for j in range(num_cols+1):
        temp.append(cell())
    kakuro.append(temp)

gap=30
SCREEN_WIDTH=gap*num_cols
SCREEN_HEIGHT=gap*num_rows

white=pygame.Color(255,255,255)
black=pygame.Color(0,0,0)
red=pygame.Color(255,0,0)

screen=pygame.display.set_mode((SCREEN_WIDTH+2,SCREEN_HEIGHT))

pygame.display.set_caption('Kakuro Solver')

font1 = pygame.font.SysFont("calibri", 15)
font2 = pygame.font.SysFont("calibri", 20)

curr_mouse_x=0
curr_mouse_y=0

def is_move_ok(i,j,num):
    rowval,colval=[],[]
    for p in range(10):
        rowval.append(True)
        colval.append(True)

    rowval[num],rowval[0],colval[num],colval[0]=False,False,False,False

    k=i-1
    while k and kakuro[k][j].val!=-1:
        if colval[kakuro[k][j].val]:
            colval[kakuro[k][j].val]=False
        else:
            return False
        k-=1

    k=j-1
    while k and kakuro[i][k].val!=-1:
        if rowval[kakuro[i][k].val]:
            rowval[kakuro[i][k].val]=False
        else:
            return False
        k-=1

    row_num_empty,col_num_empty,minrsum,mincsum,maxrsum,maxcsum=0,0,0,0,0,0

    while j+1+row_num_empty<=num_cols and kakuro[i][j+1+row_num_empty].val!=-1:
        row_num_empty+=1
    while i+1+col_num_empty<=num_rows and kakuro[i+1+col_num_empty][j].val!=-1:
        col_num_empty+=1

    temp,k=0,1
    while k<10 and temp<row_num_empty:
        if rowval[k]:
            minrsum+=k
            temp+=1
        k+=1

    temp,k=0,1
    while k<10 and temp<col_num_empty:
        if colval[k]:
            mincsum+=k
            temp+=1
        k+=1

    temp,k=0,9
    while k and temp<row_num_empty:
        if rowval[k]:
            maxrsum+=k
            temp+=1
        k-=1

    temp,k=0,9
    while k and temp<col_num_empty:
        if colval[k]:
            maxcsum+=k
            temp+=1
        k-=1

    if minrsum+num>kakuro[i][j-1].horizontal_sum or kakuro[i][j-1].horizontal_sum<100 and maxrsum+num<kakuro[i][j-1].horizontal_sum:
        return False
    
    if mincsum+num>kakuro[i-1][j].vertical_sum or kakuro[i-1][j].vertical_sum <100 and maxcsum+num<kakuro[i-1][j].vertical_sum:
        return False
    
    return True

def solve(i,j):
    if i==num_rows and j==num_cols+1:
        return True
    if j==num_cols+1:
        j=1
        i+=1
    if kakuro[i][j].val==-1:
        return solve(i,j+1)
    for num in range(1,10):
        if is_move_ok(i,j,num):
            kakuro[i][j].val=num
            kakuro[i][j].vertical_sum=kakuro[i-1][j].vertical_sum-num
            kakuro[i][j].horizontal_sum=kakuro[i][j-1].horizontal_sum-num
            if solve(i,j+1):
                return True
            kakuro[i][j].val=0
    return False

def draw_kakuro():
    for i in range(num_rows):
        for j in range(num_cols):
            if kakuro[i+1][j+1].val==-1:
                pygame.draw.rect(screen,black,pygame.Rect(j*gap,i*gap,gap+1,gap+1))
                pygame.draw.line(screen,white,(j*gap,i*gap),(j*gap+gap+1,i*gap+gap+1))

                if kakuro[i+1][j+1].vertical_sum>0 and kakuro[i+1][j+1].vertical_sum<100:
                    text1=font1.render(str(kakuro[i+1][j+1].vertical_sum),True,white)
                    screen.blit(text1,(j*gap+5,i*gap+10))

                if kakuro[i+1][j+1].horizontal_sum>0 and kakuro[i+1][j+1].horizontal_sum<100:
                    text2=font1.render(str(kakuro[i+1][j+1].horizontal_sum),True,white)
                    screen.blit(text2,(j*gap+15,i*gap))
            else:
                text1=font2.render(str(kakuro[i+1][j+1].val),True,black)
                screen.blit(text1,(j*gap+10,i*gap+5))

    for i in range(num_rows+1):
        pygame.draw.line(screen,black,(0,i*gap),(SCREEN_WIDTH,i*gap),width=2)
    for i in range(num_cols+1):
        pygame.draw.line(screen,black,(i*gap,0),(i*gap,SCREEN_HEIGHT),width=2)

    pygame.draw.line(screen,red,(curr_mouse_y*gap,curr_mouse_x*gap),(curr_mouse_y*gap+gap,curr_mouse_x*gap),width=3)
    pygame.draw.line(screen,red,(curr_mouse_y*gap,curr_mouse_x*gap),(curr_mouse_y*gap,curr_mouse_x*gap+gap),width=3)
    pygame.draw.line(screen,red,(curr_mouse_y*gap+gap,curr_mouse_x*gap),(curr_mouse_y*gap+gap,curr_mouse_x*gap+gap),width=3)
    pygame.draw.line(screen,red,(curr_mouse_y*gap,curr_mouse_x*gap+gap),(curr_mouse_y*gap+gap,curr_mouse_x*gap+gap),width=3)

    # text2=font2.render("Press 's' for the solution and 'r' for reset" ,True,green)
    # text3=font2.render("Press values 1-9 and backspace for removing a value",True,green)
    # screen.blit(text2,(20,610))
    # screen.blit(text3,(20,650))

while True:
    screen.fill(white)
    draw_kakuro()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            curr_mouse_y=(int)(pos[0]//gap)
            curr_mouse_x=(int)(pos[1]//gap)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                curr_mouse_y-=1
            if event.key==pygame.K_RIGHT:
                curr_mouse_y+=1
            if event.key==pygame.K_DOWN:
                curr_mouse_x+=1
            if event.key==pygame.K_UP:
                curr_mouse_x-=1
            if event.key==pygame.K_0:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum*=10 
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum*=10 
            if event.key==pygame.K_1:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=1+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=1+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum
            if event.key==pygame.K_2:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=2+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=2+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum
            if event.key==pygame.K_3:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=3+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=3+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum
            if event.key==pygame.K_4:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=4+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=4+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum
            if event.key==pygame.K_5:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=5+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=5+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum
            if event.key==pygame.K_6:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=6+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=6+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum
            if event.key==pygame.K_7:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=7+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=7+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum
            if event.key==pygame.K_8:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=8+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=8+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum
            if event.key==pygame.K_9:
                if kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=9+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum
                else:
                    kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=9+10*kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum
            if event.key==pygame.K_b:
                kakuro[curr_mouse_x+1][curr_mouse_y+1].val=-1
                for i in range(num_rows+1):
                    for j in range(num_cols+1):
                        print(kakuro[i][j].vertical_sum,' ',kakuro[i][j].horizontal_sum,end=' ')
                    print()
                print()
            if event.key==pygame.K_w:
                kakuro[curr_mouse_x+1][curr_mouse_y+1].val=0
                kakuro[curr_mouse_x+1][curr_mouse_y+1].vertical_sum=0
                kakuro[curr_mouse_x+1][curr_mouse_y+1].horizontal_sum=0
            if event.key==pygame.K_RETURN:
                kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum = not kakuro[curr_mouse_x+1][curr_mouse_y+1].to_fill_vertical_sum
            if event.key==pygame.K_s:
                for i in range(num_rows+1):
                    kakuro[i][0].val=-1;
                    kakuro[i][0].vertical_sum=10000;
                    kakuro[i][0].horizontal_sum=10000;

                for i in range(1,num_cols+1):
                    kakuro[0][i].val=-1;
                    kakuro[0][i].vertical_sum=10000;
                    kakuro[0][i].horizontal_sum=10000;

                for i in range(1,num_rows+1):
                    for j in range(1,num_cols+1):
                        if kakuro[i][j].val==-1:
                            if kakuro[i][j].horizontal_sum==0:
                                kakuro[i][j].horizontal_sum=10000
                            if kakuro[i][j].vertical_sum==0:
                                kakuro[i][j].vertical_sum=10000
                solve(1,1)

    pygame.display.update()
