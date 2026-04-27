# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 21:14:26 2025

@author: AleJo
"""

import pandas as pd
from utils_onTEPT import cargar_ontologia, obtener_o_crear_paciente, poblar_instancia_cuestionario

def poblar_pcl5(ruta_ontologia, archivo_ontologia):
    archivo_excel = ruta_ontologia + "\\datos\\Scores_Modificados.xlsx"
    df = pd.read_excel(archivo_excel)
    
    onto = cargar_ontologia(ruta_ontologia, archivo_ontologia)
    print("Número de individuos antes de poblar con datos PCL-5:", len(list(onto.individuals())))   
    
    Patient = onto["Patient"]
    PCL_5 = onto["PTSD_Checklist_PCL5"]

    item_cols = [f"Pre-PCL5-{i}" for i in range(1, 21)]
    total_col = "TOTAL_Pre_PCL5"

    for _, row in df.iterrows():
        participante = str(row["Participants"]).strip()
        paciente = obtener_o_crear_paciente(onto, Patient, participante)
        poblar_instancia_cuestionario(onto, paciente, PCL_5, item_cols, total_col, row,
                                      "PCL-5_", "PCL_Item", "PCL_totalScore", dataset_id="DS1")
    
    print("Número de individuos después de poblar con datos PCL-5:", len(list(onto.individuals())))
    onto.save(file=archivo_ontologia.replace(".rdf", ".rdf"), format="rdfxml")
    #onto.save(file=archivo_ontologia.replace(".rdf", "_Solo_PCL_5.rdf"), format="rdfxml")
    print("Ontología poblada con datos de PCL-5.")
