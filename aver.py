import pygame
import sys
import random
import os

pygame.init()
pantalla = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Space Invaders - Juli Rossney")
reloj = pygame.time.Clock()

#fondo
tema_fondo = pygame.image.load("image.png").convert()
tema_fondo = pygame.transform.scale(tema_fondo, (400, 600))
y1 = 0
y2 = -600
velocidad_scroll = 1

#colores
BLANCO = (255, 255, 255)
ROSA = (255, 192, 203)
VIOLETA = (120, 0, 90)

#fuentes, titulo
fuente = pygame.font.SysFont("Arial", 32)
fuente_pixel = pygame.font.Font("pixel.ttf", 38)  

#botones menu
botonjugar = pygame.image.load("botonjugar.png")
botonjugar = pygame.transform.scale(botonjugar,(300, 100))
jugar = pygame.image.load("jugar.png")
jugar = pygame.transform.scale(jugar,(300, 100))
boton  = botonjugar.get_rect(topleft=(300, 100))

botonmulti = pygame.image.load("botonmulti.png")
botonmulti = pygame.transform.scale(botonmulti,(300, 100))
multi = pygame.image.load("multi.png")

botoncreditos = pygame.image.load("botoncreditos.png")
botoncreditos = pygame.transform.scale(botoncreditos,(300, 100))
creditos = pygame.image.load("creditos.png")

botontutorial = pygame.image.load("botontutorial.png")
botontutorial = pygame.transform.scale(botontutorial,(300, 100))
tutorial = pygame.image.load("tutorial.png")

botonsalir = pygame.image.load("botonsalir.png")
botonsalir = pygame.transform.scale(botonsalir,(300, 100))
salir = pygame.image.load("salir.png")

#jugador
nave_img = pygame.image.load("nave.png")
nave_img = pygame.transform.scale(nave_img, (60, 60))
nave_rect = nave_img.get_rect(center=(200, 550))

nave2_img = pygame.image.load("nave.png")
nave2_img = pygame.transform.scale(nave2_img, (60, 60))
nave2_rect = nave2_img.get_rect(center=(100, 550))
balas2 = [] 

#bala
bala_img = pygame.image.load("bala.png")
bala_img = pygame.transform.scale(bala_img, (10, 20))
balas = []
for bala in balas:
    pantalla.blit(bala_img, bala)


#bichos
enemigo_img = pygame.image.load("bicho.png")
enemigo_img = pygame.transform.scale(enemigo_img, (40, 40))
enemigos = []

#puntos
puntos = 0

#colores titulo cambiando
colores_titulo = [(255, 105, 180), (255, 182, 193), (255, 20, 147), (255, 192, 203)]
indice_color = 0
contador_cambio_color = 0

def boton_jugar(surface): 
    Posi_mouse = pygame.mouse.get_pos()
    if boton.collidepoint(Posi_mouse):
        surface.blit(botonjugar, boton.topleft)
    else:
        surface.blit(jugar, boton.topleft)

#fondo en movimiento
def mostrar_fondo():
    global y1, y2
    y1 += velocidad_scroll
    y2 += velocidad_scroll
    if y1 >= 600:
        y1 = -600
    if y2 >= 600:
        y2 = -600
    pantalla.blit(tema_fondo, (0, y1))
    pantalla.blit(tema_fondo, (0, y2))

def mostrar_texto(texto, x, y, color=BLANCO):
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))

#distribuir los bichos y su movimiento
def crear_enemigos():
    enemigos.clear()
    filas = 4
    columnas = 7
    espacio_horizontal = 20
    espacio_vertical = 20
    ancho_bicho = 30
    alto_bicho = 30

    for fila in range(filas):
        for columna in range(columnas):
            x = 30 + columna * (ancho_bicho + espacio_horizontal)
            y = 30 + fila * (alto_bicho + espacio_vertical)
            rect = enemigo_img.get_rect(topleft=(x, y))
            enemigos.append(rect)

def dibujar_enemigos():
    for enemigo in enemigos:
        pantalla.blit(enemigo_img, enemigo)

direccion = 1  
def mover_enemigos():
    global direccion
    mover_abajo = False

    for enemigo in enemigos:
        enemigo.x += direccion * 2
        if enemigo.right >= 400 or enemigo.left <= 0:
            mover_abajo = True

    if mover_abajo:
        direccion *= -1
        for enemigo in enemigos:
            enemigo.y += 10

def detectar_colisiones():
    global score
    for bala in balas[:]:
        for enemigo in enemigos[:]:
            if bala.colliderect(enemigo):
                balas.remove(bala)
                enemigos.remove(enemigo)
                score += 10
                break

def juego(modo):
    global balas, enemigos, score, balas2
    nave_rect.center = (200, 550)
    nave2_rect.center = (100, 550)
    balas = []
    balas2 = []
    enemigos = []
    score = 0
    crear_enemigos()

    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    bala_rect = bala_img.get_rect(center=(nave_rect.centerx, nave_rect.top))
                    balas.append(bala_rect)
                if modo == "multi" and evento.key == pygame.K_w:
                    bala2_rect = bala_img.get_rect(center=(nave2_rect.centerx, nave2_rect.top))
                    balas2.append(bala2_rect)

        teclas = pygame.key.get_pressed()

        # Movimiento J1 con límite
        if teclas[pygame.K_LEFT] and nave_rect.left > 0:
            nave_rect.x -= 5
        if teclas[pygame.K_RIGHT] and nave_rect.right < 400:
            nave_rect.x += 5

        # Movimiento J2 solo en modo multijugador y con límite
        if modo == "multi":
            if teclas[pygame.K_a] and nave2_rect.left > 0:
                nave2_rect.x -= 5
            if teclas[pygame.K_d] and nave2_rect.right < 400:
                nave2_rect.x += 5

        # Mover balas
        for bala in balas:
            bala.y -= 10
        for bala in balas2:
            bala.y -= 10
        balas[:] = [b for b in balas if b.y > 0]
        balas2[:] = [b for b in balas2 if b.y > 0]

        mover_enemigos()

        # Colisiones para ambos jugadores
        for lista_balas in [balas, balas2]:
            for bala in lista_balas[:]:
                for enemigo in enemigos[:]:
                    if bala.colliderect(enemigo):
                        lista_balas.remove(bala)
                        enemigos.remove(enemigo)
                        score += 10
                        break

        mostrar_fondo()
        pantalla.blit(nave_img, nave_rect)
        if modo == "multi":
            pantalla.blit(nave2_img, nave2_rect)
        for bala in balas:
            pantalla.blit(bala_img, bala)
        if modo == "multi":
            for bala in balas2:
                pantalla.blit(bala_img, bala)
        dibujar_enemigos()
        mostrar_texto(f"Puntaje: {score}", 10, 10)

        pygame.display.flip()
        reloj.tick(60)


def mostrar_tutorial():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

        mostrar_fondo()
        mostrar_texto("Tutorial:", 150, 200)
        mostrar_texto("Muevete con ← → y dispara con ESPACIO", 30, 250)
        mostrar_texto("Elimina a todos los aliens para ganar!", 30, 300)
        mostrar_texto("Presiona cualquier tecla para volver", 30, 400)
        pygame.display.flip()
        reloj.tick(60)

def mostrar_creditos():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

        mostrar_fondo()
        mostrar_texto("Space Invaders - Juli 2025 ", 100, 300)
        mostrar_texto("Hecho con amor y pygame 💖", 100, 350)
        mostrar_texto("Presiona cualquier tecla para salir", 60, 450)
        pygame.display.flip()
        reloj.tick(60)

def menu():
    global indice_color, contador_cambio_color
    opciones = [
        ("solo", botonjugar),
        ("multi", botonmulti),
        ("tutorial", botontutorial),
        ("creditos", botoncreditos),
        ("salir", botonsalir),
    ]
    botones = []
    for i, (accion, img) in enumerate(opciones):
        rect = img.get_rect(topleft=(50, 150 + i * 80))
        botones.append((accion, img, rect))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for accion, _, rect in botones:
                    if rect.collidepoint(x, y):
                        if accion == "solo":
                            juego("solo")
                        elif accion == "multi":
                            juego("multi")
                        elif accion == "tutorial":
                            mostrar_tutorial()
                        elif accion == "creditos":
                            mostrar_creditos()
                        elif accion == "salir":
                            pygame.quit()
                            sys.exit()

        mostrar_fondo()

        contador_cambio_color += 1
        if contador_cambio_color > 30:
            contador_cambio_color = 0
            indice_color = (indice_color + 1) % len(colores_titulo)
        t1 = fuente_pixel.render("SPACE", True, colores_titulo[indice_color])
        t2 = fuente_pixel.render("INVADERS", True, colores_titulo[indice_color])
        pantalla.blit(t1, (200 - t1.get_width()//2, 50))
        pantalla.blit(t2, (200 - t2.get_width()//2, 100))

        for _, img, rect in botones:
            pantalla.blit(img, rect)

        pygame.display.flip()
        reloj.tick(60)


menu() 