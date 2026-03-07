
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


# RUN THROWING
animaciones["run_throw"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//Run Throwing//0_Dark_Oracle_Run Throwing_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["run_throw"].append(img)


   



 # animaciones de enemigos 1 y 2,escalas de imagenes Nicaury Diaz 23-SISN-2-028

# Attacking
animacionesenemigo1 = {}
animacionesenemigo1["Attacking"] = []
for i in range(11):
   img = pygame.image.load(f"enemigos//fantasma//Wraith_03//Attacking//Wraith_03_Attack_{i:03}.png")
   img = escala_img(img, constante.SCALA_ENEMIGO)
   animacionesenemigo1["Attacking"].append(img)

# IDLE
animacionesenemigo1["idle"] = []
for i in range(11):
   img = pygame.image.load(f"enemigos//fantasma//Wraith_03//idle//Wraith_03_idle_{i:03}.png")
   img = escala_img(img, constante.SCALA_ENEMIGO)
   animacionesenemigo1["idle"].append(img)

# HURT
animacionesenemigo1["Hurt"] = []
for i in range(11):
   img = pygame.image.load(f"enemigos//fantasma//Wraith_03//Hurt//Wraith_03_Hurt_{i:03}.png")
   img = escala_img(img, constante.SCALA_ENEMIGO)
   animacionesenemigo1["Hurt"].append(img)

# Dying 
animacionesenemigo1["Dying"] = []
for i in range(14):
   img = pygame.image.load(f"enemigos//fantasma//Wraith_03//Dying//Wraith_03_Dying_{i:03}.png")
   img = escala_img(img, constante.SCALA_ENEMIGO)
   animacionesenemigo1["Dying"].append(img)

#Casting Spells
animacionesenemigo1["Casting Spells"] = []
for i in range(17):
   img = pygame.image.load(f"enemigos//fantasma//Wraith_03//Casting Spells//Wraith_03_Casting Spells_{i:03}.png")
   img = escala_img(img, constante.SCALA_ENEMIGO)
   animacionesenemigo1["Casting Spells"].append(img)

# Taunt
animacionesenemigo1["Taunt"] = []
for i in range(17):
   img = pygame.image.load(f"enemigos//fantasma//Wraith_03//Taunt//Wraith_03_Taunt_{i:03}.png")
   img = escala_img(img, constante.SCALA_ENEMIGO)
   animacionesenemigo1["Taunt"].append(img)

# Walking
animacionesenemigo1["Walking"] = []
for i in range(11):
   img = pygame.image.load(f"enemigos//fantasma//Wraith_03//Walking//Wraith_03_Moving Forward_{i:03}.png")
   img = escala_img(img, constante.SCALA_ENEMIGO)
   animacionesenemigo1["Walking"].append(img)


# Dying
animacionesenemigo2 = {}
animacionesenemigo2["Dying"] = []
for i in range(14):
   img = pygame.image.load(f"enemigos//esqueletos//Skeleton_Warrior//Dying//0_Skeleton_Warrior_Dying_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animacionesenemigo2["Dying"].append(img)

# IDLE
animacionesenemigo2["idle"] = []
for i in range(17):
   img = pygame.image.load(f"enemigos//esqueletos//Skeleton_Warrior//idle//0_Skeleton_Warrior_idle_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animacionesenemigo2["idle"].append(img)

# HURT
animacionesenemigo2["Hurt"] = []
for i in range(11):
   img = pygame.image.load(f"enemigos//esqueletos//Skeleton_Warrior//Hurt//0_Skeleton_Warrior_Hurt_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animacionesenemigo2["Hurt"].append(img)

# Kicking
animacionesenemigo2["Kicking"] = []
for i in range(11):
   img = pygame.image.load(f"enemigos//esqueletos//Skeleton_Warrior//Kicking//0_Skeleton_Warrior_Kicking_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animacionesenemigo2["Kicking"].append(img)

# Running
animacionesenemigo2["Running"] = []
for i in range(11):
   img = pygame.image.load(f"enemigos//esqueletos//Skeleton_Warrior//Running//0_Skeleton_Warrior_Running_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animacionesenemigo2["Running"].append(img)

# Walking
animacionesenemigo2["Walking"] = []
for i in range(23):
   img = pygame.image.load(f"enemigos//esqueletos//Skeleton_Warrior//Walking//0_Skeleton_Warrior_Walking_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animacionesenemigo2["Walking"].append(img)

# SLASHING
animacionesenemigo2["Slashing"] = []
for i in range(11):
   img = pygame.image.load(f"enemigos//esqueletos//Skeleton_Warrior//Slashing//0_Skeleton_Warrior_Slashing_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animacionesenemigo2["Slashing"].append(img)






  