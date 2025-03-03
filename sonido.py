"""
Módulo para gestionar el sonido del juego SuperNick.
"""

import pygame
import os
import recursos

# Constantes
VOLUMEN_MUSICA = 0.5
VOLUMEN_EFECTOS = 0.7

# Diccionario para almacenar efectos de sonido
efectos = {}

def inicializar():
    """Inicializa el sistema de sonido."""
    pygame.mixer.init()
    cargar_efectos_temporales()

def cargar_efectos_temporales():
    """Crea efectos de sonido temporales para desarrollo."""
    # En una implementación real, estos serían archivos de sonido
    # Por ahora, creamos sonidos sintéticos para pruebas
    
    # Sonido de salto (tono agudo)
    salto = pygame.mixer.Sound(buffer=crear_sonido_sintetico(440, 0.3))
    salto.set_volume(VOLUMEN_EFECTOS)
    efectos["salto"] = salto
    
    # Sonido de moneda (tono más agudo y corto)
    moneda = pygame.mixer.Sound(buffer=crear_sonido_sintetico(880, 0.1))
    moneda.set_volume(VOLUMEN_EFECTOS)
    efectos["moneda"] = moneda
    
    # Sonido de daño (tono grave)
    dano = pygame.mixer.Sound(buffer=crear_sonido_sintetico(220, 0.5))
    dano.set_volume(VOLUMEN_EFECTOS)
    efectos["dano"] = dano
    
    # Sonido de victoria (secuencia ascendente)
    victoria = pygame.mixer.Sound(buffer=crear_sonido_victoria())
    victoria.set_volume(VOLUMEN_EFECTOS)
    efectos["victoria"] = victoria
    
    # Sonido de game over (secuencia descendente)
    game_over = pygame.mixer.Sound(buffer=crear_sonido_game_over())
    game_over.set_volume(VOLUMEN_EFECTOS)
    efectos["game_over"] = game_over

def crear_sonido_sintetico(frecuencia, duracion):
    """
    Crea un sonido sintético con una frecuencia y duración específicas.
    
    Args:
        frecuencia: Frecuencia del sonido en Hz
        duracion: Duración del sonido en segundos
        
    Returns:
        bytearray: Buffer de audio
    """
    import math
    import array
    
    # Parámetros de audio
    bits = 16
    sample_rate = 44100
    
    # Calcular número de muestras
    n_samples = int(round(duracion * sample_rate))
    
    # Crear buffer
    buf = array.array('h', [0] * n_samples)
    
    # Generar onda sinusoidal
    for i in range(n_samples):
        t = float(i) / sample_rate
        buf[i] = int(32767.0 * math.sin(2.0 * math.pi * frecuencia * t))
    
    return buf

def crear_sonido_victoria():
    """Crea un sonido de victoria (secuencia ascendente)."""
    import math
    import array
    
    # Parámetros de audio
    bits = 16
    sample_rate = 44100
    duracion = 1.0
    
    # Calcular número de muestras
    n_samples = int(round(duracion * sample_rate))
    
    # Crear buffer
    buf = array.array('h', [0] * n_samples)
    
    # Generar secuencia ascendente
    for i in range(n_samples):
        t = float(i) / sample_rate
        # Frecuencia que aumenta con el tiempo
        freq = 440 + 440 * t
        buf[i] = int(32767.0 * math.sin(2.0 * math.pi * freq * t))
    
    return buf

def crear_sonido_game_over():
    """Crea un sonido de game over (secuencia descendente)."""
    import math
    import array
    
    # Parámetros de audio
    bits = 16
    sample_rate = 44100
    duracion = 1.0
    
    # Calcular número de muestras
    n_samples = int(round(duracion * sample_rate))
    
    # Crear buffer
    buf = array.array('h', [0] * n_samples)
    
    # Generar secuencia descendente
    for i in range(n_samples):
        t = float(i) / sample_rate
        # Frecuencia que disminuye con el tiempo
        freq = 880 - 660 * t
        buf[i] = int(32767.0 * math.sin(2.0 * math.pi * freq * t))
    
    return buf

def reproducir_efecto(nombre):
    """
    Reproduce un efecto de sonido.
    
    Args:
        nombre: Nombre del efecto a reproducir
    """
    if nombre in efectos:
        efectos[nombre].play()

def reproducir_musica(nombre, repetir=-1):
    """
    Reproduce música de fondo.
    
    Args:
        nombre: Nombre del archivo de música
        repetir: Número de repeticiones (-1 para infinito)
    """
    try:
        ruta_completa = os.path.join(recursos.DIR_SONIDOS, nombre)
        pygame.mixer.music.load(ruta_completa)
        pygame.mixer.music.set_volume(VOLUMEN_MUSICA)
        pygame.mixer.music.play(repetir)
    except pygame.error:
        print(f"No se pudo cargar la música: {nombre}")

def detener_musica():
    """Detiene la música de fondo."""
    pygame.mixer.music.stop()

def pausar_musica():
    """Pausa la música de fondo."""
    pygame.mixer.music.pause()

def reanudar_musica():
    """Reanuda la música de fondo."""
    pygame.mixer.music.unpause()

def ajustar_volumen_musica(volumen):
    """
    Ajusta el volumen de la música.
    
    Args:
        volumen: Valor entre 0.0 y 1.0
    """
    global VOLUMEN_MUSICA
    VOLUMEN_MUSICA = max(0.0, min(1.0, volumen))
    pygame.mixer.music.set_volume(VOLUMEN_MUSICA)

def ajustar_volumen_efectos(volumen):
    """
    Ajusta el volumen de los efectos de sonido.
    
    Args:
        volumen: Valor entre 0.0 y 1.0
    """
    global VOLUMEN_EFECTOS
    VOLUMEN_EFECTOS = max(0.0, min(1.0, volumen))
    
    # Actualizar volumen de todos los efectos
    for efecto in efectos.values():
        efecto.set_volume(VOLUMEN_EFECTOS) 