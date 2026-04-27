# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 21:14:26 2025

@author: AleJo
"""

import pandas as pd
from utils_onTEPT import cargar_ontologia, obtener_o_crear_paciente, poblar_instancia_cuestionario

def poblar_pcptsd5(ruta_ontologia, archivo_ontologia):
    archivo_excel = ruta_ontologia + "\\datos\\Scores_Modificados.xlsx"
    df = pd.read_excel(archivo_excel)

    onto = cargar_ontologia(ruta_ontologia, archivo_ontologia)
    print("Número de individuos antes de poblar con datos PC-PTSD:", len(list(onto.individuals())))   
    
    Patient = onto["Patient"]
    PC_PTSD = onto["PrimaryCarePTSD_Screen_PC-PTSD-5"]

    item_cols = [f"Pre-PC_PTSD-{i}" for i in range(1, 6)]
    total_col = "TOTAL_Pre_PC_PTSD"

    for _, row in df.iterrows():
        participante = str(row["Participants"]).strip()
        paciente = obtener_o_crear_paciente(onto, Patient, participante)
        poblar_instancia_cuestionario(onto, paciente, PC_PTSD, item_cols, total_col, row,
                                      "PC-PTSD_", "PC-PTSD_Item", "PC-PTSD_ItemtotalScore", dataset_id="DS1")

    print("Número de individuos después de poblar con datos PC-PTSD:", len(list(onto.individuals())))
    onto.save(file=archivo_ontologia.replace(".rdf", ".rdf"), format="rdfxml")
    #onto.save(file=archivo_ontologia.replace(".rdf", "_Solo_PC_PTSD.rdf"), format="rdfxml")
    print("Ontología poblada con datos de PC-PTSD-5.")
