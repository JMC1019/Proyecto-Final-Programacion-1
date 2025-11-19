# Sistema de Verificación de Contraseñas Comprometidas (SHA-512)

Este proyecto es una herramienta de consola desarrollada en Python que permite a los usuarios **comparar hashes de contraseñas** de una lista de prueba contra una lista de hashes comunes conocidos para identificar cuentas comprometidas.

El sistema está diseñado para ser eficiente y modular, utilizando el poderoso algoritmo de hasheo **SHA-512**.

## Características Principales

* **Algoritmo Criptográfico:** Utiliza **SHA-512** de forma consistente para todas las operaciones de hasheo.
* **Eficiencia:** Implementa diccionarios de Python para realizar la búsqueda de coincidencias en tiempo casi constante, optimizando el rendimiento.
* **Doble Modo de Carga:** Permite cargar la lista de hashes comunes desde un archivo pre-hasheado o generarla al momento desde un archivo de texto plano.
* **Reporte Detallado:** Muestra el número de contraseñas analizadas, el número de coincidencias encontradas y el tiempo exacto de ejecución.
* **Historial:** Muestra un historial completo de las contraseñas comprometidas encontradas, incluyendo la contraseña original y recomendaciones de seguridad.

## Uso del Sistema

### Requisitos

Asegúrate de tener **Python** instalado en tu sistema.

### Ejecución

1.  Guarda el código principal como `Verificación de Contraseñas.py` (o el nombre que uses).
2.  Abre tu terminal en el directorio del proyecto y ejecuta:

    ```bash
    python Verificación de Contraseñas.py
    ```

### Opciones del Menú

El sistema presenta las siguientes opciones interactivas:

| Opción | Comando | Descripción |
| :---: | :--- | :--- |
| **1** | `Comparar contraseñas` | Ejecuta la comparación. Prioriza los hashes cargados en **memoria** (Opción 2) y, si no existen, solicita el archivo de hashes comunes. |
| **2** | `Generar y Cargar Hashes Comunes (Desde texto plano)` | **Recomendada para la primera vez.** Solicita un archivo de texto plano con contraseñas (una por línea), las hashea a SHA-512, las carga en memoria, y opcionalmente las guarda en un archivo `contraseña:hash` para futuro uso. |
| **3** | `Mostrar historial` | Muestra los resultados detallados de la última comparación, incluyendo la contraseña original y su hash, junto con recomendaciones. |
| **4** | `Salir` | Finaliza la aplicación. |

## Formato de Archivos y Nombres Esperados

Para que el sistema funcione correctamente, los archivos de entrada deben tener el siguiente formato y se espera que usen estos nombres (o los que solicite la consola):

| Archivo | Contenido | Ejemplo de Formato | Opción del Menú |
| :--- | :--- | :--- | :---: |
| **`contraseñas sin hash.txt`** | Lista de contraseñas de texto plano (una por línea). | `clave123` | **2** (Input) |
| **`hashes comunes.txt`** | Pares de contraseña y su hash SHA-512 pre-generados. | `123456:hash_sha512_completo` | **1** (Input/Output) |
| **`contraseñas de prueba.txt`** | Pares de usuario y su hash SHA-512. | `usuario1:hash_sha512_completo` | **1** (Input) |

