"""
Clase abstracta que representa las entidades generales del sistema.
"""

from abc import ABC, abstractmethod

from excepciones import ParametroFaltanteError


class EntidadBase(ABC):
    """
    Entidad general del sistema (cliente, servicio, reserva).

    Garantiza que todo objeto tenga un identificador y obliga a cada clase
    derivada a explicar cómo se presenta (``describir``).
    """

    def __init__(self, identificador: str):
        # Se valida aquí para que ninguna entidad nazca sin identificador.
        if identificador is None or not str(identificador).strip():
            raise ParametroFaltanteError("La entidad requiere un identificador.")
        self._identificador = str(identificador).strip()

    @property
    def identificador(self) -> str:
        """Identificador de solo lectura (encapsulación)."""
        return self._identificador

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""

    def __str__(self) -> str:
        return self.describir()
