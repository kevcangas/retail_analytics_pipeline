# 🚀 Proyecto ETL: Retail Analytics Pipeline

Este proyecto implementa una **pipeline ETL (Extract, Transform, Load)** completamente contenerizada. Simula un entorno de comercio electrónico donde se generan datos transaccionales sintéticos, se transforman utilizando **Polars** (para alto rendimiento) y se cargan en un Data Warehouse analítico.

## 📋 Tabla de Contenidos

* [Arquitectura](https://www.google.com/search?q=%23-arquitectura)
* [Estructura del Proyecto](https://www.google.com/search?q=%23-estructura-del-proyecto)
* [Requisitos Previos](https://www.google.com/search?q=%23-requisitos-previos)
* [Instalación y Ejecución](https://www.google.com/search?q=%23-instalaci%C3%B3n-y-ejecuci%C3%B3n)
* [Flujo de Trabajo (Paso a Paso)](https://www.google.com/search?q=%23-flujo-de-trabajo-paso-a-paso)
* [Detalles Técnicos](https://www.google.com/search?q=%23-detalles-t%C3%A9cnicos)

## 🏗 Arquitectura

El sistema se compone de 3 servicios orquestados con Docker Compose:

1. **Source DB (`source_db`):** Base de datos transaccional (PostgreSQL 13). Almacena datos crudos de usuarios y órdenes.
2. **Data Warehouse (`warehouse_db`):** Base de datos analítica (PostgreSQL 13). Almacena los datos procesados y limpios.
3. **ETL Job (`etl_job`):** Contenedor Python que contiene la lógica de negocio, generación de datos y el proceso ETL.

## 📂 Estructura del Proyecto

```text
.
├── docker-compose.yaml      # Orquestación de contenedores
└── etl/                     # Código fuente Python
    ├── Dockerfile           # Definición de la imagen del entorno ETL
    ├── etl.py               # Script principal del proceso ETL
    ├── generator.py         # Script para generar datos falsos (Mock Data)
    └── requirements.txt     # Dependencias (Polars, SQLAlchemy, Faker, etc.)

```

## 🛠 Requisitos Previos

* [Docker](https://www.docker.com/products/docker-desktop) instalado.
* [Docker Compose](https://docs.docker.com/compose/install/) instalado.

## 🚀 Instalación y Ejecución

### 1. Clonar y Construir

Descarga el proyecto y construye las imágenes de los contenedores:

```bash
docker-compose up --build -d

```

Esto levantará los tres contenedores. El contenedor `etl_job` se mantendrá activo (en espera) gracias al comando `tail -f /dev/null`, permitiéndonos ejecutar comandos dentro de él.

### 2. Acceder al Contenedor de ETL

Para ejecutar los scripts, necesitamos entrar a la terminal del contenedor:

```bash
docker exec -it <nombre_del_contenedor_etl> bash

```

*Nota: El nombre suele ser `nombre_carpeta_etl_job_1`. Puedes verlo ejecutando `docker ps`.*

## 🔄 Flujo de Trabajo (Paso a Paso)

Una vez dentro del contenedor (paso anterior), sigue este orden:

### Paso 1: Generar Datos de Prueba (Source)

Ejecuta el generador para poblar la base de datos transaccional con usuarios y órdenes falsas usando la librería `Faker`.

```bash
python generator.py

```

> **Salida esperada:** "Datos generados exitosamente."

### Paso 2: Ejecutar el ETL

Ejecuta el script de extracción, transformación y carga.

```bash
python etl.py

```

El script realizará lo siguiente:

1. **Extract:** Lee órdenes y usuarios de `source_db` usando SQL y Polars.
2. **Transform:** * Filtra solo órdenes con estatus `completed`.
* Convierte el país a mayúsculas.
* Calcula la columna `is_vip_order` (si el monto > 300).
* Añade fecha de auditoría.


3. **Load:** Escribe el resultado en la tabla `fact_sales` en `warehouse_db`.

## ⚙️ Detalles Técnicos

### Conexión a Bases de Datos (Host Local)

Si deseas inspeccionar las bases de datos desde tu máquina local (usando DBeaver, TablePlus, pgAdmin), usa las siguientes credenciales:

| Base de Datos | Puerto Local | Host | DB Name | User | Password |
| --- | --- | --- | --- | --- | --- |
| **Source** | `5432` | localhost | `ecommerce_db` | `user_source` | `password_source` |
| **Warehouse** | `5433` | localhost | `analytics_dw` | `user_dw` | `password_dw` |

### Stack Tecnológico

* **Python 3.9**: Lenguaje base.
* **Polars**: Motor de Dataframes ultra rápido (escrito en Rust) utilizado para las transformaciones en memoria.
* **SQLAlchemy**: Toolkit SQL para manejar conexiones y motores de base de datos.
* **Faker**: Generación de datos sintéticos realistas.
* **PostgreSQL**: Motor de base de datos relacional.

---

Hecho con fines educativos para demostrar una arquitectura ETL moderna y ligera.