import pygame
import constante
from personaje import Personaje
from personaje import Weapon
from animaciones import animaciones, escala_img
from Tiled_files.templo import Mapa


def draw_ui(surface, vida):
    font = pygame.font.Font(None, 24)
    text_surface = font.render(f"Vida: {vida}", True, (255, 255, 0))
    surface.blit(text_surface, (10, 10))


pygame.init()
ventana = pygame.display.set_mode((constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA))
pygame.display.set_caption("El Templo De las Sombras")
Fullscreen = False


mapa = Mapa("Tiled_files//templo.tmx", constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA)

TAMANO_MAPA_X = mapa.ancho_tiles
TAMANO_MAPA_Y = mapa.alto_tiles

jx = 5 * mapa.tile_size
jy = 5 * mapa.tile_size

jugador = Personaje(jx, jy, animaciones)
jugador.auto_seguir = False

imagen_baston1 = pygame.image.load("armas//staves_1//5.png").convert_alpha()
imagen_baston1 = escala_img(imagen_baston1, constante.SCALA_BASTON1)

poder_baston1 = pygame.image.load("armas//staves_1//poder_baston1.png").convert_alpha()
poder_baston1 = escala_img(poder_baston1, constante.SCALA_PODER_BASTON1)

baston1 = Weapon(imagen_baston1, poder_baston1)
grupos_poder = pygame.sprite.Group()

mover_izquierda = mover_derecha = mover_arriba = mover_abajo = False
reloj = pygame.time.Clock()
run = True

ultimo_calculo_astar = 0
camino = []


while run:
    dt = reloj.tick(constante.FPS)  
    ventana.fill(constante.COLOR_FONDO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: mover_izquierda = True
            if event.key == pygame.K_d: mover_derecha = True
            if event.key == pygame.K_w: mover_arriba = True
            if event.key == pygame.K_s: mover_abajo = True

            if event.key == pygame.K_F11:
                if not Fullscreen:
                    ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA = ventana.get_size()
                    Fullscreen = True
                else:
                    ventana = pygame.display.set_mode((constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA))
                    Fullscreen = False

                mapa = Mapa("Tiled_files//templo.tmx", constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: mover_izquierda = False
            if event.key == pygame.K_d: mover_derecha = False
            if event.key == pygame.K_w: mover_arriba = False
            if event.key == pygame.K_s: mover_abajo = False

    delta_x = (constante.VELOCIDAD if mover_derecha else 0) - (constante.VELOCIDAD if mover_izquierda else 0)
    delta_y = (constante.VELOCIDAD if mover_abajo else 0) - (constante.VELOCIDAD if mover_arriba else 0)

    jugador.movimiento(delta_x, delta_y, mapa)

    estado_actual = "running" if (delta_x != 0 or delta_y != 0) else "idle"
    jugador.update(estado_actual)

    poder = baston1.update(jugador, mapa)
    if poder:
        grupos_poder.add(poder)
    grupos_poder.update(mapa)

    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_calculo_astar > 400:
        grid_x = int(jugador.shape.centerx // mapa.tile_size)
        grid_y = int(jugador.shape.centery // mapa.tile_size)
        grid_x = max(0, min(grid_x, TAMANO_MAPA_X - 1))
        grid_y = max(0, min(grid_y, TAMANO_MAPA_Y - 1))
        ultimo_calculo_astar = tiempo_actual

    mapa.actualizar_animaciones(dt)         
    mapa.actualizar_interacciones(jugador)  
    mapa.draw(ventana, debug=False)                      

    jugador.draw(ventana, mapa)
    baston1.draw(ventana, mapa)

    for poder in grupos_poder:
        poder.draw(ventana, mapa)

    draw_ui(ventana, vida=jugador.vida)
    pygame.display.update()

pygame.quit()