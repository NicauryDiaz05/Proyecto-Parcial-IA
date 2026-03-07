import pygame
import constante
import math
import random
from personaje import Personaje 

# arbol de comportaminto y los direntes estado para los enemigos 
class NodoEstado:
    EXITO     = "EXITO"
    FALLO     = "FALLO"


class Nodo:
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        raise NotImplementedError


class Secuencia(Nodo):
    def __init__(self, hijos):
        self.hijos = hijos

    def ejecutar(self, enemigo, jugador, mapa, cfg):
        for hijo in self.hijos:
            if hijo.ejecutar(enemigo, jugador, mapa, cfg) == NodoEstado.FALLO:
                return NodoEstado.FALLO
        return NodoEstado.EXITO


class Selector(Nodo):
    def __init__(self, hijos):
        self.hijos = hijos

    def ejecutar(self, enemigo, jugador, mapa, cfg):
        for hijo in self.hijos:
            resultado = hijo.ejecutar(enemigo, jugador, mapa, cfg)
            if resultado != NodoEstado.FALLO:
                return resultado
        return NodoEstado.FALLO


class CondicionMuerto(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        return NodoEstado.EXITO if not enemigo.vivo else NodoEstado.FALLO


class CondicionRecibioGolpe(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        return NodoEstado.EXITO if enemigo.recibio_golpe else NodoEstado.FALLO


class CondicionDetectaJugador(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        d = enemigo._distancia_al_jugador(jugador)
        return NodoEstado.EXITO if d <= enemigo.rango_deteccion else NodoEstado.FALLO


class CondicionEnRangoAtaqueEsqueleto(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        d = enemigo._distancia_al_jugador(jugador)
        return NodoEstado.EXITO if d <= enemigo.rango_ataque else NodoEstado.FALLO


class CondicionEnRangoDisparo(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        d = enemigo._distancia_al_jugador(jugador)
        return NodoEstado.EXITO if d <= enemigo.rango_disparo else NodoEstado.FALLO


class CondicionDemasiadoCerca(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        d = enemigo._distancia_al_jugador(jugador)
        return NodoEstado.EXITO if d <= enemigo.rango_huida else NodoEstado.FALLO


class AccionMorir(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        enemigo._set_estado_anim("Dying")
        return NodoEstado.EXITO


class AccionHurt(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        enemigo._set_estado_anim("Hurt")
        enemigo.recibio_golpe = False
        return NodoEstado.EXITO


class AccionPatrullar(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        tiempo_actual = pygame.time.get_ticks()

        if (enemigo.destino_patrulla is None or
                tiempo_actual - enemigo.ultimo_cambio_patrulla > 4000):
            enemigo._elegir_nuevo_destino_patrulla(mapa)

        if (tiempo_actual - enemigo.ultimo_calculo_astar > enemigo.intervalo_astar and
                enemigo.destino_patrulla is not None):
            enemigo.ultimo_calculo_astar = tiempo_actual
            enemigo._calcular_ruta_a(enemigo.destino_patrulla, mapa, cfg)

        if enemigo.destino_patrulla is None:
            enemigo._set_estado_anim("idle")
            return NodoEstado.EXITO

        enemigo.mover_por_camino(mapa)

        dx = enemigo.destino_patrulla[0] - enemigo.shape.centerx
        dy = enemigo.destino_patrulla[1] - enemigo.shape.centery
        if math.sqrt(dx*dx + dy*dy) < mapa.tile_size:
            enemigo.destino_patrulla = None
            enemigo._set_estado_anim("idle")
        else:
            enemigo._set_estado_anim("Walking")

        return NodoEstado.EXITO

# aplicadoo el astar par detectar y perseguir al personaje 
class AccionPerseguir(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - enemigo.ultimo_calculo_astar > enemigo.intervalo_astar:
            enemigo.ultimo_calculo_astar = tiempo_actual
            enemigo.actualizar_camino(jugador, mapa, cfg)

        enemigo.mover_por_camino(mapa)
        enemigo.actualizar_flip(jugador.shape.centerx - enemigo.shape.centerx)
        enemigo._set_estado_anim("Running")
        return NodoEstado.EXITO


class AccionAtacarEsqueleto(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        tiempo_actual = pygame.time.get_ticks()
        enemigo.actualizar_flip(jugador.shape.centerx - enemigo.shape.centerx)

        if tiempo_actual - enemigo.ultimo_ataque >= enemigo.cooldown_ataque:
            jugador.recibir_danio(constante.DAÑO_ENEMIGO_ESQUELETO)
            enemigo.ultimo_ataque = tiempo_actual
            enemigo._set_estado_anim("Slashing", forzar=True)
        else:
            enemigo._set_estado_anim("idle")

        return NodoEstado.EXITO


class AccionPatrullarFantasma(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        tiempo_actual = pygame.time.get_ticks()

        if (enemigo.destino_patrulla is None or
                tiempo_actual - enemigo.ultimo_cambio_patrulla > 4000):
            enemigo._elegir_nuevo_destino_patrulla(mapa)

        if (tiempo_actual - enemigo.ultimo_calculo_astar > enemigo.intervalo_astar and
                enemigo.destino_patrulla is not None):
            enemigo.ultimo_calculo_astar = tiempo_actual
            enemigo._calcular_ruta_a(enemigo.destino_patrulla, mapa, cfg)

        if enemigo.destino_patrulla is None:
            enemigo._set_estado_anim("idle")
            return NodoEstado.EXITO

        enemigo.mover_por_camino(mapa)

        dx = enemigo.destino_patrulla[0] - enemigo.shape.centerx
        dy = enemigo.destino_patrulla[1] - enemigo.shape.centery
        if math.sqrt(dx*dx + dy*dy) < mapa.tile_size:
            enemigo.destino_patrulla = None
            enemigo._set_estado_anim("idle")
        else:
            enemigo._set_estado_anim("Walking")

        return NodoEstado.EXITO

# aplicadoo el astar par detectar y perseguir al personaje del fantasma
class AccionTauntYPerseguir(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        tiempo_actual = pygame.time.get_ticks()

        if enemigo._distancia_al_jugador(jugador) <= enemigo.rango_disparo:
            enemigo.taunt_hecho = False
            return NodoEstado.FALLO

        if not enemigo.taunt_hecho:
            enemigo._set_estado_anim("Taunt", forzar=True)
            enemigo.taunt_hecho         = True
            enemigo.taunt_tiempo_inicio = tiempo_actual
            return NodoEstado.EXITO

        duracion_taunt = len(enemigo.animaciones.get("Taunt", [1])) * 100
        if tiempo_actual - enemigo.taunt_tiempo_inicio < duracion_taunt:
            enemigo._set_estado_anim("Taunt")
            return NodoEstado.EXITO

        if tiempo_actual - enemigo.ultimo_calculo_astar > enemigo.intervalo_astar:
            enemigo.ultimo_calculo_astar = tiempo_actual
            enemigo.actualizar_camino(jugador, mapa, cfg)

        enemigo.mover_por_camino(mapa)
        enemigo.actualizar_flip(jugador.shape.centerx - enemigo.shape.centerx)
        enemigo._set_estado_anim("Walking")
        return NodoEstado.EXITO

    def reset(self, enemigo):
        enemigo.taunt_hecho = False

# solo para el enmigo fantasma 
class AccionDisparar(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        tiempo_actual = pygame.time.get_ticks()
        enemigo.actualizar_flip(jugador.shape.centerx - enemigo.shape.centerx)
        if tiempo_actual - enemigo.ultimo_ataque >= enemigo.cooldown_disparo:
            enemigo.ultimo_ataque = tiempo_actual
            angulo = enemigo._angulo_hacia_jugador(jugador)
            rad    = math.radians(angulo)
            bx = enemigo.shape.centerx + math.cos(rad) * (enemigo.shape.width  * 1.2)
            by = enemigo.shape.centery + math.sin(rad) * (enemigo.shape.height * 1.2)
            enemigo.proyectiles.append(
                BulletEnemigo(enemigo.imagen_proyectil, bx, by, angulo)
            )
            enemigo._set_estado_anim("Casting Spells", forzar=True)
        else:
            enemigo._set_estado_anim("Attacking")

        return NodoEstado.EXITO


class AccionHuir(Nodo):
    def ejecutar(self, enemigo, jugador, mapa, cfg):
        enemigo.taunt_hecho = False

        dx   = enemigo.shape.centerx - jugador.shape.centerx
        dy   = enemigo.shape.centery - jugador.shape.centery
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            enemigo.movimiento(int((dx/dist)*enemigo.velocidad),
                               int((dy/dist)*enemigo.velocidad), mapa)
        enemigo.actualizar_flip(jugador.shape.centerx - enemigo.shape.centerx)
        enemigo._set_estado_anim("Walking")
        return NodoEstado.EXITO

# clase enemigo base para los enemigos donde agrego las funciones que nececito que no estan en mi clase personaje
# y donde llamo los estado de arbol de comportamiento que comporte los enemigos Nicaury Diaz 
class Enemigo(Personaje):

    def __init__(self, x, y, animaciones, vida, velocidad, rango_deteccion):
        super().__init__(x, y, animaciones)
        self.vida                   = vida
        self.vida_max               = vida
        self.camino                 = []
        self.intervalo_astar        = 800
        self.ultimo_calculo_astar   = random.randint(0, 800)
        self.velocidad              = velocidad
        self.rango_deteccion        = rango_deteccion
        self.ultimo_ataque          = 0
        self.vivo                   = True

        self._estado_anim_actual    = "idle"
        self.recibio_golpe          = False
        self.destino_patrulla       = None
        self.ultimo_cambio_patrulla = random.randint(0, 4000)
        self.arbol                  = None

    def _set_estado_anim(self, estado, forzar=False):
        if (forzar or estado != self._estado_anim_actual) and estado in self.animaciones:
            self._estado_anim_actual = estado
            self.estado              = estado
            self.frame_index         = 0

    def _distancia_al_jugador(self, jugador):
        dx = jugador.shape.centerx - self.shape.centerx
        dy = jugador.shape.centery - self.shape.centery
        return math.sqrt(dx*dx + dy*dy)

    def _angulo_hacia_jugador(self, jugador):
        dx = jugador.shape.centerx - self.shape.centerx
        dy = jugador.shape.centery - self.shape.centery
        return math.degrees(math.atan2(dy, dx))

    def _elegir_nuevo_destino_patrulla(self, mapa):
        self.ultimo_cambio_patrulla = pygame.time.get_ticks()
        for _ in range(20):
            radio = random.randint(3, 8)
            ang   = random.uniform(0, 2 * math.pi)
            tx    = max(0, min(int(self.shape.centerx // mapa.tile_size + math.cos(ang)*radio), mapa.ancho_tiles-1))
            ty    = max(0, min(int(self.shape.centery // mapa.tile_size + math.sin(ang)*radio), mapa.alto_tiles-1))
            test  = pygame.Rect(tx*mapa.tile_size+1, ty*mapa.tile_size+1,
                                self.shape.width-2,  self.shape.height-2)
            if not mapa.verificar_colision(test, 0, 0):
                self.destino_patrulla = (tx*mapa.tile_size + mapa.tile_size//2,
                                         ty*mapa.tile_size + mapa.tile_size//2)
                return
        self.destino_patrulla = None

    def _calcular_ruta_a(self, destino_px, mapa, cfg):
        from Tiled_files.templo import MapaEstado, Astar
        ex = max(0, min(int(self.shape.centerx // mapa.tile_size), mapa.ancho_tiles-1))
        ey = max(0, min(int(self.shape.centery // mapa.tile_size), mapa.alto_tiles-1))
        dx = max(0, min(int(destino_px[0]      // mapa.tile_size), mapa.ancho_tiles-1))
        dy = max(0, min(int(destino_px[1]      // mapa.tile_size), mapa.alto_tiles-1))
        if ex == dx and ey == dy:
            return
        camino_raw, _ = Astar(MapaEstado(cfg,[ex,ey]), MapaEstado(cfg,[dx,dy]))
        self.camino = camino_raw

    def actualizar_camino(self, jugador, mapa, cfg):
        from Tiled_files.templo import MapaEstado, Astar
        ex = max(0, min(int(self.shape.centerx    // mapa.tile_size), mapa.ancho_tiles-1))
        ey = max(0, min(int(self.shape.centery    // mapa.tile_size), mapa.alto_tiles-1))
        jx = max(0, min(int(jugador.shape.centerx // mapa.tile_size), mapa.ancho_tiles-1))
        jy = max(0, min(int(jugador.shape.centery // mapa.tile_size), mapa.alto_tiles-1))
        if ex == jx and ey == jy:
            return
        camino_raw, _ = Astar(MapaEstado(cfg,[ex,ey]), MapaEstado(cfg,[jx,jy]))
        self.camino = camino_raw

    def mover_por_camino(self, mapa):
        if len(self.camino) < 2:
            return
        siguiente = self.camino[1]
        destino_x = siguiente.cordenadas[0] * mapa.tile_size + mapa.tile_size // 2
        destino_y = siguiente.cordenadas[1] * mapa.tile_size + mapa.tile_size // 2
        dx   = destino_x - self.shape.centerx
        dy   = destino_y - self.shape.centery
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < self.velocidad:
            self.shape.centerx = destino_x
            self.shape.centery = destino_y
            self.camino.pop(0)
        else:
            self.movimiento(int((dx/dist)*self.velocidad),
                            int((dy/dist)*self.velocidad), mapa)

    def recibir_danio(self, cantidad):
        self.vida -= cantidad
        self.recibio_golpe = True
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False

    def update(self, estado=None):
        if estado and estado in self.animaciones and estado != self.estado:
            self.estado      = estado
            self.frame_index = 0
        if pygame.time.get_ticks() - self.update_time > 100:
            self.frame_index += 1
            if self.frame_index >= len(self.animaciones[self.estado]):
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.estado][self.frame_index]

    def _draw_barra_vida(self, surface, mapa):
        bx = self.shape.centerx + mapa.offset_x - 20
        by = self.shape.top     + mapa.offset_y - 8
        ancho_total = 40
        ancho_vida  = int(ancho_total * max(self.vida, 0) / self.vida_max)
        pygame.draw.rect(surface, (180, 0,   0), (bx, by, ancho_total, 5))
        pygame.draw.rect(surface, (0,   200, 0), (bx, by, ancho_vida,  5))

    def draw(self, surface, mapa):
        if not self.vivo:
            return
        super().draw(surface, mapa)
        self._draw_barra_vida(surface, mapa)

    def update_enemigo(self, jugador, mapa, configuracion_grid):
        raise NotImplementedError

# clase enemigo de ataque cuerpo a cuerpo donde le añado los estado que solo necesita este enemigo y le herredo la clase enmigo base 
class Enemigoesqueleto(Enemigo):

    def __init__(self, x, y, animaciones):
        super().__init__(
            x, y, animaciones,
            vida            = constante.VIDA_ENEMIGO_ESQUELETO,
            velocidad       = constante.VELOCIDAD_ENEMIGO_ESQUELETO,
            rango_deteccion = constante.RANGO_DETECCION_ENEMIGO,
        )
        self.rango_ataque    = constante.RANGO_ATAQUE_ESQUELETO
        self.cooldown_ataque = constante.COOLDOWN_ATAQUE_ENEMIGO

        self.arbol = Selector([
            Secuencia([CondicionMuerto(),
                       AccionMorir()]),
            Secuencia([CondicionRecibioGolpe(),
                       AccionHurt()]),
            Secuencia([CondicionDetectaJugador(),
                       CondicionEnRangoAtaqueEsqueleto(),
                       AccionAtacarEsqueleto()]),
            Secuencia([CondicionDetectaJugador(),
                       AccionPerseguir()]),
            AccionPatrullar(),
        ])

    def update_enemigo(self, jugador, mapa, configuracion_grid):
        self.arbol.ejecutar(self, jugador, mapa, configuracion_grid)
        self.update(self._estado_anim_actual)

    def draw(self, surface, mapa):
        if not self.vivo:
            return
        super().draw(surface, mapa)

# clase enemigo de ataque a distancia  donde le añado los estado que solo necesita este enemigo y le herredo la clase enmigo base 
class Enemigofantasma(Enemigo):

    def __init__(self, x, y, animaciones, imagen_proyectil):
        super().__init__(
            x, y, animaciones,
            vida            = constante.VIDA_ENEMIGO_DISTANCIA,
            velocidad       = constante.VELOCIDAD_ENEMIGO_DISTANCIA,
            rango_deteccion = constante.RANGO_DETECCION_ENEMIGO,
        )
        self.imagen_proyectil = imagen_proyectil
        self.rango_disparo    = constante.RANGO_DISPARO_ENEMIGO
        self.rango_huida      = constante.RANGO_HUIDA_ENEMIGO
        self.cooldown_disparo = constante.COOLDOWN_DISPARO_ENEMIGO
        self.proyectiles      = []

        self.taunt_hecho         = False
        self.taunt_tiempo_inicio = 0

        self.arbol = Selector([
            Secuencia([CondicionMuerto(),
                       AccionMorir()]),
            Secuencia([CondicionRecibioGolpe(),
                       AccionHurt()]),
            Secuencia([CondicionDetectaJugador(),
                      CondicionDemasiadoCerca(),
                      AccionHuir()]),
            Secuencia([CondicionDetectaJugador(),
                       CondicionEnRangoDisparo(),
                       AccionDisparar()]),
            Secuencia([CondicionDetectaJugador(),
                       AccionTauntYPerseguir()]),
            AccionPatrullarFantasma(),
        ])

    def update_enemigo(self, jugador, mapa, configuracion_grid):
        if self._distancia_al_jugador(jugador) > self.rango_deteccion:
            self.taunt_hecho = False
       
        self.arbol.ejecutar(self, jugador, mapa, configuracion_grid)
        self.update(self._estado_anim_actual)

    def update_proyectiles(self, mapa, jugador):
        for p in self.proyectiles[:]:
            p.update(mapa, jugador)
            if p.muerto:
              self.proyectiles.remove(p)

    def draw(self, surface, mapa):
        if not self.vivo:
            return
        super().draw(surface, mapa)
        for p in self.proyectiles:
            p.draw(surface, mapa)


class BulletEnemigo(pygame.sprite.Sprite):

    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image.convert_alpha()
        self.angulo = angle
        self.image  = pygame.transform.rotate(self.original_image, -self.angulo)
        self.rect   = self.image.get_rect()
        self.rect.center = (x, y)
        self.shape  = self.rect
        self.velocidad = constante.VELOCIDAD_PROYECTIL_ENEMIGO
        rad = math.radians(self.angulo)
        self.delta_x = self.velocidad * math.cos(rad)
        self.delta_y = self.velocidad * math.sin(rad)
        self.frames_vivo = 0
        self.muerto = False

    def update(self, mapa, jugador):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        self.shape   = self.rect
        self.frames_vivo += 1

        if self.frames_vivo > 3 and mapa.verificar_colision(self.shape, 0, 0):
            self.muerto = True
            return

        if self.frames_vivo > 3 and self.rect.colliderect(jugador.shape):
            jugador.recibir_danio(constante.DAÑO_PROYECTIL_ENEMIGO)
            self.muerto = True
            return

        if (self.rect.right  < 0 or self.rect.left   > mapa.ancho_px or
                self.rect.bottom < 0 or self.rect.top    > mapa.alto_px):
            self.muerto = True

    def draw(self, ventana, mapa):
        ventana.blit(self.image,
                     (self.rect.x + mapa.offset_x,
                      self.rect.y + mapa.offset_y))