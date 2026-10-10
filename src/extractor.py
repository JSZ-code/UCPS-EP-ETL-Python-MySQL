
import csv
from pathlib import Path


class ExtractorCSV:
    COLUMNAS_REQUERIDAS = {
        "id_transaccion",
        "producto",
        "cantidad",
        "precio_unitario",
        "fecha_registro",
        "correo_empleado",
    }

    def __init__(self, ruta_archivo):
        self.ruta_archivo = Path(ruta_archivo)

    def extraer(self):
        try:
            with self.ruta_archivo.open(
                mode="r", encoding="utf-8-sig", newline=""
            ) as archivo:
                lector = csv.DictReader(archivo)

                if lector.fieldnames is None:
                    raise ValueError("El archivo CSV no contiene encabezados.")

                columnas = set(lector.fieldnames)
                faltantes = self.COLUMNAS_REQUERIDAS - columnas

                if faltantes:
                    raise ValueError(
                        f"Faltan columnas obligatorias: {sorted(faltantes)}"
                    )

                registros = list(lector)

                print(f"[EXTRACT] Registros leidos: {len(registros)}")
                return registros

        except FileNotFoundError:
            print(f"[ERROR] Archivo no encontrado: {self.ruta_archivo}")
            raise

        except (UnicodeError, csv.Error, OSError, ValueError) as error:
            print(f"[ERROR] No se pudo leer el CSV: {error}")
            raise
