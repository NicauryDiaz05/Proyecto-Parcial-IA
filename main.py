import pygame
import constante
import random
import math
from personaje import Personaje
from enemigos import Enemigoesqueleto, Enemigofantasma 
from personaje import Weapon
from animaciones import animaciones, animacionesenemigo1, animacionesenemigo2, escala_img
from Tiled_files.templo import Mapa

# agrege las oleadas del juego y las pantallas de vitorias 
MAX_OLEADAS = 5


def draw_ui(surface, vida, oleada):
    font = pygame.font.Font(None, 24)
    vida_clamped = max(vida, 0)
    text_vida   = font.render(f"Vida: {vida_clamped}",          True, (0, 255, 0))
    text_oleada = font.render(f"Oleada: {oleada}/{MAX_OLEADAS}", True, (0, 255, 0))
    surface.blit(text_vida,   (10, 10))
    surface.blit(text_oleada, (10, 30))


def draw_puerta(surface, puerta_rect, mapa,tick = 0):
    rect_pantalla = pygame.Rect(
        puerta_rect.x + mapa.offset_x,
        puerta_rect.y + mapa.offset_y,
        puerta_rect.width,
        puerta_rect.height,
    )

    p = abs(math.sin(tick * 0.05))
    pygame.draw.rect(surface, (70, 35, 10), rect_pantalla.inflate(4, 4), border_radius=5)
    pygame.draw.rect(surface, (150, 80, 20), rect_pantalla, border_radius=4)
    pygame.draw.rect(surface, (120, 60, 15), rect_pantalla.inflate(-14, -rect_pantalla.height//2), border_radius=3)
    pygame.draw.rect(surface, (int(200+55*p), int(160+55*p), 30), rect_pantalla, 2, border_radius=4)
    pygame.draw.circle(surface, (int(180+75*p), 140, 40), (rect_pantalla.right-10, rect_pantalla.centery), 5)

    font = pygame.font.Font(None, 15)
    surface.blit(font.render("SALIDA", True, (255, 220, 80)), 
                 font.render("SALIDA", True, (0,0,0)).get_rect(center=(rect_pantalla.centerx, rect_pantalla.y+10)))
# Pantallas de juego
def pantalla_victoria(surface, ancho, alto):
    surface.fill((10, 10, 30))
    font_grande  = pygame.font.Font(None, 80)
    font_pequena = pygame.font.Font(None, 36)

    texto1 = font_grande.render("¡VICTORIA!", True, (255, 215, 0))
    texto2 = font_pequena.render("Has escapado del Templo de las Sombras", True, (150, 150, 150))
    texto3 = font_pequena.render("Presiona ESC para volver a la pantalla de inicio", True, (150, 150, 150))

    surface.blit(texto1, texto1.get_rect(center=(ancho // 2, alto // 2 - 60)))
    surface.blit(texto2, texto2.get_rect(center=(ancho // 2, alto // 2 + 20)))
    surface.blit(texto3, texto3.get_rect(center=(ancho // 2, alto // 2 + 65)))

def pantalla_game_over(surface, ancho, alto):
    surface.fill((10, 10, 30))
    font_grande  = pygame.font.Font(None, 80)
    font_pequena = pygame.font.Font(None, 36)

    texto1 = font_grande.render("¡Perdiste!", True, (220, 20, 60))
    texto2 = font_pequena.render("Has caido en el templo de las sombras", True, (150, 150, 150))
    texto3 = font_pequena.render("Presiona la R para reiniciar la partida", True, (150, 150, 150))

    surface.blit(texto1, texto1.get_rect(center=(ancho // 2, alto // 2 - 60)))
    surface.blit(texto2, texto2.get_rect(center=(ancho // 2, alto // 2 + 20)))
    surface.blit(texto3, texto3.get_rect(center=(ancho // 2, alto // 2 + 65)))


    
def pantalla_inicio(surface, ancho, alto):
    surface.fill((10, 10, 30))
    font_grande  = pygame.font.Font(None, 80)
    font_pequena = pygame.font.Font(None, 36)

    texto1 = font_grande.render("¡Bienvenido!", True, (220, 20, 60))
    texto2 = font_pequena.render("Que inicie la aventura", True, (150, 150, 150))
    texto3 = font_pequena.render("Presione Enter para comenzar", True, (150, 150, 150))

    surface.blit(texto1, texto1.get_rect(center=(ancho // 2, alto // 2 - 60)))
    surface.blit(texto2, texto2.get_rect(center=(ancho // 2, alto // 2 + 20)))
    surface.blit(texto3, texto3.get_rect(center=(ancho // 2, alto // 2 + 65)))

def pantalla_Pausar(surface, ancho, alto):
    surface.fill((10, 10, 30))
    font_grande  = pygame.font.Font(None, 80)
    font_pequena = pygame.font.Font(None, 36)

    texto1 = font_grande.render("¡Pausa!", True, (220, 20, 60))
    texto2 = font_pequena.render("Presione la barra de espacio para continua la aventura", True, (150, 150, 150))

    surface.blit(texto1, texto1.get_rect(center=(ancho // 2, alto // 2 - 60)))
    surface.blit(texto2, texto2.get_rect(center=(ancho // 2, alto // 2 + 20)))


# hago que los enemigos apareza de manera aleatoria en el mpa pero que no este serca del jugador 
def posiciones_aleatorias(mapa, cantidad, jugador, distancia_minima_tiles=6):
    tile_jx = int(jugador.shape.centerx // mapa.tile_size)
    tile_jy = int(jugador.shape.centery // mapa.tile_size)

    candidatos = []
    for ty in range(mapa.alto_tiles):
        for tx in range(mapa.ancho_tiles):
            if mapa.configuracion_grid[ty][tx] != 0:
                continue
            dist = abs(tx - tile_jx) + abs(ty - tile_jy)
            if dist >= distancia_minima_tiles:
                candidatos.append((tx, ty))

    if len(candidatos) < cantidad:
        cantidad = len(candidatos)

    return random.sample(candidatos, cantidad)

# agrego una puerta que le de fin l juego 
def posicion_puerta_aleatoria(mapa, jugador, distancia_minima_tiles=8):
    candidatos = posiciones_aleatorias(mapa, 1, jugador, distancia_minima_tiles)
    if not candidatos:
        candidatos = posiciones_aleatorias(mapa, 1, jugador, 4)
    tx, ty = candidatos[0]
    return pygame.Rect(
        tx * mapa.tile_size,
        ty * mapa.tile_size,
        mapa.tile_size,
        mapa.tile_size,
    )

# defino cuanto enemigo habra por oleada y cuales apareceran 
def crear_oleada(mapa, jugador, numero_oleada, imagen_proyectil_enemigo):
    cantidad = constante.ENEMIGOS_BASE + (numero_oleada - 1) * constante.ENEMIGOS_POR_OLEADA
    posiciones = posiciones_aleatorias(mapa, cantidad, jugador)

    proporcion_distancia = (numero_oleada - 1) / (MAX_OLEADAS - 1) * 0.5

    lista = []
    for i, (tx, ty) in enumerate(posiciones):
        px = tx * mapa.tile_size + mapa.tile_size // 2
        py = ty * mapa.tile_size + mapa.tile_size // 2

        if random.random() < proporcion_distancia:
            enemigo = Enemigofantasma(px, py, animacionesenemigo1, imagen_proyectil_enemigo)
        else:
            enemigo = Enemigoesqueleto(px, py, animacionesenemigo2,)

        lista.append(enemigo)

    return lista

# esta reinicia el juego pero aun no la tengo en funcionamiento , lo hare cuando aggrege las pantallas
def reiniciar_juego(ruta_mapa, ancho, alto,grupos_poder, imagen_proyectil_enemigo):
    mapa = Mapa(ruta_mapa, ancho, alto)

    jx = 5 * mapa.tile_size
    jy = 5 * mapa.tile_size
    jugador = Personaje(jx, jy, animaciones)

    grupos_poder.empty()
    enemigos = crear_oleada(mapa, jugador, 1, imagen_proyectil_enemigo)

    return mapa, jugador, enemigos
# -------------------------------------------------------------------------LOOP Primcipal---------------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()
ventana = pygame.display.set_mode((constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA))
pygame.display.set_caption("El Templo De las Sombras")
Fullscreen = False

JUGANDO = 1
VICTORIA = 2
Game_over = 3
Inicio = 4
Pausar = 5 
estado_juego = Inicio

RUTA_MAPA = "Tiled_files//templo.tmx"


imagen_baston1 = pygame.image.load("armas//staves_1//5.png").convert_alpha()
imagen_baston1 = escala_img(imagen_baston1, constante.SCALA_BASTON1)

poder_baston1 = pygame.image.load("armas//staves_1//poder_baston1.png").convert_alpha()
poder_baston1 = escala_img(poder_baston1, constante.SCALA_PODER_BASTON1)

baston1 = Weapon(imagen_baston1, poder_baston1)
grupos_poder = pygame.sprite.Group()

imagen_proyectil_enemigo = pygame.image.load(constante.RUTA_PROYECTIL_ENEMIGO).convert_alpha()
imagen_proyectil_enemigo = escala_img(imagen_proyectil_enemigo, constante.SCALA_PROYECTIL_ENEMIGO)

mapa, jugador, enemigos = reiniciar_juego(RUTA_MAPA, constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA, grupos_poder, imagen_proyectil_enemigo)

mover_izquierda = mover_derecha = mover_arriba = mover_abajo = False
reloj = pygame.time.Clock()
run = True

numero_oleada = 1
puerta_rect  = None
juego_ganado = False
tick = 0

font_oleada = pygame.font.Font(None, 52)
mostrar_texto_oleada = True
timer_texto_oleada   = pygame.time.get_ticks()
DURACION_TEXTO_OLEADA = 2500

pygame.mixer_music.load("Tiled_files//musica-del-templo.mp3")
pygame.mixer_music.play(-1)

sonido_disparo = pygame.mixer.Sound("armas//Staves_1//disparo_baston.mp3")
while run:
    dt = reloj.tick(constante.FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#Eventos de teclado dentro del juego 

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
           if not Fullscreen:
              ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
              constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA = ventana.get_size()
              Fullscreen = True
           else:
              ventana = pygame.display.set_mode((constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA))
              Fullscreen = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB: 
            pygame.display.iconify()

        if estado_juego == JUGANDO:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    estado_juego = Pausar

                if jugador.vivo:
                    if event.key == pygame.K_a: mover_izquierda = True
                    if event.key == pygame.K_d: mover_derecha = True
                    if event.key == pygame.K_w: mover_arriba = True
                    if event.key == pygame.K_s: mover_abajo = True
                if event.key == pygame.K_F11: 
                    tile_jx = int(jugador.shape.centerx // mapa.tile_size)
                    tile_jy = int(jugador.shape.centery // mapa.tile_size)

                    tile_enemigos = [
                        (int(e.shape.centerx // mapa.tile_size),
                         int(e.shape.centery // mapa.tile_size))
                        for e in enemigos
                    ]
            
                    mapa = Mapa(RUTA_MAPA, constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA)

                    jugador.shape.centerx = tile_jx * mapa.tile_size + mapa.tile_size // 2
                    jugador.shape.centery = tile_jy * mapa.tile_size + mapa.tile_size // 2

                    for i, enemigo in enumerate(enemigos):
                        if i < len(tile_enemigos):
                            tx, ty = tile_enemigos[i]
                            enemigo.shape.centerx = tx * mapa.tile_size + mapa.tile_size // 2
                            enemigo.shape.centery = ty * mapa.tile_size + mapa.tile_size // 2

                    grupos_poder.empty()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: mover_izquierda = False
                if event.key == pygame.K_d: mover_derecha = False
                if event.key == pygame.K_w: mover_arriba = False
                if event.key == pygame.K_s: mover_abajo = False

            if not jugador.vivo:
                mover_izquierda = mover_derecha = mover_arriba = mover_abajo = False
       
        elif estado_juego == Inicio:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
               mapa, jugador, enemigos = reiniciar_juego(RUTA_MAPA, constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA, grupos_poder, imagen_proyectil_enemigo)
               numero_oleada = 1
               puerta_rect   = None
               juego_ganado  = False
               mostrar_texto_oleada = True
               timer_texto_oleada   = pygame.time.get_ticks()
               estado_juego = JUGANDO

        elif estado_juego == VICTORIA:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               estado_juego = Inicio

        elif estado_juego == Game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                mapa, jugador, enemigos = reiniciar_juego(RUTA_MAPA, constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA,grupos_poder, imagen_proyectil_enemigo)
                numero_oleada = 1
                puerta_rect   = None
                juego_ganado  = False
                estado_juego  = JUGANDO

        elif estado_juego == Pausar: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    estado_juego = JUGANDO        
               

    ventana.fill(constante.COLOR_FONDO)
    
    if estado_juego == JUGANDO:
 #--------------------------------------------------------- ACTUALIZACIÓN ------------------------------------------------------------------------
        delta_x = (constante.VELOCIDAD if mover_derecha else 0) - (constante.VELOCIDAD if mover_izquierda else 0)
        delta_y = (constante.VELOCIDAD if mover_abajo else 0) - (constante.VELOCIDAD if mover_arriba else 0)

        if jugador.vivo:
            jugador.movimiento(delta_x, delta_y, mapa)

        estado_actual = "running" if (delta_x != 0 or delta_y != 0) else "idle"
        jugador.update(estado_actual)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] or keys[pygame.K_e]:
           jugador.atacar_cuerpo_a_cuerpo(enemigos, constante.DAÑO_BASTON1)

        if jugador.vivo:
            poder = baston1.update(jugador, mapa)
            if poder:
                grupos_poder.add(poder)
                sonido_disparo.play()

        for bala in list(grupos_poder):
            bala.update(mapa, enemigos)

        for enemigo in enemigos:
            enemigo.update_enemigo(jugador, mapa, mapa.configuracion_grid)
            if isinstance(enemigo, Enemigofantasma):
                enemigo.update_proyectiles(mapa, jugador)

        enemigos = [e for e in enemigos if e.vivo]
   
        if not jugador.vivo:
            estado_juego = Game_over

        if jugador.vivo and len(enemigos) == 0 and not juego_ganado:
            if numero_oleada < MAX_OLEADAS:
                numero_oleada += 1
                jugador.curar(20)
                enemigos = crear_oleada(mapa, jugador, numero_oleada, imagen_proyectil_enemigo)
                mostrar_texto_oleada = True
                timer_texto_oleada   = pygame.time.get_ticks()
            elif puerta_rect is None:
                puerta_rect = posicion_puerta_aleatoria(mapa, jugador)
                mostrar_texto_oleada = True
                timer_texto_oleada   = pygame.time.get_ticks()

        if puerta_rect and jugador.vivo and jugador.shape.colliderect(puerta_rect):
            juego_ganado = True
            estado_juego = VICTORIA

        mapa.actualizar_animaciones(dt)
        mapa.actualizar_interacciones(jugador)
        mapa.draw(ventana, debug=False)
#------------------------------------------------------------DIBUJAR EN PANTALLA-----------------------------------------------
        jugador.draw(ventana, mapa)
        if jugador.vivo:
            baston1.draw(ventana, mapa)

        for poder in grupos_poder:
            poder.draw(ventana, mapa)
           

        for enemigo in enemigos:
            enemigo.draw(ventana, mapa)

        draw_ui(ventana, vida=jugador.vida, oleada=numero_oleada)

        if puerta_rect:
            draw_puerta(ventana, puerta_rect, mapa, tick)

        if mostrar_texto_oleada:
            if pygame.time.get_ticks() - timer_texto_oleada < DURACION_TEXTO_OLEADA:
                if puerta_rect and numero_oleada == MAX_OLEADAS:
                    texto = font_oleada.render("¡Felicidades los venciste a todos,!Ve a la salida!", True, (255, 215, 0))
                else:
                    texto = font_oleada.render(f"¡Oleada {numero_oleada}!", True, (255, 80, 80))
                rect_texto = texto.get_rect(center=(constante.WIDTH_VENTANA // 2, constante.HEIGHT_VENTANA // 3))
                ventana.blit(texto, rect_texto)
            else:
                mostrar_texto_oleada = False

                
#------------------------------------------------------------DIBUJAR LOS ESTADOS EN PANTALLA----------------------------------------------- 

    elif estado_juego == VICTORIA:
        pantalla_victoria(ventana, constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA)

    elif estado_juego == Game_over:
        pantalla_game_over(ventana, constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA)
        
    elif estado_juego == Inicio:
        pantalla_inicio(ventana, constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA)    

    elif estado_juego == Pausar:
        pantalla_Pausar(ventana, constante.WIDTH_VENTANA, constante.HEIGHT_VENTANA)

    tick += 1 

    pygame.display.update()

pygame.quit()