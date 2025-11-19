import hashlib
import time
import os
historial_resultados = []
hashes_comunes_en_memoria = None

def hashear_contraseña(contraseña):
    return hashlib.sha512(contraseña.encode()).hexdigest()

def cargar_contraseñas_prueba(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contraseñas = {}
            for linea in f:
                linea = linea.strip()
                if ':' in linea:
                    usuario, hash_contraseña = linea.split(':', 1)
                    contraseñas[usuario] = hash_contraseña
            return contraseñas
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'")
        return None
    except Exception as e:
        print(f"Error al leer el archivo '{archivo}': {e}")
        return None

def cargar_hashes_comunes_desde_archivo(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            hashes_dict = {}
            for linea in f:
                linea = linea.strip()
                if ':' in linea:
                    contraseña_original, hash_contraseña = linea.split(':', 1)
                    hashes_dict[hash_contraseña] = contraseña_original
            return hashes_dict
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'")
        return None
    except Exception as e:
        print(f"Error al leer el archivo '{archivo}': {e}")
        return None

def generar_y_cargar_hashes_comunes():
    global hashes_comunes_en_memoria

    archivo_entrada = input("Ingrese el nombre del archivo con contraseñas SIN HASHEAR (.txt): ").strip()

    if not os.path.exists(archivo_entrada):
        print(f"\nError: El archivo de entrada '{archivo_entrada}' no se encontró.")
        return

    hashes_dict_temp = {}
    contraseñas_procesadas = 0
    tiempo_inicio = time.time()

    print(f"\nProcesando y cargando contraseñas desde '{archivo_entrada}' usando SHA-512...")

    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f_entrada:

            for linea in f_entrada:
                contraseña_original = linea.strip()

                if not contraseña_original:
                    continue

                hash_contraseña = hashear_contraseña(contraseña_original)

                hashes_dict_temp[hash_contraseña] = contraseña_original
                contraseñas_procesadas += 1

        hashes_comunes_en_memoria = hashes_dict_temp
        tiempo_total = time.time() - tiempo_inicio

        print(f"\nCarga y Hasheo finalizados.")
        print(f"Contraseñas cargadas en memoria: {contraseñas_procesadas}")
        print(f"Tiempo de procesamiento: {tiempo_total:.4f} segundos")

        if contraseñas_procesadas > 0:
            guardar = input("\n¿Desea guardar estos hashes en un nuevo archivo? (S/N): ").strip().upper()

            if guardar == 'S':
                nombre_sugerido = archivo_entrada.replace(".txt", "_hashes_sha512.txt")
                archivo_salida = input(
                    f"Ingrese el nombre del archivo de salida (Sugerido: {nombre_sugerido}): ").strip()
                if not archivo_salida:
                    archivo_salida = nombre_sugerido

                with open(archivo_salida, 'w', encoding='utf-8') as f_salida:
                    for hash_valor, contraseña_original in hashes_dict_temp.items():
                        f_salida.write(f"{contraseña_original}:{hash_valor}\n")

                print(f"Archivo guardado exitosamente como: '{archivo_salida}'")

        print("\n¡Puede usar la Opción 1 para comparar ahora! Los hashes comunes están listos en memoria.")

    except Exception as e:
        print(f"\nOcurrió un error al procesar el archivo: {e}")
        hashes_comunes_en_memoria = None

def comparar_contraseñas():
    global historial_resultados
    global hashes_comunes_en_memoria

    contraseñas_prueba = None
    hashes_comunes = None

    if hashes_comunes_en_memoria is not None:
        print("\nUsando hashes comunes ya cargados en memoria.")
        hashes_comunes = hashes_comunes_en_memoria
    else:
        print("\nNo hay hashes comunes cargados en memoria.")
        archivo_comunes = input("Ingrese el nombre del archivo con hashes comunes (contraseña:hash): ").strip()

        print("Cargando archivo de hashes comunes...")
        hashes_comunes = cargar_hashes_comunes_desde_archivo(archivo_comunes)
        if hashes_comunes is None:
            return

    archivo_prueba = input("Ingrese el nombre del archivo con contraseñas de prueba (usuario:hash): ").strip()
    print("Cargando archivo de prueba...")
    contraseñas_prueba = cargar_contraseñas_prueba(archivo_prueba)
    if contraseñas_prueba is None:
        return

    print("Comparando contraseñas...")
    tiempo_inicio = time.time()
    historial_resultados = []
    contraseñas_encontradas = 0

    for usuario, hash_contraseña in contraseñas_prueba.items():
        if hash_contraseña in hashes_comunes:
            contraseñas_encontradas += 1
            historial_resultados.append({
                'usuario': usuario,
                'hash': hash_contraseña,
                'contraseña_original': hashes_comunes[hash_contraseña]
            })

    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio

    print(f"\n{'=' * 60}")
    print(f"RESULTADOS DE LA COMPARACIÓN")
    print(f"{'=' * 60}")
    print(f"Contraseñas analizadas: {len(contraseñas_prueba)}")
    print(f"Contraseñas encontradas en la lista común: {contraseñas_encontradas}")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")
    print(f"{'=' * 60}\n")

def mostrar_historial():
    if not historial_resultados:
        print("\nNo hay resultados para mostrar. Primero ejecute la comparación.\n")
        return

    print(f"\n{'=' * 60}")
    print(f"HISTORIAL DE CONTRASEÑAS COMPROMETIDAS")
    print(f"{'=' * 60}\n")

    for i, resultado in enumerate(historial_resultados, 1):
        usuario = resultado['usuario']
        hash_contraseña = resultado['hash']
        contraseña_original = resultado['contraseña_original']

        print(f"{i}. Usuario: {usuario}")
        print(f"   Contraseña: {contraseña_original}")
        print(f"   Hash: {hash_contraseña}")

        if len(contraseña_original) < 8:
            print(f"RECOMENDACIÓN: La contraseña debe ser de mínimo 8 dígitos")

        print()

    print(f"{'=' * 60}")
    print(f"Total de contraseñas comprometidas: {len(historial_resultados)}")
    print(f"{'=' * 60}\n")

def mostrar_menu():
    print("\n" + "=" * 60)
    print(" SISTEMA DE VERIFICACIÓN DE CONTRASEÑAS")
    print("=" * 60)
    print("1. Comparar contraseñas (Usando hashes cargados o archivo)")
    print("2. Generar y Cargar Hashes Comunes (Desde texto plano)")
    print("3. Mostrar historial")
    print("4. Salir")
    print("=" * 60)

def main():
    print("\n¡Bienvenido al Sistema de Verificación de Contraseñas!")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == '1':
            comparar_contraseñas()
        elif opcion == '2':
            generar_y_cargar_hashes_comunes()
        elif opcion == '3':
            mostrar_historial()
        elif opcion == '4':
            print("\n¡Gracias por usar el sistema! Hasta luego.\n")
            break
        else:
            print("\nOpción inválida. Por favor, seleccione una opción del 1 al 4.\n")

if __name__ == "__main__":
    main()