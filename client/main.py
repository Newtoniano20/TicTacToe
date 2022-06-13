import base64
import pygame
import os
import sys
import requests
import json
import time
from Assets import x, O, BG
pygame.font.init()
pygame.mixer.init()

with open('BG.png', 'wb+') as outputfile:
    outputfile.write(base64.b64decode(BG))
with open('O.png', 'wb+') as outputfile:
    outputfile.write(base64.b64decode(O))
with open('x.png', 'wb+') as outputfile:
    outputfile.write(base64.b64decode(x))

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
CHANGE = ""
MAIN_URL = "https://tictactoe-newton-europe.herokuapp.com"
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicTacToe")

BORDER = pygame.Rect(1, 0, 2, 1)
SPACE = pygame.transform.scale((pygame.image.load(os.path.join('BG.png'))), (WIDTH, HEIGHT))
X_IMAGE = pygame.transform.scale((pygame.image.load(os.path.join('x.png'))), (190, 130))
O_IMAGE = pygame.transform.scale((pygame.image.load(os.path.join('O.png'))), (200, 150))

FPS = 60
clock = pygame.time.Clock()

def set_text(string, coordx, coordy, fontSize): #Function to set text

    font = pygame.font.SysFont('Arial', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, (0, 0, 0)) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)
def INQUEUE_SCREEN():
    WIN.blit(SPACE, (0, 0))
    totalText = set_text("IN QUEUE", WIDTH/2, HEIGHT/2, 60)
    WIN.blit(totalText[0], totalText[1])
    pygame.display.update()

def IF_ENDED(text):
    WIN.blit(SPACE, (0, 0))
    totalText = set_text(text, WIDTH/2, HEIGHT/2, 60)
    WIN.blit(totalText[0], totalText[1])
    pygame.display.update()

def update_screen(CURRENT_GAME, VERSUS):
    WIN.blit(SPACE, (0, 0))
    totalText = set_text(VERSUS, 50, 10, 20)
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

def server_ask(QUEUE_STATUS):
    RESPONSE = json.loads(requests.get(str(MAIN_URL)+f"/game/{QUEUE_STATUS['match_id']}").content.decode('utf-8'))
    return RESPONSE, RESPONSE["BOARD"]

def main():
    CURRENT_GAME = ["", "", "", "", "", "", "", "", ""]
    IN_QUEUE = True
    PROFILE = server_login()
    if int(PROFILE["id"]) % 2 == 0:
        CHANGE="x"
    else:
        CHANGE="o"
    while True:
        if IN_QUEUE:
            INQUEUE_SCREEN()
            try:
                QUEUE_STATUS = json.loads(requests.get(str(MAIN_URL)+f"/queue/{PROFILE['id']}").content.decode('utf-8'))
            except:
                print("ERROR")
            print(QUEUE_STATUS, "\n")
            if QUEUE_STATUS["ingame"] == True:
                RESPONSE, CURRENT_GAME = server_ask(QUEUE_STATUS)
                IN_QUEUE = False
                if RESPONSE['P1']['Username'] == PROFILE['Username']:
                    VS_PLAYER = RESPONSE['P2']['Username']
                else:
                    VS_PLAYER = RESPONSE['P1']['Username']
                VERSUS = f"VS: {VS_PLAYER}"
        else:                
            RESPONSE, CURRENT_GAME = server_ask(QUEUE_STATUS)
            if RESPONSE["WON"] == CHANGE:
                IF_ENDED("YOU WON")
                time.sleep(2)
                break

            elif RESPONSE["WON"] != None and RESPONSE["WON"] != "":
                IF_ENDED("YOU LOST")
                time.sleep(2)
                break
            else:
                update_screen(CURRENT_GAME, VERSUS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        for index in BOARD:
                            coords = BOARD[index]
                            if coords[0] < pos[0] < coords[0]+140 and coords[1] < pos[1] < coords[1]+200:
                                if not (CURRENT_GAME[index-1] == "x" or CURRENT_GAME[index-1] == "o"):
                                    TO_UPDATE = {
                                        "change": CHANGE,
                                        "coords": index-1
                                    }
                                    requests.post(url=MAIN_URL+f"/Update/{QUEUE_STATUS['match_id']}", data=TO_UPDATE)
        clock.tick(FPS)    


if __name__ == "__main__":
    while True:
        main()
