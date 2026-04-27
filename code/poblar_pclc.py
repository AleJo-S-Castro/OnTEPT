# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 21:14:26 2025

@author: AleJo
"""

import pandas as pd
from utils_onTEPT import cargar_ontologia, obtener_o_crear_paciente, poblar_instancia_cuestionario

def poblar_pclc(ruta_ontologia, archivo_ontologia):
    archivo_csv = ruta_ontologia + "\\datos\\detailed_lables.csv"
    df = pd.read_csv(archivo_csv)

    onto = cargar_ontologia(ruta_ontologia, archivo_ontologia)
    print("Número de individuos antes de poblar con datos PCL-C:", len(list(onto.individuals())))   
    
    Patient = onto["Patient"]
    PCL_C = onto["PTSD_Checklist_PCL-C"]

    item_names = ["Memories", "Dreams", "Reliving", "Upset", "Physical", "ThoughtAvoidance",
                  "ActivityAvoidance", "TroubleRemembering", "NoInterest", "FeelDistant",
                  "FeelNumb", "Future_Cut_Short", "Sleep", "Irritability", "Concentration",
                  "HyperAlert", "Jumpy"]

    item_cols = [f"PCL-C_{i}_{name}" for i, name in enumerate(item_names, start=1)]
    total_col = "PTSD_severity"

    for _, row in df.iterrows():
        participante = str(row["Participant"]).strip()
        paciente = obtener_o_crear_paciente(onto, Patient, "P"+participante)
        poblar_instancia_cuestionario(onto, paciente, PCL_C, item_cols, total_col, row,
                                      "PCL-C_", "PCL_Item", "PCL_totalScore", dataset_id="DS5", id_col="Participant")
    
    print("Número de individuos después de poblar con datos PCL-C:", len(list(onto.individuals())))
    onto.save(file=archivo_ontologia.replace(".rdf", ".rdf"), format="rdfxml")
    #onto.save(file=archivo_ontologia.replace(".rdf", "_Solo_PCL_C.rdf"), format="rdfxml")
    print("Ontología poblada con datos de PCL-C.")
