import socket as cock
import pygame
import menu

HOST = "didas72.hopto.org"
PORT = 5055

CurrentWave = "99"
Name = "Gui"

pygame.font.init()
font = pygame.font.SysFont(None, 32)

def sqr(x,y,w,h,text,background, Color):
    pygame.draw.rect(background,(100,100,100),((x,y),(w,h)))
    pygame.draw.rect(background,Color,((x+2,y+2),(w-4,h-4)))
    img = font.render(str(text), True, pygame.Color(255,255,255));img_sqr = img.get_rect();img_sqr.center = (x+w/2, y+h/2)
    background.blit(img,img_sqr)

def Try_Add_To_Leaderboard(CurrentWave, Name):
    ToSendMail=[str(CurrentWave), str(Name)]
    for x in range(len(ToSendMail)):
        ToSendMail[x] = ToSendMail[x] + "\a"

    with cock.socket(cock.AF_INET, cock.SOCK_STREAM) as socks:
        socks.connect((HOST,PORT))

        mail = ""
        for i in ToSendMail:
            mail = mail + i
        socks.sendall(bytes(mail, "ascii"))

        data = socks.recv(1024);data = str(data)

        data_list = data.split("\\x07");data_list.pop()
        data_list[0] = data_list[0].removeprefix("b'")

        Leaderboards_W, Leaderboards_N = [] , []
        for x in data_list:
            try: Leaderboards_W.append(int(x))
            except: Leaderboards_N.append(x)
    
    return Leaderboards_W, Leaderboards_N

tryMore = True
Leaderboards_W, Leaderboards_N = [] , []
def Leader_Boards_Draw(background):
    global Leaderboards_W
    global Leaderboards_N
    global tryMore
    if menu.Ldo:
        if tryMore:
            try:
                Leaderboards_W, Leaderboards_N = Try_Add_To_Leaderboard(0,"-")
            except:
                tryMore = False
                return
        else:
            sqr(225, 275, 450, 50, "Failed to connect to server.", background, (0,0,0))
            return
        menu.Ldo=False

    for i in range(10):
        sqr(120,i*42+100,50,40,i+1,background, (255,212,66))


    for i in range(len(Leaderboards_W)):
        sqr(175,i*42+100,100,40,Leaderboards_W[i],background, (255,212,66))
        

    for i in range(len(Leaderboards_W)):
        sqr(280,i*42+100,500,40,Leaderboards_N[i],background, (255,212,66))
