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
            
        self.shape = self.image.get_rect(center=(x, y))
        self.vida = 100

    def movimiento(self, dx, dy, mapa):
        if dx != 0:
            self.shape.x += dx
            if self.colision(mapa): self.shape.x -= dx
            self.flip = dx < 0

        if dy != 0:
            self.shape.y += dy
            if self.colision(mapa): self.shape.y -= dy

        grid_x, grid_y = self.shape.centerx // mapa.tile_size, self.shape.centery // mapa.tile_size
        if 0 <= grid_x < mapa.ancho and 0 <= grid_y < mapa.alto:
            if mapa.matriz[grid_y][grid_x] == 9 and mapa.estado_trampa == 1:
                self.vida -= 1
                
    def colision(self, mapa):
        grid_x = self.shape.centerx // mapa.tile_size
        grid_y = self.shape.centery // mapa.tile_size

        if 0 <= grid_x < mapa.ancho and 0 <= grid_y < mapa.alto:
            return mapa.matriz[grid_y][grid_x] in [1, 3, 6, 7, 8, 10]
        return False

    def update(self, estado="idle"):
        if self.animaciones and estado in self.animaciones:
            if estado != self.estado:
                self.estado = estado
                self.frame_index = 0

            if pygame.time.get_ticks() - self.update_time > 100:
                self.frame_index = (self.frame_index + 1) % len(self.animaciones[self.estado])
                self.update_time = pygame.time.get_ticks()
            self.image = self.animaciones[self.estado][self.frame_index]

    def draw(self, surface, camara):
        rect = pygame.Rect(self.shape.x - camara.offset_x, self.shape.y - camara.offset_y, self.shape.width, self.shape.height)
        surface.blit(pygame.transform.flip(self.image, self.flip, False), rect)

class Weapon():
    def __init__(self, image, imagen_poder_baston1, weapon_length=40): 
        self.imagen_poder_baston1 = imagen_poder_baston1
        self.imagen_arma = image
        self.angulo = 0
        self.imagen = self.imagen_arma
        self.shape = self.imagen.get_rect() 
        self.disparada = False
        self.weapon_length = weapon_length

    def update(self, player, camara):  
        poder = None

        # Posicionar el arma en la mano del personaje
        self.shape.center = player.shape.center
        
        # Ajustar offset para que el arma esté en la mano
        if player.flip:
            # Mirando hacia la izquierda - arma en la mano izquierda
            offset_x = player.shape.width * 0.3
            offset_y = -player.shape.height * 0.1
        else:
            # Mirando hacia la derecha - arma en la mano derecha
            offset_x = -player.shape.width * 0.3
            offset_y = -player.shape.height * 0.1

        self.shape.x += offset_x
        self.shape.y += offset_y

        # Calcular el ángulo hacia el mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] + camara.offset_x
        mouse_y = mouse_pos[1] + camara.offset_y
        
        distancia_x = mouse_x - self.shape.centerx        
        distancia_y = mouse_y - self.shape.centery    

        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))
        self.rotar_arma(player.flip)
        
        # Detectar los clicks para disparar el poder del baston
        if pygame.mouse.get_pressed()[0]:
            tiempo_actual = pygame.time.get_ticks()
            if not self.disparada and tiempo_actual >= getattr(self, 'cooldown_time', 0):  
                self.cooldown_time = tiempo_actual + constante.COOLDOWN_PODER_BASTON1 
                self.disparada = True  
            
                # Calcular posición de la bala en la punta del arma
                rad = math.radians(self.angulo)
                bullet_x = self.shape.centerx + math.cos(rad) * self.weapon_length
                bullet_y = self.shape.centery + math.sin(rad) * self.weapon_length
                
                poder = Bullet(
                    self.imagen_poder_baston1,
                    bullet_x,  
                    bullet_y,  
                    self.angulo
                )
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
             
    def draw(self, surface, camara):
        rect = camara.aplicar(self)
        surface.blit(self.imagen, rect)

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

    def update(self):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        self.shape = self.rect

        if hasattr(constante, 'ANCHO_MAPA_PIXELES') and hasattr(constante, 'ALTO_MAPA_PIXELES'):
            if (self.rect.right < 0 or 
                self.rect.left > constante.ANCHO_MAPA_PIXELES or 
                self.rect.bottom < 0 or 
                self.rect.top > constante.ALTO_MAPA_PIXELES):
                self.kill()
      
    def draw(self, ventana, camara):
        rect = camara.aplicar(self)
        ventana.blit(self.image, rect)