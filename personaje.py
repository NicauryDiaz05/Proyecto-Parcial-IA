import pygame
import constante
import math

class Personaje:
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        self.estado = "idle"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        if self.animaciones and self.estado in self.animaciones:
            self.image = self.animaciones[self.estado][self.frame_index]
        else:
            self.image = pygame.Surface((32, 32))
            self.image.fill((0, 255, 0))

        rect_original = self.image.get_rect(center=(x, y))
        ancho_hitbox = rect_original.width * 0.5
        alto_hitbox = rect_original.height * 0.6
        self.shape = pygame.Rect(0, 0, ancho_hitbox, alto_hitbox)
        self.shape.center = rect_original.center

        self.vida_max = 100
        self.vida = self.vida_max
        self.vivo = True

        self.animaciones_bloqueantes = {
            "kicking", "slashing", "throwing", "throw_air", "run_throw", "hurt", "dying"
        }
        self.animacion_bloqueada = False

    def recibir_danio(self, cantidad):
        if not self.vivo:
            return
        self.vida -= cantidad
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            self.estado = "dying"
            self.frame_index = 0
            self.animacion_bloqueada = True
# curar al enemigo un 20 de vida cada vez que gane una oleada 
    def curar(self, cantidad):
        if not self.vivo:
            return
        self.vida = min(self.vida + cantidad, self.vida_max)

    def actualizar_flip(self, dx):
        if dx < 0:  
            self.flip = True
        elif dx > 0:  
            self.flip = False
   # movimiento del jugador     
    def movimiento(self, dx, dy, mapa):
        self.actualizar_flip(dx)

        original_x = self.shape.x
        original_y = self.shape.y

        self.shape.x += dx
        if mapa.verificar_colision(self.shape, 0, 0):
            self.shape.x = original_x

        self.shape.y += dy
        if mapa.verificar_colision(self.shape, 0, 0):
            self.shape.y = original_y

    def update(self, estado="idle"):
        if not self.animaciones:
            return

        if not self.vivo:
            self.estado = "dying"
            self.animacion_bloqueada = True
            if pygame.time.get_ticks() - self.update_time > 100:
                self.update_time = pygame.time.get_ticks()
                total_frames = len(self.animaciones["dying"])
                if self.frame_index < total_frames - 1:
                    self.frame_index += 1
            self.image = self.animaciones["dying"][self.frame_index]
            return

        keys        = pygame.key.get_pressed()
        mouse_click = pygame.mouse.get_pressed()[0]

        if not self.animacion_bloqueada:

            if keys[pygame.K_f]:
                estado = "kicking"

            elif keys[pygame.K_e]:
                estado = "slashing"

            elif keys[pygame.K_SPACE]:
                estado = "throw_air"

            elif mouse_click:
                estado = "run_throw" if estado == "running" else "throwing"

            if estado != self.estado and estado in self.animaciones:
                self.estado              = estado
                self.frame_index         = 0
                self.animacion_bloqueada = estado in self.animaciones_bloqueantes

        if pygame.time.get_ticks() - self.update_time > 100:
            self.frame_index += 1
            self.update_time  = pygame.time.get_ticks()

            total_frames = len(self.animaciones[self.estado])

            if self.frame_index >= total_frames:
                if self.estado == "dying":
                    self.frame_index = total_frames - 1
                else:
                    self.frame_index         = 0
                    self.animacion_bloqueada = False

        self.image = self.animaciones[self.estado][self.frame_index]

    def draw(self, surface, mapa):
        imagen = pygame.transform.flip(self.image, self.flip, False)

        rect_dibujo = imagen.get_rect(center=(
            self.shape.centerx + mapa.offset_x,
            self.shape.centery + mapa.offset_y
        ))

        surface.blit(imagen, rect_dibujo)
        self._draw_barra_vida(surface, mapa)
# dibujo la barra de vida 
    def _draw_barra_vida(self, surface, mapa):
        barra_ancho = 40
        barra_alto  = 5
        bx = self.shape.centerx + mapa.offset_x - barra_ancho // 2
        by = self.shape.top     + mapa.offset_y - 10

        relleno = int(barra_ancho * max(self.vida, 0) / self.vida_max)

        pygame.draw.rect(surface, (120, 0, 0), (bx, by, barra_ancho, barra_alto))

        if self.vida > 50:
            color = (0, 200, 0)
        elif self.vida > 25:
            color = (255, 165, 0)
        else:
            color = (220, 0, 0)

        pygame.draw.rect(surface, color, (bx, by, relleno, barra_alto))
        pygame.draw.rect(surface, (255, 255, 255), (bx, by, barra_ancho, barra_alto), 1)

    def atacar_cuerpo_a_cuerpo(self, enemigos, daño):
        for enemigo in enemigos:
         if enemigo.vivo and self.shape.colliderect(enemigo.shape):
            enemigo.recibir_danio(daño)

class Weapon():
    def __init__(self, image, imagen_poder_baston1, weapon_length=40):
        self.imagen_poder_baston1 = imagen_poder_baston1
        self.imagen_arma = image
        self.angulo = 0
        self.imagen = self.imagen_arma
        self.shape = self.imagen.get_rect()
        self.disparada = False
        self.weapon_length = weapon_length

    def update(self, player, mapa):
        poder = None
        self.shape.center = player.shape.center

        if player.flip:
            offset_x = player.shape.width * 0.10
            offset_y = -player.shape.height * -0.2
        else:
            offset_x = -player.shape.width * 0.10
            offset_y = -player.shape.height * -0.2

        if player.flip:
            mano_x = player.shape.centerx - offset_x
        else:
            mano_x = player.shape.centerx + offset_x

        mano_y = player.shape.centery + offset_y
        self.shape.center = (mano_x, mano_y)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_x -= mapa.offset_x
        mouse_y -= mapa.offset_y

        distancia_x = mouse_x - self.shape.centerx
        distancia_y = mouse_y - self.shape.centery

        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))
# limito el angulo de baston 
        if (distancia_x < 0 and not player.flip) or (distancia_x > 0 and player.flip):
            self.angulo = 90 if distancia_y > 0 else -90
            self.rotar_arma(player.flip)

        if pygame.mouse.get_pressed()[0]:
            tiempo_actual = pygame.time.get_ticks()
            if not self.disparada and tiempo_actual >= getattr(self, 'cooldown_time', 0):
                self.cooldown_time = tiempo_actual + constante.COOLDOWN_PODER_BASTON1
                self.disparada = True

                rad = math.radians(self.angulo)
                bullet_x = self.shape.centerx + math.cos(rad) * self.weapon_length
                bullet_y = self.shape.centery + math.sin(rad) * self.weapon_length

                poder = Bullet(self.imagen_poder_baston1, bullet_x, bullet_y, self.angulo)
        else:
            self.disparada = False

        return poder

    def rotar_arma(self, rotar):
        centro = self.shape.center

        if rotar:
            imagen_flip = pygame.transform.flip(self.imagen_arma, True, False)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_arma, False, False)

        self.imagen = pygame.transform.rotate(imagen_flip, -self.angulo)
        self.shape = self.imagen.get_rect(center=centro)

    def draw(self, surface, mapa):
        surface.blit(
            self.imagen,
            (self.shape.x + mapa.offset_x,
             self.shape.y + mapa.offset_y)
        )
# clase bala 
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)

        self.original_image = image.convert_alpha()
        self.angulo = angle

        self.image = pygame.transform.rotate(self.original_image, -self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.shape = self.rect

        self.velocidad = constante.VELOCIDAD_PODER

        rad = math.radians(self.angulo)
        self.delta_x = self.velocidad * math.cos(rad)
        self.delta_y = self.velocidad * math.sin(rad)

    def update(self, mapa, enemigos=None):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        self.shape = self.rect

        if mapa.verificar_colision(self.shape, 0, 0):
            self.kill()
            return

        if enemigos:
            for enemigo in enemigos:
                if enemigo.vivo and self.rect.colliderect(enemigo.shape):
                    enemigo.recibir_danio(constante.DAÑO_BASTON1)
                    self.kill()
                    return

        if (self.rect.right < 0 or
            self.rect.left > mapa.ancho_px or
            self.rect.bottom < 0 or
            self.rect.top > mapa.alto_px):
            self.kill()

    def draw(self, ventana, mapa):
        ventana.blit(
            self.image,
            (self.rect.x + mapa.offset_x,
             self.rect.y + mapa.offset_y)
        )