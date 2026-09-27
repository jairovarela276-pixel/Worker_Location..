# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

import funciones


def mostrar_menu():

    print("\n")
    print("===================================")
    print("         WORKER LOCATION")
    print("===================================")

    print("1. Registrar candidato")
    print("2. Buscar candidato")
    print("3. Actualizar candidato")
    print("4. Eliminar candidato")
    print("5. Mostrar total de candidatos")
    print("6. Buscar candidato para una vacante")
    print("7. Salir")


def main():

    while True:

        mostrar_menu()

        opcion = funciones.solicitar_entero(
            "Seleccione una opción: "
        )

        if opcion == 1:

            funciones.guardar_candidato()

        elif opcion == 2:

            funciones.buscar_candidato()

        elif opcion == 3:

            funciones.actualizar_candidato()

        elif opcion == 4:

            funciones.eliminar_candidato()

        elif opcion == 5:

            funciones.contar_candidatos()

        elif opcion == 6:

            funciones.buscar_por_requisitos()

        elif opcion == 7:

            print(
                "\nSaliendo del sistema "
                "Worker Location. ¡Hasta pronto!"
            )

            break

        else:

            print(
                "\nOpción inválida. "
                "Seleccione un número del 1 al 7."
            )


if __name__ == "__main__":

    main()