
from datetime import datetime
from decimal import Decimal, InvalidOperation


class Transformador:
    FORMATOS_FECHA = (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
    )

    def __init__(self):
        self.descartados = []

    def convertir_fecha(self, valor):
        for formato in self.FORMATOS_FECHA:
            try:
                return datetime.strptime(valor, formato).date()
            except ValueError:
                continue

        raise ValueError(f"Formato de fecha no reconocido: {valor}")

    def transformar(self, registros):
        self.descartados = []
        registros_limpios = []

        for numero_fila, registro in enumerate(registros, start=2):
            try:
                fila = {
                    clave: valor.strip() if isinstance(valor, str) else valor
                    for clave, valor in registro.items()
                }

                identificador = int(fila["id_transaccion"])
                producto = fila["producto"].upper()
                correo = fila["correo_empleado"].lower()

                cantidad = int(fila["cantidad"])
                precio = Decimal(fila["precio_unitario"])

                if cantidad <= 0 or precio <= 0:
                    raise ValueError("Cantidad o precio menor o igual a cero")

                if not precio.is_finite():
                    raise ValueError("Precio no finito")

                if not producto or not correo:
                    raise ValueError("Producto o correo vacio")

                fecha = self.convertir_fecha(fila["fecha_registro"])

                total = Decimal(cantidad) * precio

                registros_limpios.append({
                    "id_transaccion": identificador,
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio_unitario": precio,
                    "fecha_registro": fecha,
                    "correo_empleado": correo,
                    "total_venta": total,
                })

            except (ValueError, TypeError, InvalidOperation, KeyError) as error:
                self.descartados.append({
                    "fila": numero_fila,
                    "id": registro.get("id_transaccion"),
                    "motivo": str(error),
                })

        print(f"[TRANSFORM] Registros validos: {len(registros_limpios)}")
        print(f"[TRANSFORM] Registros descartados: {len(self.descartados)}")

        for descarte in self.descartados:
            print(
                f"[DESCARTADO] Fila {descarte['fila']} "
                f"- ID {descarte['id']}: {descarte['motivo']}"
            )

        return registros_limpios
