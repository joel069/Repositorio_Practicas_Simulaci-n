from random import randrange 
import pygame

muertes = 5.0  
Factor_R0 = 4.0 
infeccion = Factor_R0 * 10
vacunas = 0 
filas = 20 
columnas = 20 
tiempoD = 100  

global display, myfont, states, states_temp 

ven1 = (255, 255, 255) 
ven2 = (220, 210, 255)
ven3 = (24, 29, 115)
ven4 = (168, 50, 58)

def comunidad(x, y):
    incx = randrange(3)
    incy = randrange(3)
    incx = (incx * 1) - 1
    incy = (incy * 1) - 1
    x2 = x + incx
    y2 = y + incy
    
    if x2 < 0:
        x2 = 0
    if x2 >= columnas:
        x2 = columnas - 1
    if y2 < 0:
        y2 = 0
    if y2 >= filas:
        y2 = filas - 1
    return [x2, y2]


def iniciarVacunacion():
    for x in range(columnas):
        for y in range(filas):
            if randrange(99) < vacunas:
                states[x][y] = 1


def fallecidos():
    contador = 0
    for x in range(columnas):
        for y in range(filas):
            if states[x][y] == -1:
                contador +=  1
    return contador


states = [[0] * columnas for i1 in range(filas)]
states_temp = states.copy()
states[randrange(20)][randrange(20)] = 10 
it = 0 
muertos = 0 
iniciarVacunacion() 

pygame.init() 
pygame.font.init() 
display=pygame.display.set_mode((400,350),0,32) 
pygame.display.set_caption("PROPAGACION COVID EN EL ECUADOR")
font=pygame.font.SysFont('italic', 40) 
display.fill(ven1) 

while True:
    pygame.time.delay(tiempoD) 
    it = it + 1
    if it <= 10000 and it >= 2:
        states_temp = states.copy() 
        for x in range(columnas):
            for y in range(filas):
                state = states[x][y]
                if state == -1:
                    pass
                if state >= 10: 
                    states_temp[x][y] = state + 1
                if state >= 20:
                    if randrange(99) < muertes: 
                        states_temp[x][y] = -1 
                    else:
                        states_temp[x][y] = 1
                if state >= 10 and state <= 20: 
                    if randrange(99) < infeccion: 
                        neighbour = comunidad(x, y) 
                        x2 = neighbour[0]
                        y2 = neighbour[1]
                        neigh_state = states[x2][y2]
                        if neigh_state == 0: 
                            states_temp[x2][y2] = 10 
        states = states_temp.copy()
        muertos = fallecidos() 
        
    pygame.draw.rect(display, ven1, (300, 30, 260, 50)) 
    textsurface = font.render("PERSONAS FALLECIDAS: "+ str(muertos),True, (195, 235, 234))
    display.blit(textsurface, (0, 0)) 
    for x in range(columnas):
        for y in range(filas):
            if states[x][y] == 0:
                color = ven2 
            if states[x][y] == 1:
                color = ven3 
            if states[x][y] >= 10:
                color = (states[x][y] * 12, 50, 50)
            if states[x][y] == -1:
                color = ven4 
            pygame.draw.circle(display, color, (100 + x * 12 + 5, 100 + y * 12 + 5), 5)
            pygame.draw.rect(display, ven1, (100 + x * 12 + 3, 100 + y * 12 + 4, 1, 1))
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
            pygame.quit() 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
            states = [[0] * columnas for i1 in range(filas)]
            states_temp = states.copy()
            states[5][5] = 10
            it = 0
            muertos = 0
            iniciarVacunacion() 
            
    pygame.display.update()