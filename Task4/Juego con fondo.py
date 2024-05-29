import pygame
import random
import os
import platform

# Inicializar Pygame
pygame.init()

# # Función para intentar inicializar el mezclador de sonido con diferentes controladores
# def init_mixer():
#     # Definir los controladores según el sistema operativo
#     system = platform.system()
#     if system == 'Windows':
#         # Windows
#         audio_drivers = ['directsound', 'waveout', 'disk']
#     elif system == 'Linux':
#         # Linux
#         audio_drivers = ['alsa', 'pulseaudio', 'esd', 'arts', 'disk']
#     elif system == 'Darwin':
#         # macOS
#         audio_drivers = ['coreaudio', 'disk']
#     else:
#         # Otros (intentar con el controlador por defecto y 'disk')
#         audio_drivers = ['disk']
    
#     for driver in audio_drivers:
#         try:
#             os.environ['SDL_AUDIODRIVER'] = driver
#             pygame.mixer.init()
#             print(f"Mezclador de sonido inicializado con el controlador: {driver}")
#             return
#         except pygame.error as e:
#             print(f"No se pudo inicializar el mezclador de sonido con el controlador {driver}: {e}")
#     print("No se pudo inicializar el mezclador de sonido con ningún controlador disponible.")

# # Intentar inicializar el mezclador de sonido
# init_mixer()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Ruta base
base_path = os.path.dirname(__file__)

# Cargar el sonido de explosión
explosion_sound = pygame.mixer.Sound(os.path.join(base_path, "assets/pinchazo-globo-revienta-.mp3"))


# Definir las dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Cargar la imagen de fondo
fondo = pygame.image.load(os.path.join(base_path, "assets/foto fondo videojuego.jpg"))
fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Definir la clase para los globos
class Globo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Elegir un color aleatorio para el globo
        self.color = random.choice([AZUL, VERDE, ROJO])
        # Cargar la imagen del globo según el color
        if self.color == AZUL:
            self.image = pygame.image.load(os.path.join(base_path, "assets/Globo azul sin fondo.png")).convert_alpha()
        elif self.color == VERDE:
            self.image = pygame.image.load(os.path.join(base_path, "assets/Globo verde.png")).convert_alpha()
        elif self.color == ROJO:
            self.image = pygame.image.load(os.path.join(base_path, "assets/Globo rojo.png")).convert_alpha()
        # Escalar la imagen del globo
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajusta el tamaño según sea necesario
        self.rect = self.image.get_rect()
        # Colocar el globo en una posición aleatoria
        self.rect.x = random.randrange(ANCHO_PANTALLA)
        self.rect.y = random.randrange(ALTO_PANTALLA)
        # Velocidad del globo
        self.velocidad_y = random.randrange(1, 3)
        # Asignar puntos según el color del globo
        if self.color == AZUL:
            self.puntos = 1
        elif self.color == VERDE:
            self.puntos = 2
        elif self.color == ROJO:
            self.puntos = -2

    def update(self):
        # Mover el globo hacia arriba
        self.rect.y -= self.velocidad_y
        # Si el globo sale de la pantalla, resetear su posición
        if self.rect.y < -30:
            self.rect.y = ALTO_PANTALLA + 30
            self.rect.x = random.randrange(ANCHO_PANTALLA)

# Inicializar la pantalla
pantalla = pygame.display.set_mode([ANCHO_PANTALLA, ALTO_PANTALLA])
pygame.display.set_caption("Explota los globos")

# Lista de todos los sprites
todos_los_sprites = pygame.sprite.Group()

# Lista de los globos
globos = pygame.sprite.Group()

# Crear los globos
for i in range(50):
    globo = Globo()
    todos_los_sprites.add(globo)
    globos.add(globo)

# Loop principal
hecho = False
reloj = pygame.time.Clock()

puntuacion = 0

while not hecho:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True

    # Dibujar el fondo
    pantalla.blit(fondo, (0, 0))

    # Actualizar todos los sprites
    todos_los_sprites.update()

    # Detectar colisiones entre el jugador y los globos
    pos = pygame.mouse.get_pos()
    jugador_rect = pygame.Rect(pos[0], pos[1], 1, 1)
    for globo in globos:
        if globo.rect.colliderect(jugador_rect):
            puntuacion += globo.puntos
            if explosion_sound:
                explosion_sound.play()  # Reproducir el sonido de explosión si está disponible
            globos.remove(globo)
            todos_los_sprites.remove(globo)
            # Crear un nuevo globo
            nuevo_globo = Globo()
            todos_los_sprites.add(nuevo_globo)
            globos.add(nuevo_globo)

    # Dibujar todos los sprites
    todos_los_sprites.draw(pantalla)

    # Mostrar la puntuación
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render("Puntuación: " + str(puntuacion), True, BLANCO)
    pantalla.blit(texto, [10, 10])

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
