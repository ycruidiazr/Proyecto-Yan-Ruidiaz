
#Importamos las librerias de pygame y el motor de ajedrez
import pygame as p
from Chess import ChessEngine
#Se establece las dimensiones del tablero
WIDTH = HEIGHT = 512
DIMENSION = 8 #Tamaño del tablero
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #Para animaciones
IMAGES ={}

#Diccionario para llamar las imagenes de la piezas
def loadImages():
    pieces = ['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


#Función que toma las funciones de dibujo para crear el juego, incluye los comandos para poder mover las piezas
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    runnig = True
    sqSelected = ()
    playerClicks = []
    while runnig:
        for e in p.event.get():
            if e.type == p.QUIT:
                runnig = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #la posición será la misma del mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


#Dibujo del tablero de Ajedrez
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


#Dibuja los cuadros del tablero
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#Dibujo piezas
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__  == "__main__":
    main()

