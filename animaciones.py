
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
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Running//0_Dark_Oracle_Running_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["running"].append(img)

# WALKING
animaciones["walking"] = []
for i in range(23):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Walking//0_Dark_Oracle_Walking_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["walking"].append(img)

# IDLE
animaciones["idle"] = []
for i in range(17):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Idle//0_Dark_Oracle_Idle_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["idle"].append(img)

# IDLE BLINKING
animaciones["idle_blink"] = []
for i in range(17):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Idle Blinking//0_Dark_Oracle_Idle Blinking_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["idle_blink"].append(img)

# HURT
animaciones["hurt"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Hurt//0_Dark_Oracle_Hurt_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["hurt"].append(img)

# DYING
animaciones["dying"] = []
for i in range(14):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Dying//0_Dark_Oracle_Dying_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["dying"].append(img)

# FALLING DOWN
animaciones["falling"] = []
for i in range(5):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Falling Down//0_Dark_Oracle_Falling Down_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["falling"].append(img)

# JUMP START
animaciones["jump_start"] = []
for i in range(5):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Jump Start//0_Dark_Oracle_Jump Start_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["jump_start"].append(img)

# JUMP LOOP
animaciones["jump_loop"] = []
for i in range(5):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Jump Loop//0_Dark_Oracle_Jump Loop_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["jump_loop"].append(img)

# KICKING
animaciones["kicking"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Kicking//0_Dark_Oracle_Kicking_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["kicking"].append(img)

# SLASHING
animaciones["slashing"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Slashing//0_Dark_Oracle_Slashing_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["slashing"].append(img)

# SLASHING IN THE AIR
animaciones["slash_air"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Slashing in The Air//0_Dark_Oracle_Slashing in The Air_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["slash_air"].append(img)

# SLIDING
animaciones["sliding"] = []
for i in range(5):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Sliding//0_Dark_Oracle_Sliding_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["sliding"].append(img)

# THROWING
animaciones["throwing"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Throwing//0_Dark_Oracle_Throwing_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["throwing"].append(img)

# THROWING IN THE AIR
animaciones["throw_air"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Throwing in The Air//0_Dark_Oracle_Throwing in The Air_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["throw_air"].append(img)

# RUN SLASHING
animaciones["run_slash"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Run Slashing//0_Dark_Oracle_Run Slashing_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["run_slash"].append(img)

# RUN THROWING
animaciones["run_throw"] = []
for i in range(11):
   img = pygame.image.load(f"player_heroe//Dark_Oracle_3//PNG//PNG Sequences//Run Throwing//0_Dark_Oracle_Run Throwing_{i:03}.png")
   img = escala_img(img, constante.SCALA_PERSONAJE)
   animaciones["run_throw"].append(img)


   