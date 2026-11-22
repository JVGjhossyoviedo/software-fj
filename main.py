"""
Simulación de Software FJ: más de 10 operaciones completas, con casos
válidos e inválidos, para demostrar que el sistema sigue funcionando
aunque ocurran errores.

Ejecución:  python main.py
"""

from gestor import GestorSoftwareFJ
from registro import ARCHIVO_LOG, log
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def titulo(numero: int, texto: str) -> None:
    """Imprime un encabezado para separar las operaciones en la consola."""
    log.info(f"--- Operación {numero}: {texto} ---")


def main() -> None:
    gestor = GestorSoftwareFJ()
    log.info("===== INICIO DE LA SIMULACIÓN DE SOFTWARE FJ =====")

    # ---------------------------- CLIENTES ----------------------------
    titulo(1, "Cliente válido")
    gestor.registrar_cliente("1012345678", "ana maría gómez", "ana@correo.com", "3001234567")

    titulo(2, "Cliente válido")
    gestor.registrar_cliente("79456123", "Carlos Pérez", "carlos.perez@empresa.co", "3109876543")

    titulo(3, "Cliente inválido: correo sin formato")
    gestor.registrar_cliente("52123456", "Luisa Torres", "luisa-correo", "3201112233")

    titulo(4, "Cliente inválido: documento con letras")
    gestor.registrar_cliente("ABC123", "Pedro Ríos", "pedro@correo.com", "3151234567")

    titulo(5, "Cliente inválido: parámetro faltante (nombre None)")
    gestor.registrar_cliente("80123456", None, "x@correo.com", "3001112233")

    titulo(6, "Cliente inválido: documento duplicado")
    gestor.registrar_cliente("1012345678", "Ana Duplicada", "otra@correo.com", "3001234567")

    # ---------------------------- SERVICIOS ---------------------------
    titulo(7, "Servicio válido: sala de reuniones")
    gestor.registrar_servicio(ReservaSala, "S01", "Sala Andes", 50000, 25)

    titulo(8, "Servicio válido: alquiler de equipo")
    gestor.registrar_servicio(AlquilerEquipo, "S02", "Portátil Pro", 8000, "Computador")

    titulo(9, "Servicio válido: asesoría especializada")
    gestor.registrar_servicio(AsesoriaEspecializada, "S03", "Asesoría Cloud", 90000,
                              "Arquitectura en la nube", "senior")

    titulo(10, "Servicio inválido: tarifa negativa")
    gestor.registrar_servicio(ReservaSala, "S04", "Sala Rota", -100, 10)

    titulo(11, "Servicio inválido: nivel de asesoría desconocido")
    gestor.registrar_servicio(AsesoriaEspecializada, "S05", "Asesoría X", 70000,
                              "Datos", "experto")

    titulo(12, "Servicio inválido: faltan argumentos")
    gestor.registrar_servicio(AlquilerEquipo, "S06", "Proyector")

    # ----------------------------- RESERVAS ---------------------------
    titulo(13, "Reserva exitosa: sala 3 h con IVA por defecto")
    r1 = gestor.crear_reserva("1012345678", "S01", 3)
    print("   Total:", gestor.ejecutar_reserva(r1))

    titulo(14, "Reserva exitosa: equipo 10 h con descuento VIP")
    r2 = gestor.crear_reserva("79456123", "S02", 10)
    print("   Total:", gestor.ejecutar_reserva(r2, 0.19, "VIP"))

    titulo(15, "Reserva exitosa: asesoría 2 h, descuento 5 % y sin impuesto")
    r3 = gestor.crear_reserva("1012345678", "S03", 2)
    print("   Total:", gestor.ejecutar_reserva(r3, 0.0, 0.05))

    titulo(16, "Reserva fallida: duración fuera de rango (asesoría de 20 h)")
    gestor.crear_reserva("79456123", "S03", 20)

    titulo(17, "Reserva fallida: cliente inexistente")
    gestor.crear_reserva("99999999", "S01", 2)

    titulo(18, "Reserva fallida: servicio no disponible")
    r4 = gestor.crear_reserva("79456123", "S01", 2)
    gestor.servicios[0].cambiar_disponibilidad(False)
    print("   Total:", gestor.ejecutar_reserva(r4))
    gestor.servicios[0].cambiar_disponibilidad(True)

    titulo(19, "Cálculo inconsistente: código de descuento inexistente")
    r5 = gestor.crear_reserva("1012345678", "S02", 5)
    print("   Total:", gestor.ejecutar_reserva(r5, 0.19, "GRATIS"))

    titulo(20, "Operación no permitida: cancelar dos veces")
    print("   Primera cancelación:", gestor.cancelar_reserva(r5))
    print("   Segunda cancelación:", gestor.cancelar_reserva(r5))

    titulo(21, "Operación no permitida: procesar una reserva ya cancelada")
    print("   Total:", gestor.ejecutar_reserva(r5))

    # ------------------------------ RESUMEN ---------------------------
    log.info("===== FIN DE LA SIMULACIÓN: el sistema siguió activo =====")
    print("\nResumen final")
    print(f"  Clientes registrados : {len(gestor.clientes)}")
    print(f"  Servicios registrados: {len(gestor.servicios)}")
    print(f"  Reservas creadas     : {len(gestor.reservas)}")
    for reserva in gestor.reservas:
        print("   -", reserva.describir(), "| costo:", reserva.costo)
    print(f"  Registro de eventos en: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()
