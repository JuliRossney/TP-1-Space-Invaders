import pygame
import sys
import random
import os

# ventana
pygame.init()
pantalla = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Space Invaders - Juli Rossney")
reloj = pygame.time.Clock()

# fondo del juego, infinito, velocidad del fondo
tema_fondo = pygame.image.load("image.png").convert()
tema_fondo = pygame.transform.scale(tema_fondo, (400, 600))
y1 = 0
y2 = -600
velocidad_scroll = 1

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

# colores, textos
BLANCO = (255, 255, 255)
ROSA = (213, 56, 126)
VIOLETA = (120, 0, 90)

# fuentes, título
#fuente = pygame.font.SysFont("Arial", 32)
fuente_pixel = pygame.font.Font("pixel.ttf", 38)
fuente_p = pygame.font.Font("pixel.ttf", 20)
fuente_tutorial = pygame.font.Font("pixel.ttf", 14)

# botones menú
botonjugar = pygame.image.load("botonjugar.png")
botonjugar = pygame.transform.scale(botonjugar, (300, 100))

botonmulti = pygame.image.load("botonmulti.png")
botonmulti = pygame.transform.scale(botonmulti, (300, 100))

botoncreditos = pygame.image.load("botoncreditos.png")
botoncreditos = pygame.transform.scale(botoncreditos, (300, 100))

botontutorial = pygame.image.load("botontutorial.png")
botontutorial = pygame.transform.scale(botontutorial, (300, 100))

botonsalir = pygame.image.load("botonsalir.png")
botonsalir = pygame.transform.scale(botonsalir, (300, 100))

# naves
nave_img = pygame.image.load("nave.png")
nave_img = pygame.transform.scale(nave_img, (60, 60))
nave_rect = nave_img.get_rect(center=(200, 550))

nave2_img = pygame.image.load("nave.png")
nave2_img = pygame.transform.scale(nave2_img, (60, 60))
nave2_rect = nave2_img.get_rect(center=(100, 550))

# bala
bala_img = pygame.image.load("bala.png")
bala_img = pygame.transform.scale(bala_img, (10, 20))
balas = []
balas2 = []

# bichos
enemigo_img = pygame.image.load("bicho.png")
enemigo_img = pygame.transform.scale(enemigo_img, (32, 32))
enemigos = []
balas_enemigas = []  # balas disparadas por los aliens
velocidad_bala_enemiga = 2

# puntos
puntos = 0

# colores título cambiando
colores_titulo = [(255, 105, 180), (255, 182, 193), (255, 20, 147), (255, 192, 203)]
indice_color = 0
contador_cambio_color = 0

def mostrar_texto(texto, x, y, color=ROSA):
    render = fuente_tutorial.render(texto, True, color)
    pantalla.blit(render, (x, y))

# distribuir los bichos y su movimiento
def crear_enemigos():
    enemigos.clear()
    filas = 4
    columnas = 7
    espacio_horizontal = 18
    espacio_vertical = 18
    ancho_bicho = 32
    alto_bicho = 32

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

# disparo de los enemigos
def disparar_enemigos():
    for enemigo in enemigos:
        if random.random() < 0.0005:  # probabilidad de disparo de cada alien
            bala_enemiga = bala_img.get_rect(center=(enemigo.centerx, enemigo.bottom))
            balas_enemigas.append(bala_enemiga)

# mover las balas de los enemigos
def mover_balas_enemigas():
    global puntos
    for bala in balas_enemigas[:]:
        bala.y += velocidad_bala_enemiga
        if bala.y > 600:  # si la bala se sale de la pantalla, la eliminamos
            balas_enemigas.remove(bala)

# detectar colisiones
def detectar_colisiones():
    global puntos
    for bala in balas[:]:
        for enemigo in enemigos[:]:
            if bala.colliderect(enemigo):
                balas.remove(bala)
                enemigos.remove(enemigo)
                puntos += 10
                break

    for bala in balas_enemigas[:]:
        if nave_rect.colliderect(bala.inflate(-6, -6)):
            return "game_over"

    return "jugando"

def juego(modo):
    global balas, balas2, enemigos, balas_enemigas, puntos
    # Reposición inicial
    nave_rect.center = (200, 550)
    nave2_rect.center = (100, 550)
    balas, balas2, balas_enemigas, enemigos = [], [], [], []
    puntos = 0
    crear_enemigos()

    while True:
        # — Eventos y disparos —
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    balas.append(bala_img.get_rect(center=(nave_rect.centerx, nave_rect.top)))
                if modo == "multi" and evento.key == pygame.K_w:
                    balas2.append(bala_img.get_rect(center=(nave2_rect.centerx, nave2_rect.top)))

        # — Movimiento de naves —
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_rect.left > 0:
            nave_rect.x -= 5
        if teclas[pygame.K_RIGHT] and nave_rect.right < 400:
            nave_rect.x += 5
        if modo == "multi":
            if teclas[pygame.K_a] and nave2_rect.left > 0:
                nave2_rect.x -= 5
            if teclas[pygame.K_d] and nave2_rect.right < 400:
                nave2_rect.x += 5

        # — Mover balas propias —
        for b in balas:   b.y -= 10
        for b in balas2:  b.y -= 10
        balas  = [b for b in balas  if b.y > 0]
        balas2 = [b for b in balas2 if b.y > 0]

        # — Enemigos disparan y se mueven —
        mover_enemigos()
        disparar_enemigos()
        mover_balas_enemigas()

        # — 1) Si un alien cruza la Y de tu nave → Game Over —
        for e in enemigos:
            if e.bottom >= nave_rect.top:
                mostrar_fondo()
                t1 = fuente_p.render("GAME OVER", True, ROSA)
                t2 = fuente_p.render(f"PUNTAJE FINAL: {puntos}", True, ROSA)
                x1 = (400 - t1.get_width()) // 2
                x2 = (400 - t2.get_width()) // 2
                pantalla.blit(t1, (x1, 250))
                pantalla.blit(t2, (x2, 300))
                pygame.display.flip()
                pygame.time.wait(2000)
                return

        # — 2) Si no quedan enemigos → Game Over —
        if not enemigos:
            mostrar_fondo()
            t1 = fuente_pixel.render("GAME OVER", True, ROSA)
            t2 = fuente_pixel.render(f"PUNTAJE FINAL: {puntos}", True, ROSA)
            x1 = (400 - t1.get_width()) // 2
            x2 = (400 - t2.get_width()) // 2
            pantalla.blit(t1, (x1, 250))
            pantalla.blit(t2, (x2, 300))
            pygame.display.flip()
            pygame.time.wait(2000)
            return

        # — 3) Colisiones bala→enemigo y bala_enemiga→nave —
        estado = detectar_colisiones()
        if estado == "game_over":
            mostrar_fondo()
            t1 = fuente_p.render("GAME OVER", True, ROSA)
            t2 = fuente_p.render(f"PUNTAJE FINAL: {puntos}", True, ROSA)
            x1 = (400 - t1.get_width()) // 2
            x2 = (400 - t2.get_width()) // 2
            pantalla.blit(t1, (x1, 250))
            pantalla.blit(t2, (x2, 300))
            pygame.display.flip()
            pygame.time.wait(2000)
            return

        # — Dibujado final de frame —
        mostrar_fondo()
        pantalla.blit(nave_img, nave_rect)
        if modo == "multi":
            pantalla.blit(nave2_img, nave2_rect)
        for b in balas + balas2 + balas_enemigas:
            pantalla.blit(bala_img, b)
        dibujar_enemigos()
        punt_text = fuente_p.render(f"PUNTAJE: {puntos}", True, ROSA)
        pantalla.blit(punt_text, (10, 10))

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
        mostrar_texto("TUTORIAL:", 150, 180)
        mostrar_texto("- Movete con las flechas", 30, 230)
        mostrar_texto("  ← → ↑ para disparar", 30, 260)
        mostrar_texto("- Multijugador: A-W-S", 30, 300)
        mostrar_texto("- Elimina a todos", 30, 340)
        mostrar_texto("  los aliens para ganar!", 30, 370)
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