"""
Clase Reserva: integra cliente, servicio, duración y estado.
"""

from entidades import EntidadBase
from excepciones import (
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from registro import log

# Estados posibles de una reserva.
PENDIENTE = "PENDIENTE"
CONFIRMADA = "CONFIRMADA"
CANCELADA = "CANCELADA"
PROCESADA = "PROCESADA"


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, codigo: str, cliente, servicio, horas: float):
        super().__init__(codigo)
        if cliente is None or servicio is None:
            raise ParametroFaltanteError("La reserva requiere cliente y servicio.")
        try:
            # Se valida la duración ya al crear la reserva (falla temprano).
            servicio.validar_parametros(horas)
        except ErrorSoftwareFJ as error:
            raise ReservaInvalidaError(
                f"No se puede crear la reserva {codigo}."
            ) from error
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = PENDIENTE
        self._costo = None

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo(self):
        return self._costo

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    def confirmar(self) -> None:
        """Pasa la reserva de PENDIENTE a CONFIRMADA si el servicio sigue libre."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se confirman reservas PENDIENTES (estado: {self._estado})."
            )
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' no está disponible."
            )
        self._estado = CONFIRMADA
        log.info(f"Reserva {self.identificador} confirmada.")

    def cancelar(self) -> None:
        """Cancela la reserva, salvo que ya esté cancelada o procesada."""
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado}."
            )
        self._estado = CANCELADA
        log.info(f"Reserva {self.identificador} cancelada.")

    def procesar(self, impuesto=None, descuento=None) -> float:
        """
        Calcula el costo y deja la reserva PROCESADA.

        Usa try/except/else/finally: el ``else`` solo corre si el cálculo
        funcionó, y el ``finally`` deja siempre rastro en el log.
        """
        if self._estado != CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas CONFIRMADAS (estado: {self._estado})."
            )
        try:
            costo = self._servicio.calcular_costo_total(
                self._horas, impuesto, descuento
            )
        except ErrorSoftwareFJ as error:
            # Encadenamiento de excepciones: el error original queda como causa.
            raise ReservaInvalidaError(
                f"La reserva {self.identificador} no pudo procesarse."
            ) from error
        else:
            self._costo = costo
            self._estado = PROCESADA
            log.info(f"Reserva {self.identificador} procesada. Total: ${costo:,.2f}")
            return costo
        finally:
            log.debug(f"Fin del intento de procesar la reserva {self.identificador}.")

    def describir(self) -> str:
        return (f"Reserva {self.identificador} | {self._cliente.nombre} | "
                f"{self._servicio.nombre} | {self._horas} h | {self._estado}")
