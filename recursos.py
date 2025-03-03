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

# Lista de imágenes necesarias para el juego
IMAGENES_REQUERIDAS = [
    "nick.png",           # Personaje principal
    "nick_izquierda.png", # Personaje mirando a la izquierda
    "nick_derecha.png",   # Personaje mirando a la derecha
    "nick_salto.png",     # Personaje saltando
    "plataforma.png",     # Plataforma básica
    "enemigo.png",        # Enemigo básico
    "moneda.png",         # Moneda
    "fondo_nivel1.png",   # Fondo para el nivel 1
    "fondo_nivel2.png",   # Fondo para el nivel 2
    "fondo_nivel3.png",   # Fondo para el nivel 3
    "fondo_menu.png",     # Fondo para el menú
]

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
    imagenes["nick_izquierda.png"] = nick_img
    imagenes["nick_derecha.png"] = nick_img
    imagenes["nick_salto.png"] = nick_img
    
    # Plataforma
    plataforma_img = pygame.Surface((100, 20))
    plataforma_img.fill((0, 255, 0))  # Verde
    imagenes["plataforma.png"] = plataforma_img
    
    # Enemigo
    enemigo_img = pygame.Surface((30, 30))
    enemigo_img.fill((255, 0, 255))  # Magenta
    imagenes["enemigo.png"] = enemigo_img
    
    # No creamos una imagen temporal para moneda.png si ya existe
    if "moneda.png" not in imagenes:
        # Moneda (solo como respaldo si no se pudo cargar la imagen real)
        moneda_img = pygame.Surface((15, 15))
        moneda_img.fill((255, 255, 0))  # Amarillo
        pygame.draw.circle(moneda_img, (255, 215, 0), (7, 7), 7)  # Círculo dorado
        imagenes["moneda.png"] = moneda_img
    
    # Fondos
    fondo_img = pygame.Surface((800, 600))
    fondo_img.fill((107, 140, 255))  # Azul cielo
    imagenes["fondo_nivel1.png"] = fondo_img
    imagenes["fondo_nivel2.png"] = fondo_img
    imagenes["fondo_nivel3.png"] = fondo_img
    imagenes["fondo_menu.png"] = fondo_img

def verificar_imagenes_existentes():
    """Verifica qué imágenes existen en el directorio de imágenes."""
    imagenes_existentes = []
    imagenes_faltantes = []
    
    for nombre in IMAGENES_REQUERIDAS:
        ruta_completa = os.path.join(DIR_IMAGENES, nombre)
        if os.path.exists(ruta_completa):
            imagenes_existentes.append(nombre)
        else:
            imagenes_faltantes.append(nombre)
    
    return imagenes_existentes, imagenes_faltantes

def inicializar_recursos():
    """Inicializa todos los recursos necesarios para el juego."""
    # Verificar qué imágenes existen
    imagenes_existentes, imagenes_faltantes = verificar_imagenes_existentes()
    
    # Cargar imágenes existentes
    for nombre in imagenes_existentes:
        cargar_imagen(nombre)
        print(f"Imagen cargada: {nombre}")
    
    # Crear imágenes temporales para las que faltan
    if imagenes_faltantes:
        print("Algunas imágenes no se encontraron. Usando imágenes temporales:")
        for nombre in imagenes_faltantes:
            print(f"  - {nombre}")
        crear_imagenes_temporales()
    else:
        print("Todas las imágenes se cargaron correctamente.")
        
    # Aquí se cargarían los sonidos cuando estén disponibles
    # Por ejemplo:
    # cargar_sonido("salto.wav")
    # etc. 