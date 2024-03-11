import pygame
import sys

class Vehiculo:
    def __init__(self, marca, motor, color, velocidad):
        self.marca = marca
        self.motor = motor
        self.color = color
        self.velocidad = velocidad
        self.mensaje = ""
        self.mostrar_mensaje = False
        self.tiempo_mensaje = 0

    def encender(self):
        print("Auto encendido")

    def acelerar(self):
        self.velocidad += 10
        if self.velocidad >= 120:
            self.mostrar_mensaje = True
            self.mensaje = "Cuidado con el exceso de velocidad"
        else:
            self.mostrar_mensaje = True
            self.mensaje = "Acelerando 10 km/hr"
        self.tiempo_mensaje = pygame.time.get_ticks()

    def frenar(self):
        if self.velocidad > 0:
            self.velocidad -= 5
            self.mostrar_mensaje = True
            self.mensaje = "Frenando 5 km/hr"
            self.tiempo_mensaje = pygame.time.get_ticks()
        else:
            self.mostrar_mensaje = True
            self.mensaje = "El vehículo ya está detenido"
            self.tiempo_mensaje = pygame.time.get_ticks()

    def obtener_velocidad(self):
        return "Velocidad: {} km/hr".format(self.velocidad)

# Inicialización de Pygame
pygame.init()

# Definición de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulador de Vehículo")

# Cargar imagen del fondo
fondo_imagen = pygame.image.load("road.jpg")
fondo_imagen = pygame.transform.scale(fondo_imagen, (ANCHO, ALTO))

# Cargar imagen del vehículo
vehiculo_imagen = pygame.image.load("car.png")
vehiculo_imagen = pygame.transform.scale(vehiculo_imagen, (200, 100))
vehiculo_rect = vehiculo_imagen.get_rect()
vehiculo_rect.bottom = ALTO - 120  # Colocar el vehículo un poco más arriba de la parte inferior de la ventana

# Crear instancia de Vehiculo
mi_coche = Vehiculo("Toyota", "Motor 2.0", "Rojo", 0)

# Crear objetos de fuente para los mensajes
fuente = pygame.font.SysFont(None, 24)

# Dimensiones y posición del recuadro para el mensaje
recuadro_mensaje_ancho = 300
recuadro_mensaje_alto = 50
recuadro_mensaje_x = (ANCHO - recuadro_mensaje_ancho) // 2
recuadro_mensaje_y = (ALTO - recuadro_mensaje_alto) // 2

# Dimensiones y posición del recuadro para la velocidad
recuadro_velocidad_ancho = 200
recuadro_velocidad_alto = 30
recuadro_velocidad_x = (ANCHO - recuadro_velocidad_ancho) // 2
recuadro_velocidad_y = recuadro_mensaje_y - 50

# Reloj para controlar la velocidad de actualización de la pantalla
reloj = pygame.time.Clock()

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Lógica del juego
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        mi_coche.acelerar()
    elif keys[pygame.K_DOWN]:
        mi_coche.frenar()

    # Actualización de la posición del vehículo
    vehiculo_rect.x += mi_coche.velocidad / 10

    # Si el auto sale de la ventana, volver a aparecer en el lado opuesto
    if vehiculo_rect.right < 0:
        vehiculo_rect.left = ANCHO
    elif vehiculo_rect.left > ANCHO:
        vehiculo_rect.right = 0

    # Dibujo en la pantalla
    pantalla.blit(fondo_imagen, (0, 0))  # Dibujar el fondo
    pantalla.blit(vehiculo_imagen, vehiculo_rect)  # Dibujar el vehículo

    # Dibujar recuadro para la velocidad
    pygame.draw.rect(pantalla, GRIS, (recuadro_velocidad_x, recuadro_velocidad_y, recuadro_velocidad_ancho, recuadro_velocidad_alto), 0)
    pygame.draw.rect(pantalla, NEGRO, (recuadro_velocidad_x, recuadro_velocidad_y, recuadro_velocidad_ancho, recuadro_velocidad_alto), 2)

    # Dibujar velocidad en el recuadro
    texto_velocidad = fuente.render(mi_coche.obtener_velocidad(), True, NEGRO)
    texto_velocidad_rect = texto_velocidad.get_rect(center=(ANCHO // 2, recuadro_velocidad_y + recuadro_velocidad_alto // 2))
    pantalla.blit(texto_velocidad, texto_velocidad_rect)

    # Dibujar recuadro para el mensaje
    if mi_coche.mostrar_mensaje:
        pygame.draw.rect(pantalla, GRIS, (recuadro_mensaje_x, recuadro_mensaje_y, recuadro_mensaje_ancho, recuadro_mensaje_alto), 0)
        pygame.draw.rect(pantalla, NEGRO, (recuadro_mensaje_x, recuadro_mensaje_y, recuadro_mensaje_ancho, recuadro_mensaje_alto), 2)

        # Dibujar mensaje en el recuadro
        texto_superficie = fuente.render(mi_coche.mensaje, True, NEGRO)
        texto_rect = texto_superficie.get_rect(center=(ANCHO // 2, ALTO // 2))
        pantalla.blit(texto_superficie, texto_rect)

        # Comprobar si ha pasado el tiempo para ocultar el mensaje
        if pygame.time.get_ticks() - mi_coche.tiempo_mensaje > 3000:
            mi_coche.mostrar_mensaje = False

    # Actualizar la pantalla
    pygame.display.flip()

    # Control de la velocidad de actualización
    reloj.tick(60)
