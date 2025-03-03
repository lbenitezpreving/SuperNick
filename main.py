import pygame
import sys
import os
from pygame.locals import *
import recursos
import fisica
import sonido

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Constantes
ANCHO = 800
ALTO = 600
FPS = 60
TITULO = "SuperNick"

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_CIELO = (107, 140, 255)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)
reloj = pygame.time.Clock()

# Inicializar recursos
recursos.inicializar_recursos()
sonido.inicializar()

# Estados del juego
MENU = 0
JUGANDO = 1
GAME_OVER = 2
VICTORIA = 3
SELECCION_NIVEL = 4

# Clase para el personaje principal
class Nick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Usar imagen de recursos
        self.image = recursos.imagenes["nick.png"]
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 4, ALTO // 2)
        
        # Propiedades físicas
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.en_suelo = False
        self.vidas = 3
        self.direccion = 1  # 1 derecha, -1 izquierda
        self.puntuacion = 0
        
    def update(self):
        # Aplicar gravedad
        fisica.aplicar_gravedad(self)
        
        # Movimiento horizontal
        self.rect.x += self.velocidad_x
        
        # Limitar movimiento dentro de la pantalla
        fisica.limitar_movimiento(self, (0, 0, ANCHO, ALTO - 50))
            
        # Movimiento vertical
        self.rect.y += self.velocidad_y
            
    def saltar(self):
        if self.en_suelo:
            self.velocidad_y = fisica.VELOCIDAD_SALTO
            self.en_suelo = False
            sonido.reproducir_efecto("salto")
            
    def mover_izquierda(self):
        self.velocidad_x = -fisica.VELOCIDAD_MOVIMIENTO
        self.direccion = -1
        
    def mover_derecha(self):
        self.velocidad_x = fisica.VELOCIDAD_MOVIMIENTO
        self.direccion = 1
        
    def detener(self):
        self.velocidad_x = 0
        
    def perder_vida(self):
        self.vidas -= 1
        sonido.reproducir_efecto("dano")
        return self.vidas <= 0
        
    def reposicionar(self):
        self.rect.center = (ANCHO // 4, ALTO // 2)
        self.velocidad_x = 0
        self.velocidad_y = 0
        
    def recoger_moneda(self, moneda):
        self.puntuacion += moneda.valor
        sonido.reproducir_efecto("moneda")

# Clase para plataformas
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        # Usar imagen de recursos
        self.image = recursos.imagenes["plataforma.png"]
        # Escalar la imagen al tamaño deseado
        self.image = pygame.transform.scale(self.image, (ancho, alto))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Clase para enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Usar imagen de recursos
        self.image = recursos.imagenes["enemigo.png"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 2
        self.direccion = 1
        
    def update(self):
        self.rect.x += self.velocidad * self.direccion
        
        # Cambiar dirección al llegar a ciertos límites
        if self.rect.right > ANCHO - 100 or self.rect.left < 100:
            self.direccion *= -1

# Clase para monedas
class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Usar imagen de recursos
        self.image = recursos.imagenes["moneda.png"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.valor = 10

# Clase para gestionar niveles
class Nivel:
    def __init__(self, numero):
        self.numero = numero
        self.plataformas = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.monedas = pygame.sprite.Group()
        self.tiempo_limite = 120  # 2 minutos por defecto
        self.tiempo_restante = self.tiempo_limite
        self.ultimo_tiempo = pygame.time.get_ticks()
        self.monedas_totales = 0
        
        # Configurar nivel según el número
        self.configurar_nivel()
        
    def configurar_nivel(self):
        # Suelo base para todos los niveles
        self.plataformas.add(Plataforma(0, ALTO - 50, ANCHO, 50))
        
        if self.numero == 1:
            # Nivel 1: Fácil, pocas plataformas y enemigos
            self.plataformas.add(Plataforma(200, 400, 100, 20))
            self.plataformas.add(Plataforma(400, 350, 100, 20))
            self.plataformas.add(Plataforma(600, 300, 100, 20))
            
            self.enemigos.add(Enemigo(300, ALTO - 80))
            self.enemigos.add(Enemigo(500, ALTO - 80))
            
            for i in range(5):
                self.monedas.add(Moneda(150 + i * 100, 350))
                
            self.tiempo_limite = 60  # 1 minuto
            
        elif self.numero == 2:
            # Nivel 2: Dificultad media
            self.plataformas.add(Plataforma(100, 450, 100, 20))
            self.plataformas.add(Plataforma(300, 400, 100, 20))
            self.plataformas.add(Plataforma(500, 350, 100, 20))
            self.plataformas.add(Plataforma(300, 250, 100, 20))
            self.plataformas.add(Plataforma(100, 200, 100, 20))
            
            self.enemigos.add(Enemigo(200, ALTO - 80))
            self.enemigos.add(Enemigo(400, ALTO - 80))
            self.enemigos.add(Enemigo(600, ALTO - 80))
            
            for i in range(8):
                self.monedas.add(Moneda(100 + i * 80, 300))
                
            self.tiempo_limite = 90  # 1.5 minutos
            
        elif self.numero == 3:
            # Nivel 3: Difícil
            self.plataformas.add(Plataforma(100, 500, 100, 20))
            self.plataformas.add(Plataforma(300, 450, 100, 20))
            self.plataformas.add(Plataforma(500, 400, 100, 20))
            self.plataformas.add(Plataforma(300, 350, 100, 20))
            self.plataformas.add(Plataforma(100, 300, 100, 20))
            self.plataformas.add(Plataforma(300, 250, 100, 20))
            self.plataformas.add(Plataforma(500, 200, 100, 20))
            
            self.enemigos.add(Enemigo(150, ALTO - 80))
            self.enemigos.add(Enemigo(350, ALTO - 80))
            self.enemigos.add(Enemigo(550, ALTO - 80))
            self.enemigos.add(Enemigo(250, 420))
            self.enemigos.add(Enemigo(450, 320))
            
            for i in range(10):
                self.monedas.add(Moneda(80 + i * 70, 250))
                
            self.tiempo_limite = 120  # 2 minutos
        
        self.tiempo_restante = self.tiempo_limite
        self.monedas_totales = len(self.monedas)
        
    def actualizar_tiempo(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_tiempo >= 1000:  # 1 segundo
            self.tiempo_restante -= 1
            self.ultimo_tiempo = tiempo_actual
            
    def dibujar(self, pantalla):
        # Dibujar fondo
        pantalla.fill(AZUL_CIELO)
        
        # Dibujar elementos del nivel
        self.plataformas.draw(pantalla)
        self.enemigos.draw(pantalla)
        self.monedas.draw(pantalla)
        
        # Dibujar información del nivel
        fuente = pygame.font.Font(None, 36)
        texto_nivel = fuente.render(f"Nivel: {self.numero}", True, NEGRO)
        texto_tiempo = fuente.render(f"Tiempo: {self.tiempo_restante}", True, NEGRO)
        
        pantalla.blit(texto_nivel, (10, 10))
        pantalla.blit(texto_tiempo, (ANCHO - 150, 10))
        
    def manejar_colisiones(self, jugador):
        # Colisiones con plataformas
        fisica.detectar_colision_plataforma(jugador, self.plataformas)
        
        # Colisiones con enemigos
        if fisica.detectar_colision_enemigo(jugador, self.enemigos):
            if jugador.perder_vida():
                sonido.reproducir_efecto("game_over")
                return GAME_OVER
            else:
                jugador.reposicionar()
                
        # Colisiones con monedas
        fisica.detectar_colision_moneda(jugador, self.monedas, jugador.recoger_moneda)
        
        # Verificar victoria (todas las monedas recogidas)
        if len(self.monedas) == 0:
            sonido.reproducir_efecto("victoria")
            return VICTORIA
            
        return None

# Clase para el menú principal
class Menu:
    def __init__(self):
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_opciones = pygame.font.Font(None, 48)
        self.opcion_seleccionada = 0
        self.opciones = ["Jugar", "Seleccionar Nivel", "Salir"]
        
    def dibujar(self, pantalla):
        pantalla.fill(AZUL_CIELO)
        
        # Título
        texto_titulo = self.fuente_titulo.render("SuperNick", True, NEGRO)
        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 100))
        
        # Opciones
        for i, opcion in enumerate(self.opciones):
            if i == self.opcion_seleccionada:
                color = (255, 0, 0)  # Rojo para la opción seleccionada
            else:
                color = NEGRO
                
            texto_opcion = self.fuente_opciones.render(opcion, True, color)
            pantalla.blit(texto_opcion, (ANCHO // 2 - texto_opcion.get_width() // 2, 250 + i * 60))
            
    def manejar_eventos(self, evento):
        if evento.type == KEYDOWN:
            if evento.key == K_UP:
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                sonido.reproducir_efecto("moneda")  # Usar sonido de moneda como efecto de navegación
            elif evento.key == K_DOWN:
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                sonido.reproducir_efecto("moneda")
            elif evento.key == K_RETURN:
                sonido.reproducir_efecto("salto")  # Usar sonido de salto como efecto de selección
                return self.opcion_seleccionada
        return None

# Clase para la pantalla de selección de nivel
class SeleccionNivel:
    def __init__(self):
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_opciones = pygame.font.Font(None, 48)
        self.nivel_seleccionado = 0
        self.niveles = ["Nivel 1", "Nivel 2", "Nivel 3", "Volver"]
        
    def dibujar(self, pantalla):
        pantalla.fill(AZUL_CIELO)
        
        # Título
        texto_titulo = self.fuente_titulo.render("Seleccionar Nivel", True, NEGRO)
        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 100))
        
        # Opciones de niveles
        for i, nivel in enumerate(self.niveles):
            if i == self.nivel_seleccionado:
                color = (255, 0, 0)  # Rojo para la opción seleccionada
            else:
                color = NEGRO
                
            texto_nivel = self.fuente_opciones.render(nivel, True, color)
            pantalla.blit(texto_nivel, (ANCHO // 2 - texto_nivel.get_width() // 2, 250 + i * 60))
            
    def manejar_eventos(self, evento):
        if evento.type == KEYDOWN:
            if evento.key == K_UP:
                self.nivel_seleccionado = (self.nivel_seleccionado - 1) % len(self.niveles)
                sonido.reproducir_efecto("moneda")
            elif evento.key == K_DOWN:
                self.nivel_seleccionado = (self.nivel_seleccionado + 1) % len(self.niveles)
                sonido.reproducir_efecto("moneda")
            elif evento.key == K_RETURN:
                sonido.reproducir_efecto("salto")
                return self.nivel_seleccionado
        return None

# Clase para la pantalla de Game Over
class GameOver:
    def __init__(self):
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_opciones = pygame.font.Font(None, 48)
        self.opcion_seleccionada = 0
        self.opciones = ["Reintentar", "Menú Principal"]
        
    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)
        
        # Título
        texto_titulo = self.fuente_titulo.render("Game Over", True, (255, 0, 0))
        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 200))
        
        # Opciones
        for i, opcion in enumerate(self.opciones):
            if i == self.opcion_seleccionada:
                color = (255, 0, 0)
            else:
                color = BLANCO
                
            texto_opcion = self.fuente_opciones.render(opcion, True, color)
            pantalla.blit(texto_opcion, (ANCHO // 2 - texto_opcion.get_width() // 2, 300 + i * 60))
            
    def manejar_eventos(self, evento):
        if evento.type == KEYDOWN:
            if evento.key == K_UP:
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                sonido.reproducir_efecto("moneda")
            elif evento.key == K_DOWN:
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                sonido.reproducir_efecto("moneda")
            elif evento.key == K_RETURN:
                sonido.reproducir_efecto("salto")
                return self.opcion_seleccionada
        return None

# Clase para la pantalla de Victoria
class Victoria:
    def __init__(self):
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_opciones = pygame.font.Font(None, 48)
        self.opcion_seleccionada = 0
        self.opciones = ["Siguiente Nivel", "Menú Principal"]
        
    def dibujar(self, pantalla):
        pantalla.fill(AZUL_CIELO)
        
        # Título
        texto_titulo = self.fuente_titulo.render("¡Nivel Completado!", True, NEGRO)
        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 200))
        
        # Opciones
        for i, opcion in enumerate(self.opciones):
            if i == self.opcion_seleccionada:
                color = (255, 0, 0)
            else:
                color = NEGRO
                
            texto_opcion = self.fuente_opciones.render(opcion, True, color)
            pantalla.blit(texto_opcion, (ANCHO // 2 - texto_opcion.get_width() // 2, 300 + i * 60))
            
    def manejar_eventos(self, evento):
        if evento.type == KEYDOWN:
            if evento.key == K_UP:
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                sonido.reproducir_efecto("moneda")
            elif evento.key == K_DOWN:
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                sonido.reproducir_efecto("moneda")
            elif evento.key == K_RETURN:
                sonido.reproducir_efecto("salto")
                return self.opcion_seleccionada
        return None

# Función principal del juego
def main():
    # Inicializar objetos del juego
    nick = Nick()
    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(nick)
    
    # Inicializar menús
    menu_principal = Menu()
    seleccion_nivel = SeleccionNivel()
    game_over = GameOver()
    victoria = Victoria()
    
    # Estado inicial
    estado_actual = MENU
    nivel_actual = None
    nivel_numero = 1
    
    # Bucle principal del juego
    ejecutando = True
    while ejecutando:
        # Control de FPS
        reloj.tick(FPS)
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == QUIT:
                ejecutando = False
                
            # Manejo de eventos según el estado del juego
            if estado_actual == MENU:
                opcion = menu_principal.manejar_eventos(evento)
                if opcion == 0:  # Jugar
                    estado_actual = JUGANDO
                    nivel_actual = Nivel(nivel_numero)
                elif opcion == 1:  # Seleccionar Nivel
                    estado_actual = SELECCION_NIVEL
                elif opcion == 2:  # Salir
                    ejecutando = False
                    
            elif estado_actual == SELECCION_NIVEL:
                opcion = seleccion_nivel.manejar_eventos(evento)
                if opcion in [0, 1, 2]:  # Niveles 1, 2, 3
                    estado_actual = JUGANDO
                    nivel_numero = opcion + 1
                    nivel_actual = Nivel(nivel_numero)
                elif opcion == 3:  # Volver
                    estado_actual = MENU
                    
            elif estado_actual == GAME_OVER:
                opcion = game_over.manejar_eventos(evento)
                if opcion == 0:  # Reintentar
                    estado_actual = JUGANDO
                    nivel_actual = Nivel(nivel_numero)
                    nick = Nick()
                    todos_los_sprites = pygame.sprite.Group()
                    todos_los_sprites.add(nick)
                elif opcion == 1:  # Menú Principal
                    estado_actual = MENU
                    
            elif estado_actual == VICTORIA:
                opcion = victoria.manejar_eventos(evento)
                if opcion == 0:  # Siguiente Nivel
                    nivel_numero = min(nivel_numero + 1, 3)
                    nivel_actual = Nivel(nivel_numero)
                    estado_actual = JUGANDO
                elif opcion == 1:  # Menú Principal
                    estado_actual = MENU
                    
            elif estado_actual == JUGANDO:
                if evento.type == KEYDOWN:
                    if evento.key == K_SPACE:
                        nick.saltar()
        
        # Actualización del juego según el estado
        if estado_actual == JUGANDO:
            # Controles de movimiento
            teclas = pygame.key.get_pressed()
            if teclas[K_LEFT]:
                nick.mover_izquierda()
            elif teclas[K_RIGHT]:
                nick.mover_derecha()
            else:
                nick.detener()
                
            # Actualizar sprites
            todos_los_sprites.update()
            nivel_actual.enemigos.update()
            
            # Actualizar tiempo
            nivel_actual.actualizar_tiempo()
            if nivel_actual.tiempo_restante <= 0:
                sonido.reproducir_efecto("game_over")
                estado_actual = GAME_OVER
                
            # Manejar colisiones y verificar cambios de estado
            nuevo_estado = nivel_actual.manejar_colisiones(nick)
            if nuevo_estado:
                estado_actual = nuevo_estado
        
        # Dibujar según el estado del juego
        if estado_actual == MENU:
            menu_principal.dibujar(pantalla)
        elif estado_actual == SELECCION_NIVEL:
            seleccion_nivel.dibujar(pantalla)
        elif estado_actual == JUGANDO:
            nivel_actual.dibujar(pantalla)
            todos_los_sprites.draw(pantalla)
            
            # Dibujar vidas y puntuación
            fuente = pygame.font.Font(None, 36)
            texto_vidas = fuente.render(f"Vidas: {nick.vidas}", True, NEGRO)
            texto_puntuacion = fuente.render(f"Puntos: {nick.puntuacion}", True, NEGRO)
            
            pantalla.blit(texto_vidas, (ANCHO - 150, 50))
            pantalla.blit(texto_puntuacion, (10, 50))
            
        elif estado_actual == GAME_OVER:
            game_over.dibujar(pantalla)
        elif estado_actual == VICTORIA:
            victoria.dibujar(pantalla)
            
        # Actualizar pantalla
        pygame.display.flip()
        
    # Salir del juego
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 