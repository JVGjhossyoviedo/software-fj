"""
Gestor central del sistema: mantiene las listas internas (sin base de datos)
y ejecuta cada operación protegida, de modo que ningún error detenga la app.
"""

from cliente import Cliente
from excepciones import ClienteInvalidoError, ErrorSoftwareFJ, ReservaInvalidaError, ServicioInvalidoError
from registro import log
from reserva import Reserva


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en listas internas."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._contador_reservas = 0

    # ------------------------------ consultas ----------------------------
    @property
    def clientes(self):
        return tuple(self._clientes)  # copia inmutable: protege la lista interna

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    def _buscar(self, lista, identificador):
        for elemento in lista:
            if elemento.identificador == str(identificador):
                return elemento
        return None

    # ----------------------------- registros -----------------------------
    def registrar_cliente(self, documento, nombre, correo, telefono):
        """Crea y guarda un cliente. Devuelve None si hubo un error."""
        try:
            if self._buscar(self._clientes, documento) is not None:
                raise ClienteInvalidoError(f"El cliente {documento} ya existe.")
            cliente = Cliente(documento, nombre, correo, telefono)
        except ErrorSoftwareFJ as error:
            log.error(f"Registro de cliente fallido: {error}")
            return None
        else:
            self._clientes.append(cliente)
            log.info(f"Cliente registrado: {cliente.describir()}")
            return cliente
        finally:
            log.debug("Operación 'registrar_cliente' finalizada.")

    def registrar_servicio(self, clase_servicio, *args, **kwargs):
        """Crea y guarda un servicio de cualquier subclase de Servicio."""
        try:
            servicio = clase_servicio(*args, **kwargs)
            if self._buscar(self._servicios, servicio.identificador) is not None:
                raise ServicioInvalidoError(
                    f"El servicio {servicio.identificador} ya existe."
                )
        except ErrorSoftwareFJ as error:
            log.error(f"Registro de servicio fallido: {error}")
            return None
        except TypeError as error:
            # Faltan o sobran argumentos al construir el servicio.
            log.error(f"Registro de servicio fallido (argumentos): {error}")
            return None
        else:
            self._servicios.append(servicio)
            log.info(f"Servicio registrado: {servicio.describir()}")
            return servicio

    # ------------------------------ reservas -----------------------------
    def crear_reserva(self, documento_cliente, codigo_servicio, horas):
        """Crea una reserva PENDIENTE buscando cliente y servicio por código."""
        try:
            cliente = self._buscar(self._clientes, documento_cliente)
            servicio = self._buscar(self._servicios, codigo_servicio)
            if cliente is None:
                raise ReservaInvalidaError(f"Cliente {documento_cliente} no existe.")
            if servicio is None:
                raise ReservaInvalidaError(f"Servicio {codigo_servicio} no existe.")
            reserva = Reserva(f"R{self._contador_reservas + 1:03d}", cliente, servicio, horas)
        except ErrorSoftwareFJ as error:
            self._registrar_error("Creación de reserva fallida", error)
            return None
        # El consecutivo solo avanza cuando la reserva se creó con éxito.
        self._contador_reservas += 1
        self._reservas.append(reserva)
        log.info(f"Reserva creada: {reserva.describir()}")
        return reserva

    def ejecutar_reserva(self, reserva, impuesto=None, descuento=None):
        """Confirma y procesa una reserva. Devuelve el costo o None si falla."""
        try:
            reserva.confirmar()
            return reserva.procesar(impuesto, descuento)
        except ErrorSoftwareFJ as error:
            self._registrar_error("Procesamiento de reserva fallido", error)
            return None

    def cancelar_reserva(self, reserva):
        """Cancela una reserva sin dejar que un error detenga el sistema."""
        try:
            reserva.cancelar()
            return True
        except ErrorSoftwareFJ as error:
            self._registrar_error("Cancelación fallida", error)
            return False

    # ------------------------------- auxiliar ----------------------------
    @staticmethod
    def _registrar_error(contexto, error):
        """Escribe el error y, si existe, la causa original encadenada."""
        causa = f" | causa: {error.__cause__!r}" if error.__cause__ else ""
        log.error(f"{contexto}: {error}{causa}")
