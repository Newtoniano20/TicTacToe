import pygame
import os
pygame.font.init()
pygame.mixer.init()

CURRENT_GAME = ["", "", "", "", "", "", "", "", ""]
BOARD = {
    1: (120, 40),
    2: (350, 40),
    3: (580, 40),
    4: (120, 186),
    5: (350, 186),
    6: (580, 186),
    7: (120, 332),
    8: (350, 332),
    9: (580, 332),
}
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicTacToe")

BORDER = pygame.Rect(1, 0, 2, 1)
SPACE = pygame.transform.scale((pygame.image.load(os.path.join('client','Assets', 'BG.png'))), (WIDTH, HEIGHT))


X_IMAGE = pygame.transform.scale((pygame.image.load(os.path.join('client','Assets', 'x.png'))), (190, 130))
O_IMAGE = pygame.transform.scale((pygame.image.load(os.path.join('client','Assets', 'O.png'))), (200, 150))

FPS = 60
clock = pygame.time.Clock()

def update_screen():
    WIN.blit(SPACE, (0, 0))
    for index, place in enumerate(CURRENT_GAME):
        if place == "x":
            WIN.blit(X_IMAGE, BOARD[index+1])
        if place == "o":
            WIN.blit(O_IMAGE, BOARD[index+1])
    pygame.draw.rect(WIN, (0,0,0), BORDER)
    pygame.display.update()

def server():
    pass

def main():
    run = True
    while run:
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