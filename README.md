# Software FJ - Sistema integral de gestión de clientes, servicios y reservas

Proyecto de la Fase 4 del curso Programación (213023), UNAD. Aplicación en Python orientada a objetos, sin base de datos, con manejo avanzado de excepciones y registro de eventos en archivo de logs.

## Requisitos
- Python 3.9 o superior (solo biblioteca estándar, no hay dependencias externas).

## Ejecución
```bash
python main.py                          # simulación de 21 operaciones
python -m unittest discover -s tests    # pruebas unitarias
```
Los eventos y errores quedan en `logs/software_fj.log`.

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`ErrorSoftwareFJ` y derivadas) |
| `registro.py` | Configuración del archivo de logs |
| `entidades.py` | Clase abstracta `EntidadBase` |
| `cliente.py` | `Cliente` con atributos encapsulados y validaciones |
| `servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | `Reserva` con `confirmar`, `cancelar` y `procesar` |
| `gestor.py` | `GestorSoftwareFJ`: listas internas y operaciones protegidas |
| `main.py` | Simulación de operaciones válidas e inválidas |
| `tests/test_sistema.py` | Pruebas unitarias |

## Conceptos aplicados
- **Abstracción:** `EntidadBase` y `Servicio` no se pueden instanciar.
- **Herencia y polimorfismo:** cada servicio redefine `validar_parametros`, `calcular_costo_base` y `describir`.
- **Encapsulación:** atributos privados con `property` y validación en los setters.
- **Sobrecarga (simulada):** `calcular_costo_total(horas, impuesto=None, descuento=None)`, donde `descuento` puede ser un porcentaje o un código.
- **Excepciones:** clases propias, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.

## Integrantes
Jhossi Oviedo
