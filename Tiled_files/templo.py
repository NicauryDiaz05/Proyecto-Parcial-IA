import pygame
import heapq
import pytmx
import time
from pytmx import TiledTileLayer
import math


class MapaEstado:
    def __init__(self, configuracion, cordenadas) -> None:
        self.configuracion = configuracion
        self.cordenadas = cordenadas
        self.tamano_y = len(configuracion)
        self.tamano_x = len(configuracion[0]) if self.tamano_y > 0 else 0

    def GenerarSucesores(self):
        sucesores = []
        movimientos_validos = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        for movimiento in movimientos_validos:
            x = self.cordenadas[0] + movimiento[0]
            y = self.cordenadas[1] + movimiento[1]

            if 0 <= y < self.tamano_y and 0 <= x < self.tamano_x:
                if self.configuracion[y][x] in [0, 2, 4, 5, 9]: 
                    sucesores.append(MapaEstado(self.configuracion, [x, y]))

        return sucesores

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, MapaEstado):
            return self.cordenadas == __o.cordenadas
        return self.cordenadas == __o

    def __hash__(self) -> int:
        return hash(tuple(self.cordenadas))

    def Costo(self, estado_final):
        return abs(self.cordenadas[0] - estado_final.cordenadas[0]) + abs(self.cordenadas[1] - estado_final.cordenadas[1])

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

 #mapa 
class Mapa:
    def __init__(self, templo, ancho_pantalla, alto_pantalla):
        self.tmx_data = pytmx.load_pygame(templo, pixelalpha=True)

        self.tile_size_original = self.tmx_data.tilewidth
        self.ancho_tiles = self.tmx_data.width
        self.alto_tiles = self.tmx_data.height

        escala_x = ancho_pantalla / (self.ancho_tiles * self.tile_size_original)
        escala_y = alto_pantalla / (self.alto_tiles * self.tile_size_original)
        self.escala = min(escala_x, escala_y)

        self.tile_size = int(self.tile_size_original * self.escala)

        self.ancho_px = self.ancho_tiles * self.tile_size
        self.alto_px = self.alto_tiles * self.tile_size

        self.offset_x = (ancho_pantalla - self.ancho_px) // 2
        self.offset_y = (alto_pantalla - self.alto_px) // 2

        self.trampas = []
        self.trampas_info = []
        self.animaciones = {}
        self.colisiones = []
        self.configuracion_grid = []

        self._cargar_animaciones()
        self._cargar_colisiones()
        self._crear_trampas()
        self._generar_grid()

    # Animaciones 

    def _cargar_animaciones(self):
        for gid, propiedades in self.tmx_data.tile_properties.items():
            frames_data = propiedades.get("frames")
            if frames_data:
                frames_surfaces = []
                for frame in frames_data:
                    img = self.tmx_data.get_tile_image_by_gid(frame.gid)
                    if img:
                        img_escalada = pygame.transform.scale(
                            img, (self.tile_size, self.tile_size)
                        )
                        frames_surfaces.append((img_escalada, frame.duration))

                if frames_surfaces:
                    self.animaciones[gid] = {
                        "frames": frames_surfaces,
                        "indice": 0,
                        "timer": 0,
                    }

    #coliciones 

    def _cargar_colisiones(self):
        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name.lower() == "colision":
                    for obj in layer:
                        rect = pygame.Rect(
                            int(obj.x * self.escala),
                            int(obj.y * self.escala),
                            int(obj.width * self.escala),
                            int(obj.height * self.escala),
                        )
                        self.colisiones.append(rect)

    # Trampas 
    def _crear_trampas(self):
        for layer in self.tmx_data.visible_layers:
            if not isinstance(layer, TiledTileLayer):
                continue

            if "trap" not in layer.name.lower():
                continue

            for x, y, gid in layer:
                if gid == 0:
                    continue

                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )

                self.trampas.append(rect)
                self.trampas_info.append({"rect": rect, "ultimo": 0})

    # Grid de navegacion para A*
    def _generar_grid(self):
        self.configuracion_grid = [[0] * self.ancho_tiles for _ in range(self.alto_tiles)]

        for colision in self.colisiones:
            tile_x_inicio = int(colision.left   // self.tile_size)
            tile_y_inicio = int(colision.top    // self.tile_size)
            tile_x_fin    = int(colision.right  // self.tile_size)
            tile_y_fin    = int(colision.bottom // self.tile_size)

            for ty in range(tile_y_inicio, tile_y_fin + 1):
                for tx in range(tile_x_inicio, tile_x_fin + 1):
                    if 0 <= ty < self.alto_tiles and 0 <= tx < self.ancho_tiles:
                        self.configuracion_grid[ty][tx] = 1

    # animaciones actualizar 

    def actualizar_animaciones(self, dt):
        for gid, anim in self.animaciones.items():
            anim["timer"] += dt
            _, duracion_actual = anim["frames"][anim["indice"]]

            if anim["timer"] >= duracion_actual:
                anim["timer"] = 0
                anim["indice"] = (anim["indice"] + 1) % len(anim["frames"])

    # obtene tiles 

    def _get_tile_image(self, gid):
        if gid in self.animaciones:
            anim = self.animaciones[gid]
            surface, _ = anim["frames"][anim["indice"]]
            return surface

        img = self.tmx_data.get_tile_image_by_gid(gid)
        if img:
            return pygame.transform.scale(
                img, (self.tile_size, self.tile_size)
            )

        return None

    #Verifica coliciones 

    def verificar_colision(self, rect_jugador, dx, dy):
        rect_temp = rect_jugador.copy()
        rect_temp.x += dx
        rect_temp.y += dy

        # Colisión contra objetos
        for colision in self.colisiones:
            if rect_temp.colliderect(colision):
                return True

        # Límites del mapa 
        if (
            rect_temp.left < 0
            or rect_temp.right > self.ancho_px
            or rect_temp.top < 0
            or rect_temp.bottom > self.alto_px
        ):
            return True

        return False

    # INTERACCIONES


    def actualizar_interacciones(self, jugador):
        tiempo_actual = time.time()
        cooldown = 3

        for info in self.trampas_info:
            if tiempo_actual - info["ultimo"] >= cooldown:
                if jugador.shape.colliderect(info["rect"]):
                    jugador.vida -= 5
                    info["ultimo"] = tiempo_actual

    
    # DIBUJADO

    def draw(self, surface, debug=False):
        for layer in self.tmx_data.visible_layers:
            if not isinstance(layer, TiledTileLayer):
                continue

            if "colision" in layer.name.lower():
                continue

            for x, y, gid in layer:
                if gid == 0:
                    continue

                tile = self._get_tile_image(gid)
                if tile:
                    screen_x = self.offset_x + x * self.tile_size
                    screen_y = self.offset_y + y * self.tile_size
                    surface.blit(tile, (screen_x, screen_y))

        # Dibujar colisiones en debug (con offset SOLO visual)
        if debug:
            for colision in self.colisiones:
                debug_rect = colision.copy()
                debug_rect.x += self.offset_x
                debug_rect.y += self.offset_y
                pygame.draw.rect(surface, (255, 0, 0), debug_rect, 2)
