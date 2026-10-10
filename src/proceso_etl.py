
from pathlib import Path

from src.extractor import ExtractorCSV
from src.transformador import Transformador
from src.repositorio import RepositorioMySQL


class ProcesoETL:
    def __init__(self, ruta_csv):
        self.ruta_csv = Path(ruta_csv)
        self.extractor = ExtractorCSV(self.ruta_csv)
        self.transformador = Transformador()
        self.repositorio = RepositorioMySQL()

    def ejecutar(self):
        print("=== PROCESO ETL - EXAMEN UCPS ===")

        # Fase 1: Extraccion
        registros = self.extractor.extraer()

        # Fase 2: Transformacion
        registros_limpios = self.transformador.transformar(registros)

        # Fase 3: Carga
        try:
            self.repositorio.conectar()
            self.repositorio.crear_tabla()
            insertados = self.repositorio.cargar(registros_limpios)
        finally:
            self.repositorio.cerrar()

        print("\n=== RESUMEN FINAL ETL ===")
        print(f"Registros extraidos: {len(registros)}")
        print(f"Registros validos: {len(registros_limpios)}")
        print(f"Registros descartados: {len(self.transformador.descartados)}")
        print(f"Registros insertados: {insertados}")

        return insertados
