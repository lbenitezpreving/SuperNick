"""
Módulo para gestionar la configuración del juego SuperNick.
"""

import os
import json

# Ruta del archivo de configuración
CONFIG_FILE = "config.json"

# Configuración por defecto
DEFAULT_CONFIG = {
    "pantalla": {
        "ancho": 800,
        "alto": 600,
        "fullscreen": False
    },
    "sonido": {
        "volumen_musica": 0.5,
        "volumen_efectos": 0.7,
        "musica_activada": True,
        "efectos_activados": True
    },
    "controles": {
        "izquierda": "K_LEFT",
        "derecha": "K_RIGHT",
        "saltar": "K_SPACE"
    },
    "juego": {
        "dificultad": 1,  # 1: Fácil, 2: Normal, 3: Difícil
        "vidas_iniciales": 3,
        "nivel_desbloqueado": 1
    }
}

# Variable global para almacenar la configuración actual
config = {}

def cargar_configuracion():
    """
    Carga la configuración desde el archivo. Si no existe, crea uno con la configuración por defecto.
    
    Returns:
        dict: Configuración cargada
    """
    global config
    
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                
            # Verificar que todas las claves existan, si no, usar valores por defecto
            for seccion, valores in DEFAULT_CONFIG.items():
                if seccion not in config:
                    config[seccion] = valores
                else:
                    for clave, valor in valores.items():
                        if clave not in config[seccion]:
                            config[seccion][clave] = valor
        else:
            config = DEFAULT_CONFIG.copy()
            guardar_configuracion()
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        config = DEFAULT_CONFIG.copy()
        
    return config

def guardar_configuracion():
    """
    Guarda la configuración actual en el archivo.
    
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error al guardar la configuración: {e}")
        return False

def obtener_configuracion(seccion=None, clave=None):
    """
    Obtiene un valor de la configuración.
    
    Args:
        seccion: Sección de la configuración (pantalla, sonido, etc.)
        clave: Clave específica dentro de la sección
        
    Returns:
        El valor solicitado, una sección completa o toda la configuración
    """
    if not config:
        cargar_configuracion()
        
    if seccion is None:
        return config
    
    if seccion in config:
        if clave is None:
            return config[seccion]
        
        if clave in config[seccion]:
            return config[seccion][clave]
    
    return None

def establecer_configuracion(seccion, clave, valor):
    """
    Establece un valor en la configuración.
    
    Args:
        seccion: Sección de la configuración (pantalla, sonido, etc.)
        clave: Clave específica dentro de la sección
        valor: Valor a establecer
        
    Returns:
        bool: True si se estableció correctamente, False en caso contrario
    """
    if not config:
        cargar_configuracion()
        
    if seccion in config:
        config[seccion][clave] = valor
        return guardar_configuracion()
    
    return False

def restablecer_configuracion():
    """
    Restablece la configuración a los valores por defecto.
    
    Returns:
        bool: True si se restableció correctamente, False en caso contrario
    """
    global config
    config = DEFAULT_CONFIG.copy()
    return guardar_configuracion()

def desbloquear_nivel(nivel):
    """
    Desbloquea un nivel en la configuración.
    
    Args:
        nivel: Número de nivel a desbloquear
        
    Returns:
        bool: True si se desbloqueó correctamente, False en caso contrario
    """
    nivel_actual = obtener_configuracion("juego", "nivel_desbloqueado")
    
    if nivel > nivel_actual:
        return establecer_configuracion("juego", "nivel_desbloqueado", nivel)
    
    return True  # El nivel ya estaba desbloqueado

def obtener_niveles_desbloqueados():
    """
    Obtiene la lista de niveles desbloqueados.
    
    Returns:
        list: Lista de niveles desbloqueados
    """
    nivel_desbloqueado = obtener_configuracion("juego", "nivel_desbloqueado")
    return list(range(1, nivel_desbloqueado + 1))

# Inicializar la configuración al importar el módulo
cargar_configuracion() 