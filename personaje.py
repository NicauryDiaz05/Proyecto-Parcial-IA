import pygame 
import constante
import math
import constante

class Personaje:
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        self.estado = "idle"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.estado][self.frame_index]
        self.shape = self.image.get_rect(center=(x, y))

        self.camino_astar = []
        self.indice_camino = 0
        self.auto_seguir = False

    def establecer_camino(self, camino):
        self.camino_astar = camino
        self.indice_camino = 0

    def seguir_camino_astar(self, mapa):
        if not self.auto_seguir or self.indice_camino >= len(self.camino_astar):
            return

        objetivo = self.camino_astar[self.indice_camino]
        obj_x = objetivo.cordenadas[1]*32 + 16
        obj_y = objetivo.cordenadas[0]*32 + 16

        dx = obj_x - self.shape.centerx
        dy = obj_y - self.shape.centery
        dist = math.hypot(dx, dy)

        if dist < 5:
            self.indice_camino += 1
            return

        dx = int((dx/dist)*constante.VELOCIDAD)
        dy = int((dy/dist)*constante.VELOCIDAD)
        self.movimiento(dx, dy, mapa)

    def movimiento(self, dx, dy, mapa):

        if dx != 0:
            self.shape.x += dx
            if self.colision(mapa):
                self.shape.x -= dx
            self.flip = dx < 0

        if dy != 0:
            self.shape.y += dy
            if self.colision(mapa):
                self.shape.y -= dy

    def colision(self, mapa):
        for y in range(len(mapa)):
            for x in range(len(mapa[0])):
                if mapa[y][x] == 1:
                    tile_rect = pygame.Rect(x*32, y*32, 32, 32)
                    if self.shape.colliderect(tile_rect):
                        return True
        return False

    def update(self, estado="idle"):
        if estado != self.estado:
            self.estado = estado
            self.frame_index = 0

        if pygame.time.get_ticks() - self.update_time > 100:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones[self.estado])
            self.update_time = pygame.time.get_ticks()

        self.image = self.animaciones[self.estado][self.frame_index]

    def draw(self, surface, camara):
        rect = camara.aplicar(self)
        surface.blit(pygame.transform.flip(self.image, self.flip, False), rect)


class Weapon():
    def __init__(self, image, imagen_poder_baston1):
        self.imagen_poder_baston1 = imagen_poder_baston1
        self.imagen_arma = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_arma, self.angulo)
        self.shape = self.imagen.get_rect() 
        self.disparada = False

        self.weapon_length = 40  

    def update(self, player, camara):  
        
        poder = None

        # posicionar el arma en el centro del personaje
        self.shape.center = player.shape.center 

        if player.flip == False:
            self.shape.x += player.shape.width / 4.5
            self.shape.y += player.shape.height / 4.5
        else:
            self.shape.x -= player.shape.width / 4.5
            self.shape.y += player.shape.height / 4.5

        # calcular el ángulo hacia el mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] + camara.offset_x
        mouse_y = mouse_pos[1] + camara.offset_y
        
        distancia_x = mouse_x - self.shape.centerx
        distancia_y = mouse_y - self.shape.centery

        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))
        self.rotar_arma(player.flip)
        
        # dectar los clicks para disparar el poder del baston
        if pygame.mouse.get_pressed()[0]:
            if self.disparada == False:
                # calcular posición de la bala en la punta del arma
                rad = math.radians(self.angulo)
                bullet_x = self.shape.centerx + math.cos(rad) * self.weapon_length
                bullet_y = self.shape.centery + math.sin(rad) * self.weapon_length
                
                poder = Bullet(
                    self.imagen_poder_baston1,
                    bullet_x,  
                    bullet_y,  
                    self.angulo
                )
                self.disparada = True
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

        # calcular velocidad en x e y
        rad = math.radians(self.angulo)
        self.delta_x = self.velocidad * math.cos(rad)
        self.delta_y = self.velocidad * math.sin(rad)

    def update(self):
       
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        # actualizar shape para colisiones
        self.shape = self.rect

        # Eliminar bala si sale de la pantalla o del mapa
        if hasattr(constante, 'ANCHO_MAPA_PIXELES') and hasattr(constante, 'ALTO_MAPA_PIXELES'):
            if (self.rect.right < 0 or 
                self.rect.left > constante.ANCHO_MAPA_PIXELES or 
                self.rect.bottom < 0 or 
                self.rect.top > constante.ALTO_MAPA_PIXELES):
                self.kill()
      
    def draw(self, ventana, camara):
       
        rect = camara.aplicar(self)
        ventana.blit(self.image, rect)
