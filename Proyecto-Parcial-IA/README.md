# Proyecto-parcial-IA

## Nombre 
#Nicaury Carolina Diaz Amador 

## Matrícula
# 23-SISN-2-028

## Proyecto
#TEMPLO DE LAS SOMBRAS 

“El Templo de las Sombras”

https://youtu.be/d-VnIGhI36U - Video explicativo 

1. Concepto General

“El Templo de las Sombras” es un juego de exploración y supervivencia en el que el jugador debe escapar de un antiguo templo en ruinas mientras enfrenta enemigos inteligentes que patrullan las diferentes habitaciones.
El templo está dividido en múltiples salas conectadas por pasillos, puertas y zonas estratégicas. Cada decisión del jugador será clave para sobrevivir y encontrar la salida.

2. Mecánicas Principales

Exploración

* El jugador recorre diferentes habitaciones del templo.
* Cada habitación puede contener enemigos, obstáculos o rutas alternativas.
* El objetivo principal es encontrar la salida del templo.

Enfrentamiento

* El jugador puede:
* Enfrentar a los enemigos.
* Ocultarse.
* Evadirlos estratégicamente.

3. Inteligencia Artificial

Algoritmo A* (A Star)
* Se utilizará el algoritmo A* para:
* Encontrar la ruta más eficiente entre habitaciones.
* Permitir que los enemigos encuentren el camino más corto hacia el jugador.
* Guiar al jugador hacia objetivos específicos dentro del mapa.
* Esto permite que tanto enemigos como jugador tengan movimientos estratégicos realistas.

Árbol de Comportamiento – Enemigos

El comportamiento de los enemigos se definirá mediante un árbol de decisiones:

Estado 1: Patrullaje
* Si no detectan al jugador → Patrullan entre habitaciones.
* Se mueven usando A* para desplazarse entre puntos.

Estado 2: Detección
* Si ven al jugador → Cambian a modo persecución.

Estado 3: Persecución
* Usan A* para calcular la ruta más corta hacia el jugador.
* 
Estado 4: Ataque
* Si el jugador está dentro del rango → Atacan.

Árbol de Comportamiento – Jugador

* El jugador también tendrá decisiones estratégicas:
* Si el enemigo está lejos → Explorar.
* Si el enemigo está cerca → Decidir entre:
* Ocultarse.
* Enfrentarlo.
* Huir.

