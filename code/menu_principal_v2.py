# -*- coding: utf-8 -*-
"""
menu_principal_v2.py
Versión 2 del menú principal para poblar la ontología onTEPT.

Cambios respecto a v1:
- La ruta y el nombre de la ontología se obtienen mediante un cuadro de
  diálogo gráfico (tkinter) al iniciar el programa, en lugar de estar
  definidos de forma fija en el código.

@author: AleJo
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox

from poblar_pcl5 import poblar_pcl5
from poblar_pclc import poblar_pclc
from poblar_pcptsd5 import poblar_pcptsd5
from poblar_EEG import poblar_EEG
# from poblar_sinteticos import poblar_sinteticos
# from poblar_sinteticos_ext import poblar_sinteticos_ext
from poblar_sinteticos_ext_v2 import poblar_sinteticos_ext_v2
from utils_onTEPT import cargar_ontologia, limpiar_ontologia


def seleccionar_ontologia():
    """
    Abre una ventana de diálogo para que el usuario seleccione el archivo
    RDF de la ontología.

    Devuelve
    --------
    tuple[str, str]
        (ruta, nombre) donde 'ruta' es el directorio y 'nombre' es el nombre
        del archivo incluyendo la extensión.
        Devuelve (None, None) si el usuario cancela la selección.
    """
    root = tk.Tk()
    root.withdraw()          # Ocultar la ventana principal de tkinter
    root.attributes("-topmost", True)

    ruta_completa = filedialog.askopenfilename(
        title="Seleccione el archivo de la ontología onTEPT",
        filetypes=[
            ("Archivos RDF", "*.rdf"),
            ("Todos los archivos", "*.*"),
        ],
    )

    root.destroy()

    if not ruta_completa:
        return None, None

    ruta   = os.path.dirname(ruta_completa)
    nombre = os.path.basename(ruta_completa)
    return ruta, nombre


def main():
    # ------------------------------------------------------------------
    # Selección del archivo de ontología mediante cuadro de diálogo
    # ------------------------------------------------------------------
    print("Abriendo cuadro de diálogo para seleccionar la ontología...")
    ruta, nombre = seleccionar_ontologia()

    if ruta is None:
        print("No se seleccionó ningún archivo. El programa se cerrará.")
        return

    print(f"Ontología seleccionada: {os.path.join(ruta, nombre)}")

    # ------------------------------------------------------------------
    # Carga inicial de la ontología y copia de seguridad sin individuos
    # ------------------------------------------------------------------
    onto = cargar_ontologia(ruta, nombre)
    ruta_guardado = os.path.join(ruta, nombre)
    onto.save(
        file=ruta_guardado.replace(".rdf", "_copiaSinIndividuos.rdf"),
        format="rdfxml",
    )

    # ------------------------------------------------------------------
    # Bucle del menú principal
    # ------------------------------------------------------------------

    ruta_datos = r"H:\Mi unidad\Doctorado\Desarrollo\codes\pythonEEG\EEG_DS3\Codigos Final\datasetsAjustados"

    while True:
        print("\n=== Menu Principal ===")
        print(f"Ontología activa: {nombre}")
        print("1. Poblar ontología solo con PCL-5")
        print("2. Poblar ontología solo con PCL-C")
        print("3. Poblar ontología solo con PC-PTSD-5")
        print("4. Poblar ontología solo con datos EEG")
        print("5. Poblar ontología solo con datos sintéticos")
        print("6. Poblar ontología con datos sintéticos, PCLs y PC-PTSD")
        print("7. Limpiar todos los individuos de la ontología")
        print("8. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            poblar_pcl5(ruta, nombre)

        elif opcion == "2":
            poblar_pclc(ruta, nombre)

        elif opcion == "3":
            poblar_pcptsd5(ruta, nombre)

        elif opcion == "4":
            poblar_EEG(ruta, nombre, ruta_datos)

        elif opcion == "5":
            poblar_sinteticos_ext_v2(ruta, nombre)

        elif opcion == "6":
            poblar_pcl5(ruta, nombre)
            poblar_pclc(ruta, nombre)
            poblar_pcptsd5(ruta, nombre)
            poblar_EEG(ruta, nombre)
            poblar_sinteticos_ext_v2(ruta, nombre)

        elif opcion == "7":
            confirmacion = input(
                "Esta seguro que desea eliminar todos los individuos? (s/n): "
            ).lower()

            if confirmacion in ("s", "S"):
                onto.save(
                    file=ruta_guardado.replace(".rdf", "-backup.rdf"),
                    format="rdfxml",
                )
                limpiar_ontologia(ruta, nombre)

        elif opcion == "8":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
