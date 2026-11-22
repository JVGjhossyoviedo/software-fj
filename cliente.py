"""
Clase Cliente: encapsula los datos personales y los valida de forma estricta.
"""

import re

from entidades import EntidadBase
from excepciones import ClienteInvalidoError, ParametroFaltanteError

# Expresión regular sencilla para validar correos (usuario@dominio.ext).
_PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(EntidadBase):
    """Cliente de Software FJ con atributos privados y validados."""

    def __init__(self, documento: str, nombre: str, correo: str, telefono: str):
        # El documento actúa como identificador único del cliente.
        super().__init__(documento)
        # Cada asignación pasa por su setter, que contiene la validación.
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---------------------------- documento ----------------------------
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError(
                f"Documento '{valor}' inválido: debe tener entre 6 y 12 dígitos."
            )
        self._documento = valor

    # ------------------------------ nombre -----------------------------
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        valor = str(valor).strip()
        # Se aceptan letras (con tildes y ñ) y espacios, mínimo 3 caracteres.
        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise ClienteInvalidoError(
                f"Nombre '{valor}' inválido: solo letras y mínimo 3 caracteres."
            )
        self._nombre = valor.title()

    # ------------------------------ correo -----------------------------
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")
        valor = str(valor).strip().lower()
        if not _PATRON_CORREO.match(valor):
            raise ClienteInvalidoError(f"Correo '{valor}' con formato inválido.")
        self._correo = valor

    # ----------------------------- teléfono ----------------------------
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError(
                f"Teléfono '{valor}' inválido: debe tener exactamente 10 dígitos."
            )
        self._telefono = valor

    def describir(self) -> str:
        return f"Cliente [{self.documento}] {self.nombre} <{self.correo}>"
