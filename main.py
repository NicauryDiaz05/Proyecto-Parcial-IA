import heapq
import time
import pygame
import random
import pytmx  

import constante
from personaje import Personaje
from personaje import Weapon
from animaciones import animaciones, escala_img

#mapa
class Mapa:
    def __init__(self, configuracion, cordenadas) -> None:
        self.configuracion = configuracion
        self.cordenadas = cordenadas
        self.tamano_x = len(configuracion)
        self.tamano_y = len(configuracion[0]) if self.tamano_x > 0 else 0

    def GenerarSucesores(self):
        sucesores = []
        movimientos_validos = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        for movimiento in movimientos_validos:
            x = self.cordenadas[0] + movimiento[0]
            y = self.cordenadas[1] + movimiento[1]

            if 0 <= x < self.tamano_x and 0 <= y < self.tamano_y:
                if self.configuracion[x][y] != 1: 
                    sucesores.append(Mapa(self.configuracion, [x, y]))

        return sucesores

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Mapa):
            return self.cordenadas == __o.cordenadas
        return self.cordenadas == __o

    def __hash__(self) -> int:
        return hash(tuple(self.cordenadas))

    def Costo(self, estado_final):
        return abs(self.cordenadas[0] - estado_final.cordenadas[0]) + abs(self.cordenadas[1] - estado_final.cordenadas[1])
 # NODO
class Nodo:
    def __init__(self, dato, padre=None, distancia=0):
        self.dato = dato
        self.padre = padre
        self.H = distancia
        self.profundidad = 0 if padre is None else padre.profundidad + 1

    def GenerarSucesores(self):
        return self.dato.GenerarSucesores()

    def __eq__(self, __o) -> bool:
        if isinstance(__o, Nodo):
            return self.dato == __o.dato
        if isinstance(__o, type(self.dato)):
            return self.dato == __o
        return False

    def __lt__(self, __o) -> bool:
        return isinstance(__o, Nodo) and self.Heuristica() < __o.Heuristica()

    def __gt__(self, __o) -> bool:
        return isinstance(__o, Nodo) and self.Heuristica() > __o.Heuristica()

    def Heuristica(self):
        return self.H + self.profundidad

    def __hash__(self) -> int:
        return hash(str(self.dato))
    
 # ASTAR
def Astar(estado_inicial, estado_final):
    totalnodos = 1
    nodoactual = Nodo(estado_inicial, None, estado_inicial.Costo(estado_final))
    nodosgenerado = []
    nodosvisitados = set()
    heapq.heapify(nodosgenerado)

    while nodoactual.dato != estado_final:
        sucesores = nodoactual.GenerarSucesores()
        totalnodos += len(sucesores)

        for sucesor in sucesores:
            temp = Nodo(sucesor, nodoactual, sucesor.Costo(estado_final))
            if temp not in nodosvisitados:
                heapq.heappush(nodosgenerado, temp)

        nodosvisitados.add(nodoactual)
        
        # Evitar bucles infinitos si no existe un camino posible
        if len(nodosgenerado) == 0:
            return [], totalnodos
            
        while len(nodosgenerado) > 0 and nodoactual in nodosvisitados:
            nodoactual = heapq.heappop(nodosgenerado)

    camino = []
    while nodoactual:
        camino.append(nodoactual.dato)
        nodoactual = nodoactual.padre

    camino.reverse()
    return camino, totalnodos

# MAPA TMX
def cargar_mapa(nombre_mapa):
    tmx_data = pytmx.util_pygame.load_pygame("mapa//templo_antiguo.tmx")
    ancho = tmx_data.width
    alto = tmx_data.height

    matriz_logica = [[0 for _ in range(alto)] for _ in range(ancho)]
      
    #coliciones 
    try:
        capa_colisiones = tmx_data.get_layer_by_name("Colisiones")
        for x, y, gid in capa_colisiones:
            if gid != 0:
                matriz_logica[x][y] = 1
    except ValueError:
        pass 
        
    #inicio del mundo 
    matriz_logica[0][0] = "S"
    destino = [random.randint(1, ancho-1), random.randint(1, alto-1)]

    while matriz_logica[destino[0]][destino[1]] == 1 or destino == [0,0]:
        destino = [random.randint(1, ancho-1), random.randint(1, alto-1)]
    
    matriz_logica[destino[0]][destino[1]] = "E"

    # Generación de mundo
    for i in range(ancho):
        for j in range(alto):
            # no poner obtaculos en el inicio, destino o donde ya hay colisiones
            if (i == 0 and j == 0) or (i == destino[0] and j == destino[1]) or matriz_logica[i][j] == 1:
                continue
            if random.random() < 0.1:
                matriz_logica[i][j] = 1

    return tmx_data, matriz_logica, destino
        
    # Si no se encuentra un  destino
    if not destino:
        destino = [random.randint(1, ancho-1), random.randint(1, alto-1)]
        while matriz_logica[destino[0]][destino[1]] == 1:
            destino = [random.randint(1, ancho-1), random.randint(1, alto-1)]
            
    return tmx_data, matriz_logica, destino

def draw_mundo_tmx(surface, tmx_data, camara):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            if layer.name == "Colisiones": 
                continue
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, (x * tmx_data.tilewidth - camara.offset_x, 
                                        y * tmx_data.tileheight - camara.offset_y))
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
        centro_x = self.ancho_ventana // 2
        centro_y = self.alto_ventana // 2

        self.offset_x = jugador.shape.centerx - centro_x
        self.offset_y = jugador.shape.centery - centro_y

        self.offset_x = max(0, min(self.offset_x, self.ancho_mapa - self.ancho_ventana))
        self.offset_y = max(0, min(self.offset_y, self.alto_mapa - self.alto_ventana))

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

def draw_ui(surface):
    font = pygame.font.Font(None, 24)
    text_surface = font.render("A* Guía Activa - Sigue la ruta azul", True, (255, 255, 0))
    surface.blit(text_surface, (10, 10))

#ventana
pygame.init()
ventana = pygame.display.set_mode((constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA))
pygame.display.set_caption("El Templo De la Sombras")
pantallaCompleta = False

# Cargamos el mapa
try:
    tmx_data, matriz_logica, destino = cargar_mapa("templo_antiguo.tmx")
    TILE_SIZE = tmx_data.tilewidth
    TAMANO_MAPA_X = tmx_data.width
    TAMANO_MAPA_Y = tmx_data.height
except Exception as e:
    print(f"Error al cargar: {e}")
    pygame.quit()
    exit()

jugador = Personaje(50, 50, animaciones)
jugador.auto_seguir = False 

imagen_baston1 = pygame.image.load("armas//PNG//staves_1//5.png")
imagen_baston1 = escala_img(imagen_baston1, constante.SCALA_BASTON1)
poder_baston1 = pygame.image.load("armas//PNG//staves_1//poder_baston1.png").convert_alpha()
poder_baston1 = escala_img(poder_baston1, constante.SCALA_PODER_BASTON1)
baston1 = Weapon(imagen_baston1, poder_baston1)
grupos_poder = pygame.sprite.Group()

camara = Camara(
    TAMANO_MAPA_X * TILE_SIZE, TAMANO_MAPA_Y * TILE_SIZE,
    constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA
)

mover_izquierda = mover_derecha = mover_arriba = mover_abajo = False
reloj = pygame.time.Clock()
run = True

estado_final = Mapa(matriz_logica, destino)
ultimo_calculo_astar = 0
camino = []

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
                pantallaCompleta = not pantallaCompleta
                ventana = pygame.display.set_mode((constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA), pygame.FULLSCREEN if pantallaCompleta else 0)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: mover_izquierda = False
            if event.key == pygame.K_d: mover_derecha = False
            if event.key == pygame.K_w: mover_arriba = False
            if event.key == pygame.K_s: mover_abajo = False

    # MOVIMIENTO
    delta_x = (constante.VELOCIDAD if mover_derecha else 0) - (constante.VELOCIDAD if mover_izquierda else 0)
    delta_y = (constante.VELOCIDAD if mover_abajo else 0) - (constante.VELOCIDAD if mover_arriba else 0)

    jugador.movimiento(delta_x, delta_y, matriz_logica)
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
        
        if matriz_logica[grid_x][grid_y] != 1:
            estado_inicial = Mapa(matriz_logica, [grid_x, grid_y])
            camino, _ = Astar(estado_inicial, estado_final)
            
        ultimo_calculo_astar = tiempo_actual

    # DIBUJAR 
    draw_mundo_tmx(ventana, tmx_data, matriz_logica, camara)
    if camino: draw_camino(ventana, camino, camara, TILE_SIZE, TILE_SIZE)
    jugador.draw(ventana, camara)
    baston1.draw(ventana, camara)
    for poder in grupos_poder: poder.draw(ventana, camara)
    
    draw_ui(ventana)
    pygame.display.update()

pygame.quit()