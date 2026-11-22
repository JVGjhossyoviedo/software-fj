"""
Servicios de Software FJ: clase abstracta Servicio y tres servicios concretos.

Python no tiene sobrecarga de métodos como Java o C++, así que se simula con
parámetros opcionales y con despacho según el tipo del argumento recibido
(por ejemplo, un descuento puede ser un porcentaje o un código promocional).
"""

from abc import abstractmethod
from typing import Optional, Union

from entidades import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)

IVA_POR_DEFECTO = 0.19
CODIGOS_DESCUENTO = {"VIP": 0.10, "PROMO": 0.05}


class Servicio(EntidadBase):
    """Clase abstracta: define lo que todo servicio debe saber hacer."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float):
        super().__init__(codigo)
        if nombre is None or not str(nombre).strip():
            raise ParametroFaltanteError("El servicio requiere un nombre.")
        # bool es subclase de int: se descarta explícitamente.
        if isinstance(tarifa_hora, bool) or not isinstance(tarifa_hora, (int, float)):
            raise ServicioInvalidoError("La tarifa por hora debe ser numérica.")
        if tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser mayor que cero.")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    # --------------------------- propiedades ---------------------------
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    def cambiar_disponibilidad(self, disponible: bool) -> None:
        """Habilita o deshabilita el servicio para nuevas reservas."""
        self._disponible = bool(disponible)

    # ------------------- métodos que cada servicio redefine ------------
    @abstractmethod
    def validar_parametros(self, horas: float) -> None:
        """Lanza ServicioInvalidoError si la duración no es válida."""

    @abstractmethod
    def calcular_costo_base(self, horas: float) -> float:
        """Costo del servicio sin impuestos ni descuentos."""

    @abstractmethod
    def describir(self) -> str:
        """Descripción del servicio."""

    # ---------------- método sobrecargado (variantes de uso) -----------
    def calcular_costo_total(
        self,
        horas: float,
        impuesto: Optional[float] = None,
        descuento: Union[float, str, None] = None,
    ) -> float:
        """
        Calcula el costo final. Variantes de llamada:

        - ``calcular_costo_total(3)``                  -> solo IVA por defecto.
        - ``calcular_costo_total(3, 0.0)``             -> sin impuesto.
        - ``calcular_costo_total(3, 0.19, 0.10)``      -> descuento porcentual.
        - ``calcular_costo_total(3, 0.19, "VIP")``     -> descuento por código.
        """
        self.validar_parametros(horas)
        try:
            base = self.calcular_costo_base(horas)
            tasa_impuesto = IVA_POR_DEFECTO if impuesto is None else impuesto
            if not 0 <= tasa_impuesto <= 1:
                raise ValueError(f"Impuesto fuera de rango: {tasa_impuesto}")
            tasa_descuento = self._resolver_descuento(descuento)
            total = base * (1 - tasa_descuento) * (1 + tasa_impuesto)
        except (TypeError, ValueError) as error:
            # Encadenamiento: se conserva el error original como causa.
            raise CalculoInconsistenteError(
                f"No fue posible calcular el costo de '{self.nombre}'."
            ) from error

        if total <= 0:
            raise CalculoInconsistenteError("El costo calculado no es positivo.")
        return round(total, 2)

    @staticmethod
    def _resolver_descuento(descuento: Union[float, str, None]) -> float:
        """Convierte un descuento (None, porcentaje o código) a porcentaje."""
        if descuento is None:
            return 0.0
        if isinstance(descuento, str):
            codigo = descuento.strip().upper()
            if codigo not in CODIGOS_DESCUENTO:
                raise ValueError(f"Código de descuento desconocido: '{descuento}'")
            return CODIGOS_DESCUENTO[codigo]
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise TypeError("El descuento debe ser número o código.")
        if not 0 <= descuento <= 0.5:
            raise ValueError(f"El descuento debe estar entre 0 y 0.5: {descuento}")
        return float(descuento)

    @staticmethod
    def _validar_rango_horas(horas: float, minimo: float, maximo: float) -> None:
        """Validación común de la duración, reutilizada por las subclases."""
        if horas is None:
            raise ParametroFaltanteError("La duración es obligatoria.")
        if isinstance(horas, bool) or not isinstance(horas, (int, float)):
            raise ServicioInvalidoError("La duración debe ser numérica.")
        if not minimo <= horas <= maximo:
            raise ServicioInvalidoError(
                f"Duración {horas} h fuera del rango permitido ({minimo}-{maximo} h)."
            )


class ReservaSala(Servicio):
    """Reserva de salas de reuniones, con recargo por sala grande."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, capacidad: int):
        super().__init__(codigo, nombre, tarifa_hora)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, horas: float) -> None:
        self._validar_rango_horas(horas, 1, 12)

    def calcular_costo_base(self, horas: float) -> float:
        base = self.tarifa_hora * horas
        # Las salas de más de 20 personas tienen un recargo del 15 %.
        return base * 1.15 if self._capacidad > 20 else base

    def describir(self) -> str:
        return (f"Sala '{self.nombre}' (capacidad {self._capacidad} personas) "
                f"- ${self.tarifa_hora:,.0f}/h")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos, con depósito fijo no reembolsable."""

    DEPOSITO = 20000.0

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, tipo_equipo: str):
        super().__init__(codigo, nombre, tarifa_hora)
        if tipo_equipo is None or not str(tipo_equipo).strip():
            raise ParametroFaltanteError("Debe indicar el tipo de equipo.")
        self._tipo_equipo = str(tipo_equipo).strip()

    def validar_parametros(self, horas: float) -> None:
        self._validar_rango_horas(horas, 1, 72)

    def calcular_costo_base(self, horas: float) -> float:
        return self.tarifa_hora * horas + self.DEPOSITO

    def describir(self) -> str:
        return (f"Equipo '{self.nombre}' ({self._tipo_equipo}) "
                f"- ${self.tarifa_hora:,.0f}/h + depósito ${self.DEPOSITO:,.0f}")


class AsesoriaEspecializada(Servicio):
    """Asesoría con un especialista; el nivel modifica la tarifa."""

    FACTOR_NIVEL = {"junior": 1.0, "senior": 1.5}

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float,
                 especialidad: str, nivel: str = "junior"):
        super().__init__(codigo, nombre, tarifa_hora)
        if especialidad is None or not str(especialidad).strip():
            raise ParametroFaltanteError("Debe indicar la especialidad.")
        nivel = str(nivel).strip().lower()
        if nivel not in self.FACTOR_NIVEL:
            raise ServicioInvalidoError(
                f"Nivel '{nivel}' inválido. Opciones: {list(self.FACTOR_NIVEL)}."
            )
        self._especialidad = str(especialidad).strip()
        self._nivel = nivel

    def validar_parametros(self, horas: float) -> None:
        self._validar_rango_horas(horas, 1, 8)

    def calcular_costo_base(self, horas: float) -> float:
        return self.tarifa_hora * horas * self.FACTOR_NIVEL[self._nivel]

    def describir(self) -> str:
        return (f"Asesoría de {self._especialidad} (nivel {self._nivel}) "
                f"- ${self.tarifa_hora:,.0f}/h")
