"""
Módulo para gestionar la física del juego SuperNick.
Incluye funciones para detectar colisiones y aplicar gravedad.
"""

import pygame

# Constantes físicas
GRAVEDAD = 0.5
VELOCIDAD_SALTO = -12
VELOCIDAD_MOVIMIENTO = 5
VELOCIDAD_MAXIMA_CAIDA = 10

def aplicar_gravedad(objeto, delta_tiempo=1.0):
    """
    Aplica gravedad a un objeto.
    
    Args:
        objeto: Objeto con propiedades velocidad_y
        delta_tiempo: Factor de tiempo para la física
    """
    objeto.velocidad_y += GRAVEDAD * delta_tiempo
    
    # Limitar la velocidad máxima de caída
    if objeto.velocidad_y > VELOCIDAD_MAXIMA_CAIDA:
        objeto.velocidad_y = VELOCIDAD_MAXIMA_CAIDA

def detectar_colision_plataforma(objeto, plataformas):
    """
    Detecta colisiones con plataformas y ajusta la posición del objeto.
    
    Args:
        objeto: Objeto que colisiona (debe tener rect, velocidad_y)
        plataformas: Grupo de sprites de plataformas
        
    Returns:
        bool: True si hay colisión con alguna plataforma
    """
    # Guardar posición Y anterior
    pos_y_anterior = objeto.rect.y
    
    # Detectar colisiones
    hits = pygame.sprite.spritecollide(objeto, plataformas, False)
    
    if hits:
        # Si estamos cayendo (velocidad positiva) y nuestra posición anterior
        # estaba por encima de la plataforma, nos posicionamos encima
        if objeto.velocidad_y > 0 and pos_y_anterior < hits[0].rect.top:
            objeto.rect.bottom = hits[0].rect.top
            objeto.velocidad_y = 0
            objeto.en_suelo = True
            return True
    
    return False

def detectar_colision_enemigo(objeto, enemigos, callback=None):
    """
    Detecta colisiones con enemigos.
    
    Args:
        objeto: Objeto que colisiona
        enemigos: Grupo de sprites de enemigos
        callback: Función a llamar cuando hay colisión
        
    Returns:
        bool: True si hay colisión con algún enemigo
    """
    hits = pygame.sprite.spritecollide(objeto, enemigos, False)
    
    if hits and callback:
        callback(hits[0])
        
    return len(hits) > 0

def detectar_colision_moneda(objeto, monedas, callback=None):
    """
    Detecta colisiones con monedas y las elimina.
    
    Args:
        objeto: Objeto que colisiona
        monedas: Grupo de sprites de monedas
        callback: Función a llamar cuando hay colisión
        
    Returns:
        int: Número de monedas recogidas
    """
    hits = pygame.sprite.spritecollide(objeto, monedas, True)
    
    if hits and callback:
        for moneda in hits:
            callback(moneda)
            
    return len(hits)

def limitar_movimiento(objeto, limites):
    """
    Limita el movimiento de un objeto dentro de unos límites.
    
    Args:
        objeto: Objeto con rect
        limites: Tupla (x_min, y_min, x_max, y_max)
    """
    x_min, y_min, x_max, y_max = limites
    
    if objeto.rect.left < x_min:
        objeto.rect.left = x_min
    if objeto.rect.right > x_max:
        objeto.rect.right = x_max
    if objeto.rect.top < y_min:
        objeto.rect.top = y_min
        objeto.velocidad_y = 0  # Evitar que siga subiendo
    if objeto.rect.bottom > y_max:
        objeto.rect.bottom = y_max
        objeto.velocidad_y = 0
        objeto.en_suelo = True 