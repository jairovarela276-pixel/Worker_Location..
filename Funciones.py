# ==========================================================
# FUNCIONES DE WORKER LOCATION
# ==========================================================

from entidades import Candidato
from datos import lista_candidatos


# ==========================================================
# VALIDACIONES Y MANEJO DE ERRORES
# ==========================================================

def solicitar_texto(mensaje):

    while True:

        texto = input(mensaje).strip()

        if texto != "":
            return texto

        print("Error: El campo no puede estar vacío.")


def solicitar_entero(mensaje):

    while True:

        try:

            numero = int(input(mensaje))

            if numero >= 0:
                return numero

            print("Error: El número no puede ser negativo.")

        except ValueError:

            print("Error: Debe ingresar un número entero válido.")


# ==========================================================
# REGISTRAR CANDIDATO
# ==========================================================

def guardar_candidato():

    print("\n--- REGISTRAR NUEVO CANDIDATO ---")

    id_cand = solicitar_entero(
        "Ingrese el ID del candidato: "
    )

    # Comprobar que el ID no esté registrado
    for candidato in lista_candidatos:

        if candidato.id_candidato == id_cand:

            print("Error: Ya existe un candidato con ese ID.")
            return

    nombre = solicitar_texto(
        "Nombre del candidato: "
    )

    profesion = solicitar_texto(
        "Profesión: "
    )

    experiencia = solicitar_entero(
        "Años de experiencia: "
    )

    habilidades = solicitar_texto(
        "Habilidades (separadas por coma): "
    )

    nuevo_candidato = Candidato(
        id_cand,
        nombre,
        profesion,
        experiencia,
        habilidades
    )

    lista_candidatos.append(nuevo_candidato)

    print("\n¡Candidato guardado exitosamente!")


# ==========================================================
# BUSCAR CANDIDATO
# ==========================================================

def buscar_candidato():

    print("\n--- BUSCAR CANDIDATO ---")

    if not lista_candidatos:

        print("No hay candidatos registrados.")
        return

    id_buscar = solicitar_entero(
        "Ingrese el ID del candidato: "
    )

    for candidato in lista_candidatos:

        if candidato.id_candidato == id_buscar:

            print("\n--- CANDIDATO ENCONTRADO ---")

            print("ID:", candidato.id_candidato)
            print("Nombre:", candidato.nombre)
            print("Profesión:", candidato.profesion)
            print("Experiencia:", candidato.experiencia, "años")
            print("Habilidades:", candidato.habilidades)

            return

    print("Candidato no encontrado.")


# ==========================================================
# ACTUALIZAR CANDIDATO
# ==========================================================

def actualizar_candidato():

    print("\n--- ACTUALIZAR CANDIDATO ---")

    if not lista_candidatos:

        print("No hay candidatos registrados.")
        return

    id_actualizar = solicitar_entero(
        "Ingrese el ID del candidato: "
    )

    for candidato in lista_candidatos:

        if candidato.id_candidato == id_actualizar:

            print(
                f"\nActualizando datos de: "
                f"{candidato.nombre}"
            )

            candidato.nombre = solicitar_texto(
                "Nuevo nombre: "
            )

            candidato.profesion = solicitar_texto(
                "Nueva profesión: "
            )

            candidato.experiencia = solicitar_entero(
                "Nuevos años de experiencia: "
            )

            candidato.habilidades = solicitar_texto(
                "Nuevas habilidades: "
            )

            print(
                "\n¡Candidato actualizado exitosamente!"
            )

            return

    print("Candidato no encontrado.")


# ==========================================================
# ELIMINAR CANDIDATO
# ==========================================================

def eliminar_candidato():

    print("\n--- ELIMINAR CANDIDATO ---")

    if not lista_candidatos:

        print("No hay candidatos registrados.")
        return

    id_eliminar = solicitar_entero(
        "Ingrese el ID del candidato: "
    )

    for i, candidato in enumerate(lista_candidatos):

        if candidato.id_candidato == id_eliminar:

            eliminado = lista_candidatos.pop(i)

            print(
                f"El candidato {eliminado.nombre} "
                f"ha sido eliminado."
            )

            return

    print("Candidato no encontrado.")


# ==========================================================
# CONTAR CANDIDATOS
# ==========================================================

def contar_candidatos():

    total = len(lista_candidatos)

    print("\n--- TOTAL DE CANDIDATOS ---")

    print(
        f"Actualmente hay {total} "
        f"candidato(s) registrado(s) en el sistema."
    )


# ==========================================================
# BUSCAR CANDIDATOS SEGÚN REQUISITOS
# ==========================================================

def buscar_por_requisitos():

    print("\n===================================")
    print(" BUSCAR CANDIDATO PARA UNA VACANTE ")
    print("===================================")

    if not lista_candidatos:

        print("No hay candidatos registrados.")
        return

    profesion_requerida = solicitar_texto(
        "Profesión requerida: "
    )

    experiencia_minima = solicitar_entero(
        "Experiencia mínima requerida: "
    )

    habilidades_requeridas = solicitar_texto(
        "Habilidades requeridas (separadas por coma): "
    )

    # Convertir las habilidades requeridas
    # en una lista y convertirlas a minúsculas.
    habilidades_requeridas = [
        habilidad.strip().lower()
        for habilidad in habilidades_requeridas.split(",")
    ]

    resultados = []

    # Revisar todos los candidatos registrados
    for candidato in lista_candidatos:

        puntos = 0

        # ------------------------------------------
        # COMPARAR PROFESIÓN
        # ------------------------------------------

        if candidato.profesion.lower() == profesion_requerida.lower():

            puntos += 50

        # ------------------------------------------
        # COMPARAR EXPERIENCIA
        # ------------------------------------------

        if candidato.experiencia >= experiencia_minima:

            puntos += 30

        # ------------------------------------------
        # COMPARAR HABILIDADES
        # ------------------------------------------

        habilidades_candidato = [
            habilidad.strip().lower()
            for habilidad in candidato.habilidades.split(",")
        ]

        coincidencias = 0

        for habilidad in habilidades_requeridas:

            if habilidad in habilidades_candidato:

                coincidencias += 1

        puntos += coincidencias * 10

        # Guardar solamente candidatos
        # que tengan alguna coincidencia.
        if puntos > 0:

            resultados.append(
                (puntos, candidato)
            )

    # Ordenar los resultados de mayor
    # a menor cantidad de puntos.
    resultados.sort(
        key=lambda resultado: resultado[0],
        reverse=True
    )

    if not resultados:

        print(
            "\nNo se encontraron "
            "candidatos compatibles."
        )

        return

    print("\n========== RESULTADOS ==========")

    for puntos, candidato in resultados:

        print("\nCandidato:", candidato.nombre)
        print("Profesión:", candidato.profesion)
        print(
            "Experiencia:",
            candidato.experiencia,
            "años"
        )
        print("Habilidades:", candidato.habilidades)
        print("Coincidencia:", puntos, "puntos")