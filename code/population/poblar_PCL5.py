# -*- coding: utf-8 -*-
"""
poblar_PCL5.py
==============
Pobla la ontología OnTEPT con datos del PCL-5
(PTSD Checklist for DSM-5, 20 ítems, escala 0-4, umbral ≥31).

Formato del CSV de entrada:
    patient_id, item_1, item_2, ..., item_20, total_score
    P001, 2, 3, 1, 0, 2, 3, 1, 0, 2, 1, 3, 2, 1, 0, 2, 3, 1, 0, 2, 3, 36

Uso:
    from population.poblar_PCL5 import poblar_desde_PCL5
    poblar_desde_PCL5("ontologia.rdf", "datos_pcl5.csv", "salida.rdf")
"""
import os, sys
import pandas as pd
from owlready2 import *

# Umbral PCL-5 para TEPT probable (Weathers et al., 2013)
UMBRAL_PCL5 = 31

# Mapeo ítem PCL-5 → nombre de la data property en la ontología
PROP_ITEMS = {i: f"PCL_Item{i}" for i in range(1, 21)}


def poblar_desde_PCL5(ruta_onto: str, ruta_datos: str, ruta_salida: str):
    """
    Carga el CSV de PCL-5, crea instancias en la ontología y guarda el resultado.

    Parámetros
    ----------
    ruta_onto   : ruta al archivo .rdf de la ontología base
    ruta_datos  : ruta al CSV con los datos PCL-5
    ruta_salida : ruta donde guardar la ontología poblada
    """
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from utils.ontology_utils import cargar_ontologia, guardar_ontologia
    from utils.validators import validar_fila_pcl5

    onto = cargar_ontologia(ruta_onto)
    df   = pd.read_csv(ruta_datos)
    print(f"  Datos cargados: {len(df)} filas")

    n_ok = n_err = 0
    with onto:
        for _, fila in df.iterrows():
            pid  = str(fila.get("patient_id", f"P{_}"))
            valida, errores = validar_fila_pcl5(fila.to_dict())
            if not valida:
                print(f"  [!] {pid} — errores: {errores}")
                n_err += 1
                continue

            # Crear instrumento PCL-5
            pcl = onto.PTSD_Checklist_PCL5(f"PCL5_{pid}")
            for i, prop_nombre in PROP_ITEMS.items():
                prop = getattr(onto, prop_nombre)
                prop[pcl] = [int(fila.get(f"item_{i}", 0))]
            total = int(fila.get("total_score",
                                 sum(int(fila.get(f"item_{i}", 0)) for i in range(1, 21))))
            onto.PCL_totalScore[pcl] = [total]

            # Crear paciente y vincularlo al instrumento
            p = onto.Patient(f"Patient_PCL5_{pid}")
            onto.isAssessedBy[p].append(pcl)
            n_ok += 1

    guardar_ontologia(onto, ruta_salida)
    print(f"  Poblados: {n_ok} pacientes. Errores: {n_err}.")
    print(f"  Nota: ejecutar el razonador (Fact++) en Protégé para inferir "
          f"Patient_probablyMeets_PTSD_byAssesmentInstrument.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python poblar_PCL5.py <ontologia.rdf> <datos.csv> <salida.rdf>")
        sys.exit(1)
    poblar_desde_PCL5(sys.argv[1], sys.argv[2], sys.argv[3])
