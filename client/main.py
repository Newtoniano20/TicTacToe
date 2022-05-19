import pygame
import os
import time
import requests
pygame.font.init()
pygame.mixer.init()

CURRENT_GAME = ["", "", "", "", "", "", "", "", ""]
VERSUS = ""
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

MAIN_URL = "http://localhost:3000"

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicTacToe")

BORDER = pygame.Rect(1, 0, 2, 1)
SPACE = pygame.transform.scale((pygame.image.load(os.path.join('client','Assets', 'BG.png'))), (WIDTH, HEIGHT))


X_IMAGE = pygame.transform.scale((pygame.image.load(os.path.join('client','Assets', 'x.png'))), (190, 130))
O_IMAGE = pygame.transform.scale((pygame.image.load(os.path.join('client','Assets', 'O.png'))), (200, 150))

FPS = 60
clock = pygame.time.Clock()

def set_text(string, coordx, coordy, fontSize): #Function to set text

    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, (0, 0, 0)) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)

def update_screen():
    WIN.blit(SPACE, (0, 0))
    totalText = set_text(VERSUS, 0, 0, 60)
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
    run = True
    IN_QUEUE = True
    PROFILE = server_login()
    while run:
        if IN_QUEUE:
            time.sleep(1)
            QUEUE_STATUS = requests.get(str(MAIN_URL)+f"/queue/{PROFILE['id']}").content
            print(QUEUE_STATUS, "\n")
        clock.tick(FPS)
        update_screen()
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
                            print(True)
                            CURRENT_GAME[index-1] = "x"


if __name__ == "__main__":
    main()