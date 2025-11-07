import os
import shutil
import zipfile
#import rarfile  # 🆕 Para descomprimir archivos .rar

practicas_dir = input("Nombre del directorio de prácticas")
# Directorio origen y destino
origen = practicas_dir+"/entradas"
destino = practicas_dir+"/salidas"

# Crea el destino si no existe
os.makedirs(destino, exist_ok=True)

# Recorremos los archivos del directorio origen
for archivo in os.listdir(origen):
    ruta_archivo = os.path.join(origen, archivo)

    # Solo procesamos archivos (no carpetas)
    if not os.path.isfile(ruta_archivo):
        continue

    # Buscamos la estructura esperada: nombre_numero_assignsubmission_file_algo.ext
    if "_assignsubmission_file_" in archivo:
        # Separamos nombre y número
        parte1, resto = archivo.split("_assignsubmission_file_", 1)
        
        # El nombre del alumno (con número) será parte1
        nombre_alumno = parte1

        # Creamos el directorio del alumno
        dir_alumno = os.path.join(destino, nombre_alumno)
        os.makedirs(dir_alumno, exist_ok=True)

        # El nuevo nombre de archivo será lo que viene tras "file_"
        nuevo_nombre = resto

        # Ruta destino final
        ruta_destino = os.path.join(dir_alumno, nuevo_nombre)

        # Copiamos el archivo
        shutil.copy2(ruta_archivo, ruta_destino)
        print(f"✅ Copiado: {archivo} → {ruta_destino}")

        # 🧩 Descomprimir si es un ZIP o RAR
        extension = os.path.splitext(ruta_destino)[1].lower()

        try:
            if extension == ".zip":
                with zipfile.ZipFile(ruta_destino, 'r') as zip_ref:
                    zip_ref.extractall(dir_alumno)
                print(f"📦 Descomprimido ZIP: {ruta_destino} → {dir_alumno}")

            elif extension == ".rar":
                with rarfile.RarFile(ruta_destino, 'r') as rar_ref:
                    rar_ref.extractall(dir_alumno)
                print(f"📦 Descomprimido RAR: {ruta_destino} → {dir_alumno}")

            # 🧹 Opcional: eliminar el archivo comprimido tras extraer
            # os.remove(ruta_destino)
            # print(f"🗑️ Eliminado archivo comprimido: {ruta_destino}")

        except (zipfile.BadZipFile, rarfile.Error) as e:
            print(f"❌ Error al descomprimir {ruta_destino}: {e}")

    else:
        print(f"⚠️ No coincide el patrón esperado: {archivo}")
