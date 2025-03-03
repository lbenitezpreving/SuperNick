import pygame
import os

# Directorios de recursos
DIR_PRINCIPAL = os.path.dirname(os.path.abspath(__file__))
DIR_ASSETS = os.path.join(DIR_PRINCIPAL, "assets")
DIR_IMAGENES = os.path.join(DIR_ASSETS, "images")
DIR_SONIDOS = os.path.join(DIR_ASSETS, "sounds")
DIR_FUENTES = os.path.join(DIR_ASSETS, "fonts")

# Diccionarios para almacenar recursos
imagenes = {}
sonidos = {}
fuentes = {}

def cargar_imagen(nombre, escala=1):
    """Carga una imagen desde el directorio de imágenes."""
    if nombre in imagenes:
        return imagenes[nombre]
    
    try:
        ruta_completa = os.path.join(DIR_IMAGENES, nombre)
        imagen = pygame.image.load(ruta_completa).convert_alpha()
        
        if escala != 1:
            ancho_original = imagen.get_width()
            alto_original = imagen.get_height()
            nuevo_ancho = int(ancho_original * escala)
            nuevo_alto = int(alto_original * escala)
            imagen = pygame.transform.scale(imagen, (nuevo_ancho, nuevo_alto))
            
        imagenes[nombre] = imagen
        return imagen
    except pygame.error as e:
        print(f"No se pudo cargar la imagen {nombre}: {e}")
        # Crear una superficie de reemplazo (para desarrollo)
        superficie = pygame.Surface((50, 50))
        superficie.fill((255, 0, 255))  # Magenta para indicar error
        return superficie

def cargar_sonido(nombre):
    """Carga un sonido desde el directorio de sonidos."""
    if nombre in sonidos:
        return sonidos[nombre]
    
    try:
        ruta_completa = os.path.join(DIR_SONIDOS, nombre)
        sonido = pygame.mixer.Sound(ruta_completa)
        sonidos[nombre] = sonido
        return sonido
    except pygame.error as e:
        print(f"No se pudo cargar el sonido {nombre}: {e}")
        return None

def cargar_fuente(nombre, tamaño):
    """Carga una fuente desde el directorio de fuentes o usa la predeterminada."""
    clave = f"{nombre}_{tamaño}"
    
    if clave in fuentes:
        return fuentes[clave]
    
    try:
        ruta_completa = os.path.join(DIR_FUENTES, nombre)
        fuente = pygame.font.Font(ruta_completa, tamaño)
        fuentes[clave] = fuente
        return fuente
    except pygame.error as e:
        print(f"No se pudo cargar la fuente {nombre}: {e}")
        # Usar fuente predeterminada
        fuente = pygame.font.Font(None, tamaño)
        fuentes[clave] = fuente
        return fuente

def crear_imagenes_temporales():
    """Crea imágenes temporales para desarrollo."""
    # Personaje (Nick)
    nick_img = pygame.Surface((30, 50))
    nick_img.fill((255, 0, 0))  # Rojo
    imagenes["nick.png"] = nick_img
    
    # Plataforma
    plataforma_img = pygame.Surface((100, 20))
    plataforma_img.fill((0, 255, 0))  # Verde
    imagenes["plataforma.png"] = plataforma_img
    
    # Enemigo
    enemigo_img = pygame.Surface((30, 30))
    enemigo_img.fill((255, 0, 255))  # Magenta
    imagenes["enemigo.png"] = enemigo_img
    
    # Moneda
    moneda_img = pygame.Surface((15, 15))
    moneda_img.fill((255, 255, 0))  # Amarillo
    pygame.draw.circle(moneda_img, (255, 215, 0), (7, 7), 7)  # Círculo dorado
    imagenes["moneda.png"] = moneda_img
    
    # Fondo
    fondo_img = pygame.Surface((800, 600))
    fondo_img.fill((107, 140, 255))  # Azul cielo
    imagenes["fondo.png"] = fondo_img

def inicializar_recursos():
    """Inicializa todos los recursos necesarios para el juego."""
    # Por ahora, creamos imágenes temporales
    crear_imagenes_temporales()
    
    # Aquí se cargarían los recursos reales cuando estén disponibles
    # Por ejemplo:
    # cargar_imagen("nick.png")
    # cargar_imagen("plataforma.png")
    # cargar_sonido("salto.wav")
    # etc. 