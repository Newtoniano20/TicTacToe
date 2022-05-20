import base64
import pygame
import os
import time
import requests
import json
from Assets import x, O, BG
pygame.font.init()
pygame.mixer.init()

with open('BG.png', 'wb+') as outputfile:
    outputfile.write(base64.b64decode(BG))
with open('O.png', 'wb+') as outputfile:
    outputfile.write(base64.b64decode(O))
with open('x.png', 'wb+') as outputfile:
    outputfile.write(base64.b64decode(x))

VERSUS = "VS: DANI"
BOARD = {
    1: (120, 40),
    2: (350, 40),
    3: (580, 40),
    4: (120, 186),
    5: (350, 186),
    6: (580, 186),
    7: (120, 332),
    8: (350, 332),
    9: (580, 332)
}
PROFILE = {
    "user": "MOLA",
    "match_id": None,
    "Match": None,
    "id": None
}

MAIN_URL = "https://tictactoe-newton.herokuapp.com"

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicTacToe")

BORDER = pygame.Rect(1, 0, 2, 1)
SPACE = pygame.transform.scale((pygame.image.load(os.path.join('BG.png'))), (WIDTH, HEIGHT))


X_IMAGE = pygame.transform.scale((pygame.image.load(os.path.join('x.png'))), (190, 130))
O_IMAGE = pygame.transform.scale((pygame.image.load(os.path.join('O.png'))), (200, 150))

FPS = 10
clock = pygame.time.Clock()

def set_text(string, coordx, coordy, fontSize): #Function to set text

    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, (0, 0, 0)) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)

def update_screen(CURRENT_GAME):
    WIN.blit(SPACE, (0, 0))
    totalText = set_text(VERSUS, 60, 60, 60)
    WIN.blit(totalText[0], totalText[1])
    for index, place in enumerate(CURRENT_GAME):
        if place == "x":
            WIN.blit(X_IMAGE, BOARD[index+1])
        if place == "o":
            WIN.blit(O_IMAGE, BOARD[index+1])
    pygame.draw.rect(WIN, (0,0,0), BORDER)
    pygame.display.update()

def server_login():
    return requests.post(url=MAIN_URL+"/auth", data=PROFILE).json()

def main():
    CURRENT_GAME = ["", "", "", "", "", "", "", "", ""]
    run = True
    IN_QUEUE = True
    PROFILE = server_login()
    while run:
        if IN_QUEUE:
            try:
                QUEUE_STATUS = json.loads(requests.get(str(MAIN_URL)+f"/queue/{PROFILE['id']}").content.decode('utf-8'))
            except:
                print("ERROR")
            print(QUEUE_STATUS, "\n")
            if QUEUE_STATUS["ingame"] == True:
                IN_QUEUE = False
        else:
            RESPONSE = json.loads(requests.get(str(MAIN_URL)+f"/game/{QUEUE_STATUS['match_id']}").content.decode('utf-8'))
            print(RESPONSE)
            CURRENT_GAME = RESPONSE["BOARD"] 
            update_screen(CURRENT_GAME)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for index in BOARD:
                        coords = BOARD[index]
                        if coords[0] < pos[0] < coords[0]+140 and coords[1] < pos[1] < coords[1]+200:
                            if not (CURRENT_GAME[index-1] == "x"):
                                TO_UPDATE = {
                                    "change": "x",
                                    "coords": index-1
                                }
                                requests.post(url=MAIN_URL+f"/Update/{QUEUE_STATUS['match_id']}", data=TO_UPDATE)
                                #CURRENT_GAME[index-1] = "x"
        clock.tick(FPS)    


if __name__ == "__main__":
    main()