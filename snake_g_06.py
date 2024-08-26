import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (213, 50, 80)
VERDE = (0, 255, 0)
AZUL = (50, 153, 213)
GRIS = (100, 100, 100)

# Dimensiones de la ventana del juego
ANCHO_VENTANA = 600
ALTO_VENTANA = 400

# Crear la ventana del juego
ventana_juego = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption('Snake Game')

# Controlar el tiempo
reloj = pygame.time.Clock()

# Tamaño de los bloques (segmentos) del Snake
TAMANO_BLOQUE = 10

# Definir las fuentes para mostrar la puntuación y los mensajes
fuente_puntuacion = pygame.font.SysFont("bahnschrift", 10)  # Tamaño 10 para la puntuación
fuente = pygame.font.SysFont("bahnschrift", 25)
fuente_grande = pygame.font.SysFont("comicsansms", 35)

def mostrar_puntuacion(puntuacion):
    valor = fuente_puntuacion.render("Puntuación: " + str(puntuacion), True, BLANCO)
    rect = valor.get_rect()
    rect.topleft = (10, 10)
    pygame.draw.rect(ventana_juego, GRIS, rect.inflate(10, 10))  # Añadir un rectángulo alrededor del texto
    ventana_juego.blit(valor, rect)

def nuestro_snake(lista_snake):
    for x in lista_snake:
        pygame.draw.rect(ventana_juego, VERDE, [x[0], x[1], TAMANO_BLOQUE, TAMANO_BLOQUE])

def mensaje_centrado(texto, color, desplazamiento_y=0, fuente_tipo='pequeña'):
    if fuente_tipo == 'grande':
        texto_superficie = fuente_grande.render(texto, True, color)
    else:
        texto_superficie = fuente.render(texto, True, color)
    texto_rect = texto_superficie.get_rect(center=(ANCHO_VENTANA/2, ALTO_VENTANA/2 + desplazamiento_y))
    ventana_juego.blit(texto_superficie, texto_rect)

def mapear_velocidad(seleccion_usuario):
    """
    Mapea la selección de velocidad del usuario (1-10) a FPS (5-30).
    """
    return 5 + (seleccion_usuario - 1) * 2.5  # Velocidad entre 5 y 30 FPS

def pantalla_inicio():
    seleccion_velocidad = 5  # Valor inicial por defecto
    en_pantalla_inicio = True

    while en_pantalla_inicio:
        ventana_juego.fill(NEGRO)
        mensaje_centrado("Bienvenido al Snake Game!", BLANCO, -100, 'grande')
        mensaje_centrado("Usa las flechas ARRIBA y ABAJO para seleccionar la velocidad", GRIS, -50)
        mensaje_centrado("Presiona ENTER para empezar", GRIS, 0)

        # Mostrar la velocidad seleccionada dentro de un recuadro
        rect_width = 100
        rect_height = 50
        rect_x = (ANCHO_VENTANA - rect_width) / 2
        rect_y = (ALTO_VENTANA / 2) + 50

        pygame.draw.rect(ventana_juego, GRIS, [rect_x, rect_y, rect_width, rect_height])
        velocidad_texto = fuente.render(str(seleccion_velocidad), True, BLANCO)
        velocidad_rect = velocidad_texto.get_rect(center=(ANCHO_VENTANA/2, rect_y + rect_height/2))
        ventana_juego.blit(velocidad_texto, velocidad_rect)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if seleccion_velocidad < 10:
                        seleccion_velocidad += 1
                elif evento.key == pygame.K_DOWN:
                    if seleccion_velocidad > 1:
                        seleccion_velocidad -= 1
                elif evento.key == pygame.K_RETURN:
                    en_pantalla_inicio = False

    return seleccion_velocidad

def animacion_comer(posicion_comida):
    # Efecto de partículas cuando el Snake come la comida
    for _ in range(20):  # Generar 20 partículas
        x_particula = posicion_comida[0] + random.randint(-10, 10)
        y_particula = posicion_comida[1] + random.randint(-10, 10)
        pygame.draw.circle(ventana_juego, AZUL, (x_particula, y_particula), 3)
    pygame.display.update()
    pygame.time.delay(100)  # Pequeño retraso para mostrar la animación

def animacion_colision():
    # Efecto de destello de la pantalla cuando hay una colisión
    ventana_juego.fill(ROJO)
    pygame.display.update()
    pygame.time.delay(150)  # Retardo breve para el destello
    ventana_juego.fill(NEGRO)

def juego(velocidad_snake):
    juego_terminado = False
    juego_cerrado = False

    # Posición inicial del Snake
    x_snake = ANCHO_VENTANA / 2
    y_snake = ALTO_VENTANA / 2

    x_cambio = 0
    y_cambio = 0

    lista_snake = []
    longitud_snake = 1

    # Posición inicial de la comida
    x_comida = round(random.randrange(0, ANCHO_VENTANA - TAMANO_BLOQUE) / 10.0) * 10.0
    y_comida = round(random.randrange(0, ALTO_VENTANA - TAMANO_BLOQUE) / 10.0) * 10.0

    comida_especial = False

    while not juego_terminado:

        while juego_cerrado:
            ventana_juego.fill(NEGRO)
            mensaje_centrado("Perdiste! Presiona C para jugar de nuevo o Q para salir", ROJO, -50)
            mensaje_centrado(f"Puntuación: {longitud_snake - 1}", BLANCO, 50)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        pygame.quit()
                        return
                    if evento.key == pygame.K_c:
                        juego(velocidad_snake)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_terminado = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and x_cambio != TAMANO_BLOQUE:
                    x_cambio = -TAMANO_BLOQUE
                    y_cambio = 0
                elif evento.key == pygame.K_RIGHT and x_cambio != -TAMANO_BLOQUE:
                    x_cambio = TAMANO_BLOQUE
                    y_cambio = 0
                elif evento.key == pygame.K_UP and y_cambio != TAMANO_BLOQUE:
                    y_cambio = -TAMANO_BLOQUE
                    x_cambio = 0
                elif evento.key == pygame.K_DOWN and y_cambio != -TAMANO_BLOQUE:
                    y_cambio = TAMANO_BLOQUE
                    x_cambio = 0

        if x_snake >= ANCHO_VENTANA or x_snake < 0 or y_snake >= ALTO_VENTANA or y_snake < 0:
            animacion_colision()
            juego_cerrado = True

        x_snake += x_cambio
        y_snake += y_cambio

        ventana_juego.fill(NEGRO)

        # Determinar el color de la comida (rojo para especial, azul para normal)
        if comida_especial:
            pygame.draw.rect(ventana_juego, ROJO, [x_comida, y_comida, TAMANO_BLOQUE, TAMANO_BLOQUE])
        else:
            pygame.draw.rect(ventana_juego, AZUL, [x_comida, y_comida, TAMANO_BLOQUE, TAMANO_BLOQUE])

        cabeza_snake = []
        cabeza_snake.append(x_snake)
        cabeza_snake.append(y_snake)
        lista_snake.append(cabeza_snake)

        if len(lista_snake) > longitud_snake:
            del lista_snake[0]

        # Comprobar colisión con el propio cuerpo
        for segmento in lista_snake[:-1]:
            if segmento == cabeza_snake:
                animacion_colision()
                juego_cerrado = True

        nuestro_snake(lista_snake)
        mostrar_puntuacion(longitud_snake - 1)

        pygame.display.update()

        # Comprobar si el Snake come la comida
        if x_snake == x_comida and y_snake == y_comida:
            x_comida = round(random.randrange(0, ANCHO_VENTANA - TAMANO_BLOQUE) / 10.0) * 10.0
            y_comida = round(random.randrange(0, ALTO_VENTANA - TAMANO_BLOQUE) / 10.0) * 10.0
            if comida_especial:
                longitud_snake += 5  # Sumar 5 puntos por comida especial
            else:
                longitud_snake += 1  # Sumar 1 punto por comida normal

            comida_especial = False

            if (longitud_snake - 1) % 10 == 0:  # Si la puntuación es múltiplo de 10, la próxima comida será especial
                comida_especial = True

            animacion_comer((x_comida, y_comida))

        reloj.tick(velocidad_snake)

    pygame.quit()

def main():
    seleccion_usuario = pantalla_inicio()
    velocidad_snake = mapear_velocidad(seleccion_usuario)
    juego(velocidad_snake)

if __name__ == "__main__":
    main()
