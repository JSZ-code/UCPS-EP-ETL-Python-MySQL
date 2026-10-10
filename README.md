
# Examen Practico UCPS - Proceso ETL en Python y MySQL

## Descripcion

Implementacion de un proceso ETL (Extract, Transform, Load)
utilizando Python, Programacion Orientada a Objetos (POO)
y una base de datos relacional MySQL.

Curso: Desarrollo de Aplicaciones Empresariales.
Docente: Ing. Eder Tejada Mellado.

## Objetivo

Procesar el archivo transacciones_almacen.csv,
corregir inconsistencias y almacenar los registros
validos en la tabla historial_ventas de MySQL.

## Tecnologias

- Python 3.12
- MySQL 8.0
- mysql-connector-python
- python-dotenv
- Git y GitHub
- Visual Studio Code

## Arquitectura

El proyecto utiliza cuatro clases principales:

- ExtractorCSV: lectura y validacion del archivo CSV.
- Transformador: limpieza, normalizacion y calculos.
- RepositorioMySQL: acceso y persistencia de datos.
- ProcesoETL: coordinacion del proceso completo.

## Fases ETL

### Extract

Lee el CSV y verifica la existencia de las columnas
obligatorias, manejando errores de lectura.

### Transform

- Elimina espacios en blanco innecesarios.
- Convierte nombres de productos a mayusculas.
- Convierte correos electronicos a minusculas.
- Descarta cantidades y precios invalidos.
- Estandariza fechas al formato YYYY-MM-DD.
- Calcula total_venta = cantidad * precio_unitario.

### Load

- Conecta Python con MySQL.
- Crea automaticamente la tabla historial_ventas.
- Inserta registros mediante executemany().
- Confirma transacciones con commit().
- Ejecuta rollback() ante errores.
- Evita insertar IDs que ya existen.

## Instalacion

Crear el entorno virtual:

    python -m venv .venv

Activar en PowerShell:

    .\.venv\Scripts\Activate.ps1

Instalar dependencias:

    python -m pip install -r requirements.txt

## Configuracion

Crear un archivo .env con las variables:

    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_USER=USUARIO_MYSQL
    DB_PASSWORD=CONTRASEÑA_LOCAL
    DB_NAME=ucps_etl_examen

La base de datos ucps_etl_examen debe existir previamente.
La tabla historial_ventas se crea automaticamente
desde el programa.

No publicar el archivo .env con credenciales reales.

## Ejecucion

Desde la carpeta principal:

    python main.py

## Resultados verificados

- Registros extraidos: 100
- Registros validos: 97
- Registros descartados: 3
- Registros cargados inicialmente: 97
- Importe total registrado: 229195.00
- Registros nuevos en segunda ejecucion: 0

## Consulta de verificacion

    SELECT *
    FROM ucps_etl_examen.historial_ventas;

## Pruebas realizadas

- Extraccion del CSV.
- Transformacion y descarte de registros invalidos.
- Insercion parametrizada en MySQL.
- Verificacion de datos mediante SELECT.
- Prueba de rollback ante error por duplicado.
- Segunda ejecucion sin inserciones duplicadas.

## Autor

Proyecto academico desarrollado para el curso
Desarrollo de Aplicaciones Empresariales - UCPS.
