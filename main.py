
from pathlib import Path

from src.proceso_etl import ProcesoETL


def main():
    ruta_csv = Path(__file__).resolve().parent / "transacciones_almacen.csv"

    proceso = ProcesoETL(ruta_csv)
    proceso.ejecutar()


if __name__ == "__main__":
    main()
