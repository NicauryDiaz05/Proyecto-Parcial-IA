
import pygame

import constante

# Importar imagenes Nicaury Diaz 23-SISN-2-028
def escala_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, size=(w*scale, h*scale))

# animaciones y escalas de imagenes Nicaury Diaz 23-SISN-2-028

# RUNNING
animaciones = {}
animaciones["running"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Running//0_Dark_Oracle_Running_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["running"].append(img)

# IDLE
animaciones["idle"] = []
for i in range(17):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Idle//0_Dark_Oracle_Idle_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["idle"].append(img)

# HURT
animaciones["hurt"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Hurt//0_Dark_Oracle_Hurt_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["hurt"].append(img)

# DYING
animaciones["dying"] = []
for i in range(14):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Dying//0_Dark_Oracle_Dying_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["dying"].append(img)

# KICKING
animaciones["kicking"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Kicking//0_Dark_Oracle_Kicking_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["kicking"].append(img)

# SLASHING
animaciones["slashing"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Slashing//0_Dark_Oracle_Slashing_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["slashing"].append(img)

# THROWING
animaciones["throwing"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Throwing//0_Dark_Oracle_Throwing_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["throwing"].append(img)

# THROWING IN THE AIR
animaciones["throw_air"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Throwing in The Air//0_Dark_Oracle_Throwing in The Air_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["throw_air"].append(img)


# RUN THROWING
animaciones["run_throw"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Run Throwing//0_Dark_Oracle_Run Throwing_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["run_throw"].append(img)


   