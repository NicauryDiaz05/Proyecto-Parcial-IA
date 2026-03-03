import pygame
import random
import constante
from personaje import Personaje
from personaje import Weapon
from animaciones import animaciones, escala_img
from mapa.templo import Mapa

#camara 
class Camara:
    def __init__(self, ancho_mapa, alto_mapa, ancho_ventana, alto_ventana):
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana
        self.offset_x = 0
        self.offset_y = 0

    def centrar_en_jugador(self, jugador):
        self.offset_x = jugador.shape.centerx - self.ancho_ventana // 2
        self.offset_y = jugador.shape.centery - self.alto_ventana // 2
        self.offset_x = max(0, min(self.offset_x, self.ancho_mapa - self.ancho_ventana))
        self.offset_y = max(0, min(self.offset_y, self.alto_mapa - self.alto_ventana))
        
    def aplicar(self, sprite):
        return sprite.shape.move(-self.offset_x, -self.offset_y)

def draw_camino(surface, camino, camara, tile_w, tile_h):
    for nodo in camino:
        x, y = nodo.cordenadas
        rect = pygame.Rect(
            x * tile_w - camara.offset_x + (tile_w // 3),
            y * tile_h - camara.offset_y + (tile_h // 3),
            tile_w // 3,
            tile_h // 3
        )
        pygame.draw.rect(surface, (0, 150, 255, 150), rect) 

def draw_ui(surface, vida):
    font = pygame.font.Font(None, 24)
    text_surface = font.render(f"Vida: {vida}", True, (255, 255, 0))
    surface.blit(text_surface, (10, 10))

#ventana
pygame.init()
ventana = pygame.display.set_mode((constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA,))
pygame.display.set_caption("El Templo De la Sombras")
Fullscreen = False

TILE_SIZE = 32
TAMANO_MAPA_X, TAMANO_MAPA_Y = 80, 80
mapa = Mapa(TAMANO_MAPA_X, TAMANO_MAPA_Y, TILE_SIZE)

# Buscar una habitación válida para colocar al jugador
if mapa.habitaciones and len(mapa.habitaciones) > 0:
    
    hab_inicial = mapa.habitaciones[0]
    encontrado = False
    for intento in range(100):  
        jx = random.randint(hab_inicial.x + 1, hab_inicial.x + hab_inicial.w - 2)
        jy = random.randint(hab_inicial.y + 1, hab_inicial.y + hab_inicial.h - 2)
        if 0 <= jy < TAMANO_MAPA_Y and 0 <= jx < TAMANO_MAPA_X:
            if mapa.matriz[jy][jx] == 0:
                jx = jx * TILE_SIZE
                jy = jy * TILE_SIZE
                encontrado = True
                break
 # Fallback: usar el centro de la habitación si no se encuentra una celda de suelo
       
        jx = hab_inicial.centerx * TILE_SIZE
        jy = hab_inicial.centery * TILE_SIZE
else:
    
    jx = 5 * TILE_SIZE
    jy = 5 * TILE_SIZE

jugador = Personaje(jx, jy, animaciones)
jugador.auto_seguir = False 

imagen_baston1 = pygame.image.load("armas//PNG//staves_1//5.png")
imagen_baston1 = escala_img(imagen_baston1, constante.SCALA_BASTON1)
poder_baston1 = pygame.image.load("armas//PNG//staves_1//poder_baston1.png").convert_alpha()
poder_baston1 = escala_img(poder_baston1, constante.SCALA_PODER_BASTON1)
baston1 = Weapon(imagen_baston1, poder_baston1)
grupos_poder = pygame.sprite.Group()

camara = Camara(TAMANO_MAPA_X * TILE_SIZE, TAMANO_MAPA_Y * TILE_SIZE, constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA)

mover_izquierda = mover_derecha = mover_arriba = mover_abajo = False
reloj = pygame.time.Clock()
run = True

ultimo_calculo_astar = 0
camino = []

# Variables para la niebla
radio_vision = 200

while run:
    reloj.tick(constante.FPS)
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
                 camara.ancho_ventana = constante.WIDTH_VENTANA
                 camara.alto_ventana = constante.HEIGHT_VENTANA
                 Fullscreen = True
               else:
                 ventana = pygame.display.set_mode( (constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA) )
                 Fullscreen = False
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: mover_izquierda = False
            if event.key == pygame.K_d: mover_derecha = False
            if event.key == pygame.K_w: mover_arriba = False
            if event.key == pygame.K_s: mover_abajo = False

    # MOVIMIENTO
    delta_x = (constante.VELOCIDAD if mover_derecha else 0) - (constante.VELOCIDAD if mover_izquierda else 0)
    delta_y = (constante.VELOCIDAD if mover_abajo else 0) - (constante.VELOCIDAD if mover_arriba else 0)

    jugador.movimiento(delta_x, delta_y, mapa)
        
    estado_actual = "walking" if (delta_x != 0 or delta_y != 0) else "idle"

    camara.centrar_en_jugador(jugador)
    jugador.update(estado_actual)

    poder = baston1.update(jugador, camara)
    if poder: grupos_poder.add(poder)
    grupos_poder.update()

    # ACTUALIZAR RUTA A* 
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_calculo_astar > 400: 
        grid_x = int(jugador.shape.centerx // TILE_SIZE)
        grid_y = int(jugador.shape.centery // TILE_SIZE)
        
        # Limitar para evitar errores fuera del mapa
        grid_x = max(0, min(grid_x, TAMANO_MAPA_X - 1))
        grid_y = max(0, min(grid_y, TAMANO_MAPA_Y - 1))
             
        ultimo_calculo_astar = tiempo_actual

    # Actualizar interacciones del mapa (cofres, trampas)
    mapa.actualizar_interacciones(jugador)
    
    # Actualizar niebla
    mapa.actualizar_niebla(
        jugador.shape.centerx - camara.offset_x,
        jugador.shape.centery - camara.offset_y,
        radio_vision
    )

    # DIBUJAR 
    mapa.draw(ventana, camara)
    if camino: draw_camino(ventana, camino, camara, TILE_SIZE, TILE_SIZE)
    jugador.draw(ventana, camara)
    baston1.draw(ventana, camara)
    for poder in grupos_poder: poder.draw(ventana, camara)
    
    # Dibujar niebla
    mapa.draw_niebla(ventana, camara)
    
    draw_ui(ventana, vida=jugador.vida)
    pygame.display.update()

pygame.quit()