import os
from datetime import datetime

# ==========================
# 1. CONFIGURACIÓN GENERAL
# ==========================

ARCHIVO_CONTACTOS = ""      # Agenda seleccionada
SEPARADOR = ";"             # Separador de campos


# ==========================
# 2. ARCHIVO Y AGENDAS
# ==========================

def seleccionar_agenda():
    """Selecciona una agenda existente o crea una nueva."""
    while True:
        resp = input("¿Ya tienes una agenda creada? (s/n): ").strip().lower()
        if resp in ("s", "n"):
            break
        print("Respuesta no válida. Por favor escribe 's' o 'n'.")

    # Caso: no tiene agenda
    if resp == "n":
        while True:
            crear = input("¿Quieres crear una agenda nueva? (s/n): ").strip().lower()
            if crear in ("s", "n"):
                break
            print("Respuesta no válida. Por favor escribe 's' o 'n'.")

        if crear == "n":
            print("\nNo se creó ninguna agenda. ¡Hasta pronto!")
            return None

        return crear_nueva_agenda()

    # Caso: dice que tiene agenda
    while True:
        nombre = input("Escribe el nombre de la agenda (sin extensión): ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            continue

        archivo = nombre + ".txt"

        if os.path.exists(archivo):
            print(f"Agenda seleccionada: {archivo}")
            return archivo

        print(f"\nLa agenda '{archivo}' no existe.")
        print("¿Qué deseas hacer?")
        print("1. Intentar con otro nombre")
        print("2. Crear una agenda nueva")
        print("3. Salir")

        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            continue
        elif opcion == "2":
            return crear_nueva_agenda()
        elif opcion == "3":
            print("\nSaliendo del programa. ¡Hasta pronto!")
            return None
        else:
            print("Opción no válida. Volviendo a intentar.")


def crear_nueva_agenda():
    """Crea una nueva agenda; si el nombre ya existe, permite usarla o cancelar."""
    print("\nCreación de nueva agenda.")
    print("IMPORTANTE: los nombres de agenda no pueden repetirse.\n")

    while True:
        nombre = input("Escribe un nombre para la agenda (sin extensión): ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            continue

        archivo = nombre + ".txt"

        if os.path.exists(archivo):
            print(f"\nERROR: Ya existe una agenda llamada '{archivo}'.")
            print("¿Qué deseas hacer?")
            print("1. Intentar con otro nombre")
            print("2. Usar esta agenda existente")
            print("3. Cancelar creación")

            opcion = input("Elige una opción: ").strip()
            if opcion == "1":
                continue
            elif opcion == "2":
                print(f"Usando agenda existente: {archivo}")
                return archivo
            elif opcion == "3":
                print("Creación cancelada.")
                return None
            else:
                print("Opción inválida. Volviendo a intentar.")
                continue

        try:
            with open(archivo, "w", encoding="utf-8"):
                pass
            print(f"Agenda '{archivo}' creada correctamente.")
            return archivo
        except Exception as e:
            print("Error al crear la agenda:", e)


def inicializar_archivo():
    """Crea el archivo de la agenda si no existe."""
    try:
        with open(ARCHIVO_CONTACTOS, "a", encoding="utf-8"):
            pass
    except Exception as e:
        print("Error al inicializar archivo:", e)


def cargar_contactos():
    """Lee todos los contactos desde el archivo y devuelve una lista de diccionarios."""
    lista = []
    try:
        with open(ARCHIVO_CONTACTOS, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(SEPARADOR)
                while len(partes) < 5:
                    partes.append("")
                nombre, telefono, correo, nota, fecha = partes[:5]
                lista.append({
                    "nombre": nombre,
                    "telefono": telefono,
                    "correo": correo,
                    "nota": nota,
                    "fecha": fecha
                })
    except FileNotFoundError:
        inicializar_archivo()
    except Exception as e:
        print("Error al leer archivo:", e)

    return lista


def guardar_contactos(lista):
    """Sobrescribe el archivo con la lista de contactos."""
    try:
        with open(ARCHIVO_CONTACTOS, "w", encoding="utf-8") as f:
            for c in lista:
                linea = SEPARADOR.join([
                    c["nombre"], c["telefono"], c["correo"], c["nota"], c["fecha"]
                ])
                f.write(linea + "\n")
    except Exception as e:
        print("Error al guardar contactos:", e)


def eliminar_agenda():
    """Elimina el archivo completo de la agenda actual."""
    global ARCHIVO_CONTACTOS

    if not ARCHIVO_CONTACTOS:
        print("No hay agenda activa.")
        esperar_para_volver()
        return

    print(f"\nVas a eliminar la agenda completa: {ARCHIVO_CONTACTOS}")
    print("Esta acción borrará TODO el contenido de la agenda.")
    confirm = input("Escribe 'ELIMINAR' para confirmar (o Enter para cancelar): ").strip()

    if confirm != "ELIMINAR":
        print("Operación cancelada.")
        esperar_para_volver()
        return

    try:
        os.remove(ARCHIVO_CONTACTOS)
        print("Agenda eliminada correctamente.")
    except Exception as e:
        print("Error al eliminar la agenda:", e)

    ARCHIVO_CONTACTOS = ""
    esperar_para_volver()


def esperar_para_volver():
    input("\nPresiona Enter para volver al menú principal...")


# ==========================
# 3. VALIDACIONES
# ==========================

def pedir_nombre_completo():
    while True:
        nombre = input("Nombre y apellido (o 0 para cancelar): ").strip()
        if nombre == "0":
            return None
        if not nombre:
            print("El nombre no puede estar vacío.")
            continue
        partes = [p for p in nombre.split(" ") if p]
        if len(partes) < 2:
            print("Debes ingresar nombre y apellido.")
            continue
        return nombre


def pedir_telefono():
    while True:
        telefono = input("Teléfono (8 dígitos, o 0 para cancelar): ").strip()
        if telefono == "0":
            return None
        if not telefono.isdigit():
            print("Solo se permiten números.")
            continue
        if len(telefono) != 8:
            print("Debe tener exactamente 8 dígitos.")
            continue
        return telefono


def pedir_fecha():
    while True:
        fecha_str = input("Fecha próxima reunión (dd/mm/yy, o 0 para cancelar): ").strip()
        if fecha_str == "0":
            return None
        try:
            dt = datetime.strptime(fecha_str, "%d/%m/%y")
            return dt.strftime("%d/%m/%y")  # Normalizada
        except ValueError:
            print("Formato inválido. Ejemplo válido: 05/11/25")


def pedir_correo():
    """Validación básica de correo; permite cancelar con 0."""
    while True:
        correo = input("Correo electrónico (o 0 para cancelar): ").strip()
        if correo == "0":
            return None
        if not correo:
            print("El correo no puede estar vacío.")
            continue
        if " " in correo:
            print("El correo no debe contener espacios.")
            continue
        if correo.count("@") != 1:
            print("Debe contener exactamente un '@'.")
            continue

        at = correo.find("@")
        if at == 0 or at == len(correo) - 1:
            print("No puede empezar ni terminar con '@'.")
            continue
        if "." not in correo:
            print("Debe contener al menos un '.'.")
            continue

        dot = correo.rfind(".")
        if dot < at + 2:
            print("Debe haber texto entre '@' y '.'.")
            continue
        if dot == len(correo) - 1:
            print("Debe haber texto después del '.'.")
            continue
        if ".@" in correo or "@." in correo:
            print("Formato incorrecto. Revisa la posición de '@' y '.'.")
            continue

        return correo


# ==========================
# 4. MANEJO DE FECHAS MÚLTIPLES
# ==========================

def combinar_fechas(fecha_actual, nueva_fecha):
    """
    Combina la fecha actual (puede tener varias separadas por coma)
    con una nueva fecha, normaliza, quita duplicados y ordena.
    """
    fechas = []

    if fecha_actual:
        for parte in fecha_actual.split(","):
            parte = parte.strip()
            if not parte:
                continue
            try:
                fechas.append(datetime.strptime(parte, "%d/%m/%y"))
            except ValueError:
                continue  # ignora formatos viejos raros

    try:
        fechas.append(datetime.strptime(nueva_fecha, "%d/%m/%y"))
    except ValueError:
        return fecha_actual

    fechas_unicas = sorted(set(fechas))
    return ", ".join(d.strftime("%d/%m/%y") for d in fechas_unicas)


# ==========================
# 5. OPERACIONES PRINCIPALES
# ==========================

def mostrar_menu():
    print("\n===== AGENDA DE CONTACTOS =====")
    print(f"Agenda actual: {ARCHIVO_CONTACTOS}")
    print("1. Agregar contacto")
    print("2. Listar contactos")
    print("3. Buscar contactos por nombre")
    print("4. Actualizar fecha (reemplazar)")
    print("5. Agregar nueva reunión (añadir)")
    print("6. Eliminar contacto")
    print("7. Eliminar esta agenda")
    print("8. Salir")


def listar_contactos():
    print("\n--- Lista de contactos ---")
    lista = cargar_contactos()
    if not lista:
        print("No hay contactos guardados.")
        esperar_para_volver()
        return

    for i, c in enumerate(lista, start=1):
        print(f"\nContacto #{i}")
        print(f"Nombre : {c['nombre']}")
        print(f"Teléfono : {c['telefono']}")
        print(f"Correo : {c['correo']}")
        print(f"Nota : {c['nota']}")
        print(f"Próxima(s) reunión(es) : {c['fecha']}")
    esperar_para_volver()


def agregar_contacto():
    print("\n--- Agregar nuevo contacto ---")
    nombre = pedir_nombre_completo()
    if nombre is None:
        print("Operación cancelada.")
        esperar_para_volver()
        return

    lista = cargar_contactos()
    nombre_norm = nombre.lower().strip()

    # Si ya existe, ofrecer agregar nueva reunión
    for idx, c in enumerate(lista):
        if c["nombre"].lower().strip() == nombre_norm:
            print(f"\nEl contacto '{nombre}' ya existe.")
            while True:
                resp = input("¿Deseas agregar una nueva reunión a este contacto? (s/n): ").strip().lower()
                if resp in ("s", "n"):
                    break
                print("Respuesta no válida. Escribe 's' o 'n'.")

            if resp == "s":
                nueva_fecha = pedir_fecha()
                if nueva_fecha is None:
                    print("Operación cancelada.")
                    esperar_para_volver()
                    return
                lista[idx]["fecha"] = combinar_fechas(lista[idx]["fecha"], nueva_fecha)
                guardar_contactos(lista)
                print("Reunión añadida correctamente.")
            esperar_para_volver()
            return

    telefono = pedir_telefono()
    if telefono is None:
        print("Operación cancelada.")
        esperar_para_volver()
        return

    correo = pedir_correo()
    if correo is None:
        print("Operación cancelada.")
        esperar_para_volver()
        return

    nota = input("Nota / Descripción breve: ").strip()

    fecha = pedir_fecha()
    if fecha is None:
        print("Operación cancelada.")
        esperar_para_volver()
        return

    try:
        with open(ARCHIVO_CONTACTOS, "a", encoding="utf-8") as f:
            linea = SEPARADOR.join([nombre, telefono, correo, nota, fecha])
            f.write(linea + "\n")
        print("Contacto agregado correctamente.")
    except Exception as e:
        print("Error al guardar contacto:", e)

    esperar_para_volver()


def buscar_contactos():
    print("\n--- Buscar contactos ---")
    texto = input("Ingrese parte del nombre (Enter para cancelar): ").strip().lower()
    if not texto:
        print("Búsqueda cancelada.")
        esperar_para_volver()
        return

    lista = cargar_contactos()
    encontrados = [c for c in lista if texto in c["nombre"].lower()]

    if not encontrados:
        print("No se encontraron contactos.")
        esperar_para_volver()
        return

    for i, c in enumerate(encontrados, start=1):
        print(f"\nResultado #{i}")
        print(f"Nombre: {c['nombre']}")
        print(f"Teléfono: {c['telefono']}")
        print(f"Correo: {c['correo']}")
        print(f"Nota: {c['nota']}")
        print(f"Próxima(s) reunión(es): {c['fecha']}")
    esperar_para_volver()


def actualizar_fecha():
    print("\n--- Actualizar fecha de reunión (reemplazar) ---")
    texto = input("Nombre o parte del nombre (Enter para cancelar): ").strip().lower()
    if not texto:
        print("Operación cancelada.")
        esperar_para_volver()
        return

    lista = cargar_contactos()
    coincidencias = [i for i, c in enumerate(lista) if texto in c["nombre"].lower()]

    if not coincidencias:
        print("No se encontraron contactos.")
        esperar_para_volver()
        return

    if len(coincidencias) == 1:
        idx = coincidencias[0]
    else:
        print("Se encontraron varios contactos:")
        for i, idx in enumerate(coincidencias, start=1):
            print(f"{i}. {lista[idx]['nombre']}")
        try:
            s = int(input("Elija uno (0 para cancelar): "))
            if s == 0:
                print("Operación cancelada.")
                esperar_para_volver()
                return
            idx = coincidencias[s - 1]
        except Exception:
            print("Selección inválida.")
            esperar_para_volver()
            return

    nueva_fecha = pedir_fecha()
    if nueva_fecha is None:
        print("Operación cancelada.")
        esperar_para_volver()
        return

    lista[idx]["fecha"] = nueva_fecha
    guardar_contactos(lista)
    print("Fecha actualizada.")
    esperar_para_volver()


def agregar_nueva_reunion():
    print("\n--- Agregar nueva reunión ---")
    texto = input("Nombre o parte del nombre (Enter para cancelar): ").strip().lower()
    if not texto:
        print("Operación cancelada.")
        esperar_para_volver()
        return

    lista = cargar_contactos()
    coincidencias = [i for i, c in enumerate(lista) if texto in c["nombre"].lower()]

    if not coincidencias:
        print("No se encontraron contactos.")
        esperar_para_volver()
        return

    if len(coincidencias) == 1:
        idx = coincidencias[0]
    else:
        print("Se encontraron varios contactos:")
        for i, idx in enumerate(coincidencias, start=1):
            print(f"{i}. {lista[idx]['nombre']}")
        try:
            s = int(input("Elija uno (0 para cancelar): "))
            if s == 0:
                print("Operación cancelada.")
                esperar_para_volver()
                return
            idx = coincidencias[s - 1]
        except Exception:
            print("Selección inválida.")
            esperar_para_volver()
            return

    nueva_fecha = pedir_fecha()
    if nueva_fecha is None:
        print("Operación cancelada.")
        esperar_para_volver()
        return

    lista[idx]["fecha"] = combinar_fechas(lista[idx]["fecha"], nueva_fecha)
    guardar_contactos(lista)
    print("Reunión añadida correctamente.")
    esperar_para_volver()


def eliminar_contacto():
    print("\n--- Eliminar contacto ---")
    nombre = input("Nombre y apellido exactos (Enter para cancelar): ").strip().lower()
    if not nombre:
        print("Operación cancelada.")
        esperar_para_volver()
        return

    lista = cargar_contactos()
    coincidencias = [i for i, c in enumerate(lista)
                     if c["nombre"].strip().lower() == nombre]

    if not coincidencias:
        print("No existe ese contacto.")
        esperar_para_volver()
        return

    print("Se eliminará:")
    for i in coincidencias:
        print(f"- {lista[i]['nombre']}")

    confirm = input("Escribe el nombre exacto para confirmar (Enter para cancelar): ").strip().lower()
    if not confirm:
        print("Operación cancelada.")
        esperar_para_volver()
        return
    if confirm != nombre:
        print("Confirmación incorrecta.")
        esperar_para_volver()
        return

    for i in sorted(coincidencias, reverse=True):
        lista.pop(i)

    guardar_contactos(lista)
    print("Contacto eliminado.")
    esperar_para_volver()


# ==========================
# 6. MENÚ PRINCIPAL
# ==========================

def main():
    global ARCHIVO_CONTACTOS

    agenda = seleccionar_agenda()
    if agenda is None:
        return

    ARCHIVO_CONTACTOS = agenda
    inicializar_archivo()

    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            agregar_contacto()
        elif opcion == "2":
            listar_contactos()
        elif opcion == "3":
            buscar_contactos()
        elif opcion == "4":
            actualizar_fecha()
        elif opcion == "5":
            agregar_nueva_reunion()
        elif opcion == "6":
            eliminar_contacto()
        elif opcion == "7":
            eliminar_agenda()
            break
        elif opcion == "8":
            print("Saliendo... ¡Hasta luego!")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()

