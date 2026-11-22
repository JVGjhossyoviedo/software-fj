"""
Módulo de excepciones personalizadas de Software FJ.

Se define una jerarquía con una excepción base, de modo que el sistema pueda
capturar cualquier error propio con un solo ``except ErrorSoftwareFJ`` y, al
mismo tiempo, distinguir cada situación particular con una subclase.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de la aplicación. Todas las demás heredan de ella."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se invoca una operación sin un dato obligatorio (None o vacío)."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Los datos personales de un cliente no cumplen las validaciones."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Los parámetros con los que se crea o usa un servicio son inválidos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado existe, pero no está disponible para reservar."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Una reserva no puede crearse o procesarse con los datos recibidos."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """La operación no es válida para el estado actual del objeto."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Un cálculo de costos produjo un resultado inválido o no se pudo hacer."""
