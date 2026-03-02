# Examen Parcial

**Valor:** 20 puntos  

**Fecha de entrega:** 09/03/2026  

**Fecha de presentación:** (12/13)/03/2026 y 14/03/2026

---

## Desarrollar un juego utilizando Pygame

El proyecto parcial consiste en realizar un *fork* del repositorio de GitHub donde se encuentra este archivo y, a partir de él, desarrollar un juego en el que el jugador deba interactuar con uno o más agentes en un entorno competitivo hasta ganar o perder. El juego debe incluir al menos un **Árbol de Comportamiento** y un algoritmo **A\***.

### Detalles:

- El juego se desarrollará utilizando las mecánicas del juego que se le asigne, pero no debe ser un clon de dicho juego, debe crear un juego diferente sobre esas mecánicas y debe estar programado por usted mismo.  

- Si utiliza un proyecto de Internet o uno entregado en cuatrimestres anteriores y lo hace pasar como suyo, **reprobará el parcial**.  

- Si sospecho plagio de algún tipo, tendrá que realizar una prueba compleja que solo podrá superar si el proyecto es suyo.  

- Deberá presentar el juego a personas que lo probarán frente a usted. Además, deberá explicar cómo funciona su proyecto y cómo está implementada la inteligencia artificial en él.  

- También deberá subir un video a YouTube de su juego explicando cómo lo desarrolló, el funcionamiento de los algoritmos en profundidad y mostrando cómo se juega.  
  - En el video debe aparecer usted en cámara explicando su proyecto mientras muestra el código y el juego en funcionamiento.  
  - La relación del video debe ser **16:9** y la resolución mínima debe ser **720p**.  

- Si un trabajo presenta **solo** el Árbol de Comportamiento o **solo** el A\*, se restarán **10 puntos** de la calificación.  
  Si no incluye ninguno de los dos, el proyecto valdrá **0**.  

- La estructura del proyecto debe ser la siguiente:

```plaintext
proyecto/
├── main.py
├── scripts/
│   ├── ...
│   ├── ...
├── assets/
│   ├── images/
│   ├── sounds/
│   ├── music/
├── requirements.txt
└── README.md
```

Más lo que ya incluía el repositorio original.  

- El Árbol de Comportamiento, el algoritmo A\* y, en general, toda la lógica de los agentes, debe estar implementada **desde cero**.  
  No se debe utilizar ninguna librería externa para esto.  
  **No se recibirán proyectos que incumplan este punto.**  

- El juego debe incluir el uso de **controles / gamepad**. Habrá 3 puntos extra por implementarlo.  

- El juego debe incluir **sonidos y música**. Esto es obligatorio.  
  Pueden ser descargados de Internet o generados por usted.  

- El juego debe incluir **sprites**, que pueden ser descargados de Internet, tomados de juegos famosos, creados por usted o generados con inteligencia artificial.  

- No puede ejecutar el juego en la presentación desde un entorno de desarrollo (IDE).  
  Debe ejecutarse desde la terminal o consola.  

- El juego debe contar con un **menú** que permita:  
  - **Iniciar el juego**  
  - **Reiniciar la partida** al terminar o perder  

- El juego debe ocupar la totalidad de la pantalla durante la presentación.  

- El **rendimiento del juego será evaluado**.  
  Si el rendimiento es deficiente, se aplicarán penalizaciones, lo mismo en caso de fallos.  

- Su juego debe estar en un repositorio de **GitHub** y debe contar con el historial de *commits* correspondiente al proyecto.  
  - Se evaluará el historial en caso de encontrar irregularidades.  
  - Se recomienda hacer *commits* con cada funcionalidad y cambio, con mensajes descriptivos.  
  - Utilizar Git para el proyecto es obligatorio. Si sube archivos manualmente al repositorio, no se evaluará su proyecto y la calificación será **0**.  


### Formato de entrega:

- El proyecto debe subirse en un archivo de texto plano "Nombre-matricula.txt", que debe contener:  
  - Su **nombre, matrícula y el enlace al repositorio de GitHub** y el enlace al **video**, que también debe estar en el repositorio.  

### Estructura del repositorio:

- Debe contener los scripts de Python, imágenes, sonidos o cualquier recurso necesario para ejecutar el proyecto.  
- No debe incluir archivos innecesarios que aumenten el tamaño del repositorio: rar, zip, binarios, etc.  
- Debe incluir un archivo `requirements.txt` con las librerías utilizadas.  
  - Este archivo permite instalar todas las dependencias con un solo comando.  
  - **Si no sabe qué es `requirements.txt`, investigue.**  
    No envíe un PDF con las librerías, ni un archivo que diga "las librerías usadas son:".  
    **Por el amor de Dios, investigue.**  

- Utilice un archivo `.gitignore` para evitar subir binarios y archivos innecesarios que aumenten el tamaño del repositorio.  

### Código y comentarios:

- Los scripts de Python deben contener **comentarios** que faciliten la lectura del código.  
- Cada script debe incluir un **comentario con su nombre y matrícula**.  

---

**El proyecto debe subirse a la carpeta de _Examen Parcial_ hasta el 09/03/2026 .**  
**Pasada esa fecha no se recibirán proyectos.**
