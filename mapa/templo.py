import pygame
import random
import heapq

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

class Mapa:
    def __init__(self, ancho, alto, tile_size):
        self.ancho = ancho
        self.alto = alto
        self.tile_size = tile_size

        self.matriz = [[1 for _ in range(ancho)] for _ in range(alto)]  
        self.habitaciones = []
        self.habitacion_central = None

        self.tiempo_animacion = pygame.time.get_ticks()
        self.estado_trampa = 0
        self.frame_vela = 0
        mundo_data, destino = self.generar_mundo(ancho)
        self.matriz = mundo_data
        self.destino = destino

        self.generar_habitaciones_grandes()

        self.cargar_sprites()

        self.cofres_abiertos = set()
        self.trampas_activadas = set()
        
        self.niebla = pygame.Surface((ancho * tile_size, alto * tile_size), pygame.SRCALPHA)
        self.niebla.fill((0, 0, 0, 150))

    def generar_mundo(self, n):
        mapa = [[0 for _ in range(n)] for _ in range(n)]
        
        inicio_x = random.randint(0, n-1)
        inicio_y = random.randint(0, n-1)
        mapa[inicio_y][inicio_x] = "S"
        
        destino_x, destino_y = inicio_x, inicio_y
        while destino_x == inicio_x and destino_y == inicio_y:
            destino_x = random.randint(0, n-1)
            destino_y = random.randint(0, n-1)
        mapa[destino_y][destino_x] = "E"
        
        for i in range(n):
            for j in range(n):
                if mapa[i][j] in ["S", "E"]:
                    continue
                if random.random() < 0.1:
                    mapa[i][j] = 1 
                else:
                    mapa[i][j] = 0  
        
        return mapa, (destino_x, destino_y)

    def generar_habitaciones_grandes(self):
        self.habitaciones = []
        
        hab_ancho = random.randint(12, 18) 
        hab_alto = random.randint(12, 18)
        
        centro_x = self.ancho // 2 - hab_ancho // 2
        centro_y = self.alto // 2 - hab_alto // 2
        central = pygame.Rect(centro_x, centro_y, hab_ancho, hab_alto)
        self.habitacion_central = central
        self.habitaciones.append(central)
        
        for y in range(central.y, central.y + central.h):
            for x in range(central.x, central.x + central.w):
                if 0 <= y < self.alto and 0 <= x < self.ancho:
                    self.matriz[y][x] = 0
        
        self.decorar_habitacion(central, es_central=True)
        num_habitaciones = random.randint(6, 10)
        intentos = 0
        
        while len(self.habitaciones) < num_habitaciones + 1 and intentos < 100:
            intentos += 1
            w = random.randint(10, 16)
            h = random.randint(10, 16)
            lado = random.randint(0, 3)  
            
            if lado == 0:  
                x = random.randint(2, self.ancho - w - 2)
                y = random.randint(2, centro_y - h - 2)
            elif lado == 1:  
                x = random.randint(centro_x + central.w + 2, self.ancho - w - 2)
                y = random.randint(2, self.alto - h - 2)
            elif lado == 2:  
                x = random.randint(2, self.ancho - w - 2)
                y = random.randint(centro_y + central.h + 2, self.alto - h - 2)
            else:  
                x = random.randint(2, centro_x - w - 2)
                y = random.randint(2, self.alto - h - 2)
            
            nueva_hab = pygame.Rect(x, y, w, h)
            
            if not any(nueva_hab.colliderect(hab) for hab in self.habitaciones):
                if 0 <= x and x + w < self.ancho and 0 <= y and y + h < self.alto:
                    self.habitaciones.append(nueva_hab)
                    for i in range(y, y + h):
                        for j in range(x, x + w):
                            if 0 <= i < self.alto and 0 <= j < self.ancho:
                                self.matriz[i][j] = 0
                    
                    self.decorar_habitacion(nueva_hab)
                    self.conectar_con_central(nueva_hab)
        
        for i in range(1, len(self.habitaciones) - 1):
            if random.random() < 0.5:
                self.conectar_habitaciones(self.habitaciones[i], self.habitaciones[i + 1])

    def conectar_con_central(self, habitacion):
        c1 = self.habitacion_central.center
        c2 = habitacion.center
        
        if random.random() < 0.5:
            self.crear_pasillo_h(c1[0], c2[0], c1[1])
            self.crear_pasillo_v(c1[1], c2[1], c2[0])
        else:
            self.crear_pasillo_v(c1[1], c2[1], c1[0])
            self.crear_pasillo_h(c1[0], c2[0], c2[1])

    def conectar_habitaciones(self, hab1, hab2):
        c1 = hab1.center
        c2 = hab2.center
        
        if random.random() < 0.5:
            self.crear_pasillo_h(c1[0], c2[0], c1[1])
            self.crear_pasillo_v(c1[1], c2[1], c2[0])
        else:
            self.crear_pasillo_v(c1[1], c2[1], c1[0])
            self.crear_pasillo_h(c1[0], c2[0], c2[1])

    def crear_pasillo_h(self, x1, x2, y):
        for x in range(min(x1, x2) - 1, max(x1, x2) + 2):
            for dy in range(-1, 2):  
                ny = y + dy
                if 0 <= ny < self.alto and 0 <= x < self.ancho:
                    if self.matriz[ny][x] == 1: 
                        self.matriz[ny][x] = 0

    def crear_pasillo_v(self, y1, y2, x):
        for y in range(min(y1, y2) - 1, max(y1, y2) + 2):
            for dx in range(-1, 2):  
                nx = x + dx
                if 0 <= y < self.alto and 0 <= nx < self.ancho:
                    if self.matriz[y][nx] == 1:  
                        self.matriz[y][nx] = 0

    def decorar_habitacion(self, hab, es_central=False):
        cx, cy = hab.centerx, hab.centery
        if 0 <= cy < self.alto and 0 <= cx < self.ancho and self.matriz[cy][cx] == 0:
            if es_central:
                self.matriz[cy][cx] = 7
            else:
                if random.random() < 0.3:
                    self.matriz[cy][cx] = 2 
        
        for y in range(hab.y + 1, hab.y + hab.h - 1):
            for x in range(hab.x + 1, hab.x + hab.w - 1):
                if self.matriz[y][x] == 0:
                    prob = random.random()
                    
                    if prob < 0.03:
                        self.matriz[y][x] = 3
                    elif prob < 0.06:
                        self.matriz[y][x] = 4
                    elif prob < 0.09:
                        self.matriz[y][x] = 5
                    elif prob < 0.12:
                        self.matriz[y][x] = 6
                    elif prob < 0.15:
                        self.matriz[y][x] = 7
                    elif prob < 0.18:
                        self.matriz[y][x] = 8
                    elif prob < 0.21:
                        self.matriz[y][x] = 9
                    elif prob < 0.23:
                        self.matriz[y][x] = 10
                    elif prob < 0.25:
                        self.matriz[y][x] = 11
                    
                    if (x == hab.x + 1 or x == hab.x + hab.w - 2) and \
                       (y == hab.y + 1 or y == hab.y + hab.h - 2):
                        if random.random() < 0.4:
                            self.matriz[y][x] = 5  

    def cargar_sprites(self):
        self.sprites = {
            0: pygame.image.load("mapa/suelo.png").convert(),
            1: pygame.image.load("mapa/Muro principal.png").convert(),
            2: pygame.image.load("mapa/Trampa desactivada.png").convert_alpha(),
            3: pygame.image.load("mapa/Estatua.png").convert_alpha(),
            4: pygame.image.load("mapa/Antorcha.png").convert_alpha(),
            5: pygame.image.load("mapa/Muro decorado.png").convert_alpha(),
            6: pygame.image.load("mapa/Cofre.png").convert_alpha(),
            7: pygame.image.load("mapa/Altar central.png").convert_alpha(),
            8: pygame.image.load("mapa/Sarcófago.png").convert_alpha(),
            9: pygame.image.load("mapa/Trampa activada.png").convert_alpha(),
            10: pygame.image.load("mapa/Escaleras.png").convert_alpha(),
            11: pygame.image.load("mapa/Símbolo1.png").convert_alpha(), 
            12: pygame.image.load("mapa/Columna.png").convert_alpha(),  
            13: pygame.image.load("mapa/Portal oscuro.png").convert_alpha(),  
            14: pygame.image.load("mapa/Altar secundario.png").convert_alpha(),  
            15: pygame.image.load("mapa/Vacío oscuro.png").convert_alpha(),  
            16: pygame.image.load("mapa/simbolo2.png").convert_alpha(), 
            17: pygame.image.load("mapa/antocha2.png").convert_alpha(), 
            18: pygame.image.load("mapa/fuente.png").convert_alpha(), 
        }
        
        for key in self.sprites:
            self.sprites[key] = pygame.transform.scale(
                self.sprites[key], 
                (self.tile_size, self.tile_size)
            )

    def actualizar_animaciones(self):    
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_animacion > 300:  
            self.tiempo_animacion = ahora
            self.estado_trampa = 1 - self.estado_trampa
            self.frame_vela = (self.frame_vela + 1) % 4  

    def actualizar_interacciones(self, jugador):
        tile_x = jugador.shape.centerx // self.tile_size
        tile_y = jugador.shape.centery // self.tile_size

        if 0 <= tile_y < self.alto and 0 <= tile_x < self.ancho:
            tile = self.matriz[tile_y][tile_x]
            if tile == 8:
                self.cofres_abiertos.add((tile_x, tile_y))
                self.matriz[tile_y][tile_x] = 6
            if tile == 9:
                self.trampas_activadas.add((tile_x, tile_y))
            if hasattr(self, 'destino') and (tile_x, tile_y) == self.destino:
                print("¡Has llegado al destino!")

    def dibujar_luces(self, surface, camara):
        for y in range(self.alto):
            for x in range(self.ancho):
                if self.matriz[y][x] in [4, 14]: 
                    centro_x = x * self.tile_size - camara.offset_x + self.tile_size // 2
                    centro_y = y * self.tile_size - camara.offset_y + self.tile_size // 2

                    radio = 50 + random.randint(-20, 20)
                    luz = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
                    
                    pygame.draw.circle(luz, (255, 200, 100, 120), (radio, radio), radio)
                    pygame.draw.circle(luz, (255, 220, 150, 80), (radio, radio), radio//2)
                    pygame.draw.circle(luz, (255, 255, 200, 50), (radio, radio), radio//3)

                    surface.blit(luz, (centro_x-radio, centro_y-radio), special_flags=pygame.BLEND_ADD)

    def draw(self, surface, camara):
        self.actualizar_animaciones()

        surface.fill((12, 16, 28))  

        inicio_x = max(0, camara.offset_x // self.tile_size)
        inicio_y = max(0, camara.offset_y // self.tile_size)
        fin_x = min(self.ancho, (camara.offset_x + camara.ancho_ventana) // self.tile_size + 2)
        fin_y = min(self.alto, (camara.offset_y + camara.alto_ventana) // self.tile_size + 2)

        for y in range(inicio_y, fin_y):
            for x in range(inicio_x, fin_x):
                tile_id = self.matriz[y][x]
                
                rect = pygame.Rect(
                    x * self.tile_size - camara.offset_x,
                    y * self.tile_size - camara.offset_y,
                    self.tile_size,
                    self.tile_size
                )
                if tile_id != 1:  
                    suelo_rect = rect.copy()
                    if (x + y) % 2 == 0:
                        suelo_color = (70, 70, 85)
                    else:
                        suelo_color = (80, 80, 95)
                    pygame.draw.rect(surface, suelo_color, suelo_rect)
                    pygame.draw.rect(surface, (50, 50, 60), suelo_rect, 1)

        for y in range(inicio_y, fin_y):
            for x in range(inicio_x, fin_x):
                tile_id = self.matriz[y][x]
                
                if tile_id == 0:
                    continue

                if (x, y) in self.trampas_activadas and self.estado_trampa:
                    tile_id = 2  

                rect = pygame.Rect(
                    x * self.tile_size - camara.offset_x,
                    y * self.tile_size - camara.offset_y,
                    self.tile_size,
                    self.tile_size
                )

                if tile_id in self.sprites:
                    imagen = self.sprites[tile_id]
                    if tile_id == 1:
                        sombra = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
                        sombra.fill((0, 0, 0, 60))
                        imagen.blit(sombra, (0, 0))

                    surface.blit(imagen, rect)

        sombra_global = pygame.Surface((camara.ancho_ventana, camara.alto_ventana), pygame.SRCALPHA)
        sombra_global.fill((0, 0, 20, 40))
        surface.blit(sombra_global, (0, 0))

        self.dibujar_luces(surface, camara)

    def actualizar_niebla(self, jugador_x, jugador_y, radio_vision):
        self.niebla.fill((0, 0, 0, 180))
        
        radio_vision = radio_vision + 50
        
        pygame.draw.circle(self.niebla, (0, 0, 0, 0),
                           (int(jugador_x), int(jugador_y)), radio_vision)
        
        for i in range(3):
            radio_grad = radio_vision - i * 30
            if radio_grad > 0:
                alpha = 30 - i * 8
                pygame.draw.circle(self.niebla, (0, 0, 0, alpha), 
                                  (int(jugador_x), int(jugador_y)), radio_grad, 3)

    def draw_niebla(self, surface, camara):
        surface.blit(self.niebla, (-camara.offset_x, -camara.offset_y))