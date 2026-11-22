"""
Configuración del registro de eventos y errores (archivo de logs).

Se usa el módulo estándar ``logging``. Todo evento relevante queda en
``logs/software_fj.log``; los mensajes también se muestran por consola para
poder seguir la ejecución en tiempo real.
"""

import logging
import os

RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger de la aplicación, configurándolo solo una vez."""
    logger = logging.getLogger("software_fj")
    if logger.handlers:  # ya configurado: evita duplicar mensajes
        return logger

    logger.setLevel(logging.DEBUG)
    os.makedirs(RUTA_LOGS, exist_ok=True)

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # Handler de archivo: guarda todo, incluido el nivel DEBUG.
    manejador_archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    manejador_archivo.setFormatter(formato)
    logger.addHandler(manejador_archivo)

    # Handler de consola: muestra desde INFO hacia arriba.
    manejador_consola = logging.StreamHandler()
    manejador_consola.setLevel(logging.INFO)
    manejador_consola.setFormatter(formato)
    logger.addHandler(manejador_consola)

    return logger


log = obtener_logger()
