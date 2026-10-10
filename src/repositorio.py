
import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


class RepositorioMySQL:
    def __init__(self):
        load_dotenv()

        self.configuracion = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }

        self.conexion = None

    def conectar(self):
        self.conexion = mysql.connector.connect(
            **self.configuracion
        )
        print("[LOAD] Conexion establecida con MySQL")

    def crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS historial_ventas (
            id_transaccion INT PRIMARY KEY,
            producto VARCHAR(150) NOT NULL,
            cantidad INT NOT NULL,
            precio_unitario DECIMAL(12,2) NOT NULL,
            fecha_registro DATE NOT NULL,
            correo_empleado VARCHAR(255) NOT NULL,
            total_venta DECIMAL(14,2) NOT NULL
        ) ENGINE=InnoDB
        """

        cursor = self.conexion.cursor()

        try:
            cursor.execute(sql)
            print("[LOAD] Tabla historial_ventas verificada")
        finally:
            cursor.close()

    def cargar(self, registros):
        if not registros:
            print("[LOAD] No hay registros para cargar")
            return 0

        cursor = self.conexion.cursor()

        try:
            ids = [
                fila["id_transaccion"]
                for fila in registros
            ]

            if len(ids) != len(set(ids)):
                raise ValueError(
                    "Existen identificadores duplicados "
                    "en el lote de origen"
                )

            # Consultar registros existentes
            marcadores = ", ".join(["%s"] * len(ids))

            cursor.execute(
                f"""
                SELECT id_transaccion
                FROM historial_ventas
                WHERE id_transaccion IN ({marcadores})
                """,
                tuple(ids)
            )

            ids_existentes = {
                fila[0] for fila in cursor.fetchall()
            }

            # Filtrar registros ya cargados
            nuevos = [
                fila for fila in registros
                if fila["id_transaccion"] not in ids_existentes
            ]

            omitidos = len(registros) - len(nuevos)

            print(
                f"[LOAD] Registros existentes omitidos: {omitidos}"
            )

            if not nuevos:
                print(
                    "[LOAD] No existen registros nuevos para insertar"
                )
                return 0

            # Insercion parametrizada
            sql = """
            INSERT INTO historial_ventas (
                id_transaccion,
                producto,
                cantidad,
                precio_unitario,
                fecha_registro,
                correo_empleado,
                total_venta
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            valores = [
                (
                    fila["id_transaccion"],
                    fila["producto"],
                    fila["cantidad"],
                    fila["precio_unitario"],
                    fila["fecha_registro"],
                    fila["correo_empleado"],
                    fila["total_venta"],
                )
                for fila in nuevos
            ]

            # Transaccion de carga
            self.conexion.start_transaction()

            cursor.executemany(sql, valores)

            insertados = cursor.rowcount

            self.conexion.commit()

            print(
                f"[LOAD] Registros nuevos insertados: {insertados}"
            )

            return insertados

        except (Error, ValueError) as error:
            if self.conexion.in_transaction:
                self.conexion.rollback()

            print(f"[ROLLBACK] Error de carga: {error}")
            raise

        finally:
            cursor.close()

    def cerrar(self):
        if self.conexion is not None:
            if self.conexion.is_connected():
                self.conexion.close()
                print("[LOAD] Conexion cerrada")
