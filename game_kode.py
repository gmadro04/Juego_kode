import pygame
import sys
import random

# Inicializar PyGame
pygame.init()

# Configuración de la pantalla
ancho_screen = 800
alto_screen = 600
display = pygame.display.set_mode((ancho_screen, alto_screen))
pygame.display.set_caption("Space Shooter by gmadro")

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)
verde = (0, 255, 0)

# Configuraciones del jugador
jugador_velocidad = 3
jugador_width = 50
jugador_height = 40
jugador = pygame.Rect(ancho_screen // 2 - jugador_width // 2, alto_screen - jugador_height - 10, jugador_width, jugador_height)
vidas = 3  # Inicializamos con 3 vidas

# Configuración de los enemigos
enemigo_width = 40
enemigo_height = 30
enemigos = []
balas_enemigas = []
velocidad_enemigos = 2  # Ajustada a una velocidad más baja
enemigos_vivos = 3  # 3 enemigos por nivel


# Variables de disparo del jugador
bala_jugador_width = 5
bala_jugador_height = 10
balas_jugador = []
bala_velocidad = -6
tiempo_disparo = 0  # Temporizador para controlar la frecuencia de disparo
cooldown_disparo = 500  # Tiempo en milisegundos entre disparos (0.5 segundos)

# Variables del juego
nivel = 1
juego_activo = True
reloj = pygame.time.Clock()

# Función para generar enemigos
def generar_enemigos(n):
    enemigos = []
    for i in range(n):
        enemigo = pygame.Rect(random.randint(0, ancho_screen - enemigo_width), random.randint(-300, -enemigo_height), enemigo_width, enemigo_height)
        enemigos.append(enemigo)
    return enemigos

# Función para disparar balas del enemigo
def disparar_bala_enemigo(enemigo):
    if random.randint(0, 100) < 5:  # Probabilidad de disparo enemigo
        bala = pygame.Rect(enemigo.x + enemigo_width // 2, enemigo.y + enemigo_height, 5, 10)
        balas_enemigas.append(bala)

# Función para mover las balas
def mover_balas(balas, velocidad):
    for bala in balas[:]:
        bala.y += velocidad
        if bala.y > alto_screen or bala.y < 0:  # Eliminar balas que salen de la pantalla
            balas.remove(bala)

# Función para mover los enemigos
def mover_enemigos(enemigos, velocidad):
    for enemigo in enemigos:
        enemigo.y += velocidad
        if enemigo.y > alto_screen:  # Si el enemigo pasa la pantalla, lo reubicamos arriba
            enemigo.y = random.randint(-300, -enemigo_height)
            enemigo.x = random.randint(0, ancho_screen - enemigo_width)

# Función para dibujar el jugador, enemigos y balas
def dibujar_escenario(jugador, enemigos, balas_jugador, balas_enemigas):
    display.fill(negro)  # Limpiar pantalla

    # Dibuja al jugador
    pygame.draw.rect(display, blanco, jugador)

    # Dibuja los enemigos
    for enemigo in enemigos:
        pygame.draw.rect(display, rojo, enemigo)

    # Dibuja las balas del jugador
    for bala in balas_jugador:
        pygame.draw.rect(display, verde, bala)

    # Dibuja las balas enemigas
    for bala in balas_enemigas:
        pygame.draw.rect(display, rojo, bala)

    # Mostrar las vidas restantes
    fuente = pygame.font.Font(None, 36)
    vidas_texto = fuente.render(f"Vidas: {vidas}", True, blanco)
    display.blit(vidas_texto, (10, 10))

    # Mostrar las vidas restantes
    fuente = pygame.font.Font(None, 36)
    nivel_texto = fuente.render(f"Nivel: {nivel}", True, blanco)
    display.blit(nivel_texto, (10, 50))

    pygame.display.flip()  # Actualizar la pantalla

# Función principal del juego
def iniciar_juego():
    global juego_activo, enemigos, nivel, velocidad_enemigos, enemigos_vivos, vidas, tiempo_disparo

    enemigos = generar_enemigos(3)

    while juego_activo:
        manejar_eventos()

        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.x > 0:
            jugador.x -= jugador_velocidad
        if teclas[pygame.K_RIGHT] and jugador.x < ancho_screen - jugador_width:
            jugador.x += jugador_velocidad

        # Controlar el tiempo de disparo del jugador
        if teclas[pygame.K_SPACE] and pygame.time.get_ticks() - tiempo_disparo > cooldown_disparo:
            disparar_jugador()
            tiempo_disparo = pygame.time.get_ticks()  # Actualizar el tiempo del último disparo

        # Movimiento de las balas
        mover_balas(balas_jugador, bala_velocidad)
        mover_balas(balas_enemigas, 4)

        # Movimiento de enemigos y disparos enemigos
        mover_enemigos(enemigos, velocidad_enemigos)
        for enemigo in enemigos:
            disparar_bala_enemigo(enemigo)  # Los enemigos siguen disparando

        # Detectar colisiones
        detectar_colisiones()

        # Dibujar todo
        dibujar_escenario(jugador, enemigos, balas_jugador, balas_enemigas)

        # Si matas a los 3 enemigos, subes de nivel
        if enemigos_vivos == 0:
            nivel += 1
            enemigos_vivos = 3
            velocidad_enemigos += 0.5 # Aumentar la velocidad en niveles
            enemigos = generar_enemigos(3)  # Generar nuevos enemigos
            balas_enemigas.clear()  # Limpiar las balas enemigas anteriores

        reloj.tick(60)  # Mantener el juego a 60 FPS

# Función para gestionar los eventos del juego
def manejar_eventos():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Función para disparar las balas del jugador
def disparar_jugador():
    if len(balas_jugador) < 3:  # Limitar el número de balas en pantalla
        bala = pygame.Rect(jugador.x + jugador_width // 2 - bala_jugador_width // 2, jugador.y, bala_jugador_width, bala_jugador_height)
        balas_jugador.append(bala)

# Función para detectar colisiones
def detectar_colisiones():
    global enemigos_vivos, vidas
    # Detectar colisiones entre las balas del jugador y los enemigos
    for bala in balas_jugador[:]:
        for enemigo in enemigos[:]:
            if bala.colliderect(enemigo):
                enemigos.remove(enemigo)
                enemigos_vivos -= 1
                balas_jugador.remove(bala)
                break

    # Detectar colisiones entre las balas enemigas y el jugador
    for bala in balas_enemigas[:]:
        if bala.colliderect(jugador):
            balas_enemigas.remove(bala)
            vidas -= 1  # Restar una vida
            if vidas == 0:
                game_over()

# Función para terminar el juego
def game_over():
    global juego_activo
    juego_activo = False
    display.fill(negro)
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render("Game Over :c", True, rojo)
    display.blit(texto, (ancho_screen // 3, alto_screen // 3))
    pygame.display.flip()
    pygame.time.wait(3000)  # Esperar 3 segundos antes de salir
    pygame.quit()
    sys.exit()

# Función para el menú principal
def menu_inicial():
    display.fill(negro)
    fuente = pygame.font.Font(None, 70)
    titulo = fuente.render("Space shoter :D", True, blanco)
    display.blit(titulo, (ancho_screen // 3, alto_screen // 3))
    pygame.display.flip()
    # Mensaje de instrucciones
    fuente1 = pygame.font.Font(None, 34)
    instrucciones = fuente1.render("Presiona Enter para comenzar", True, blanco)
    display.blit(instrucciones, (ancho_screen // 4, alto_screen // 3 + 80))
    instrucciones2 = fuente1.render("Usa las flechas para moverte", True, blanco)
    display.blit(instrucciones2, (ancho_screen // 4, alto_screen // 3 + 120))
    instrucciones3 = fuente1.render("Espacio para disparar", True, blanco)
    display.blit(instrucciones3, (ancho_screen // 4, alto_screen // 3 + 160))
    pygame.display.flip()
    bucle = True
    while bucle:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Iniciar el juego al presionar Enter
                    bucle = False
# Iniciar el menú principal
menu_inicial()
iniciar_juego()

# Cerrar PyGame al terminar
pygame.quit()
