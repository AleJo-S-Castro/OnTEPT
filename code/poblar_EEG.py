# -*- coding: utf-8 -*-
"""
Módulo para poblar la ontología onTEPT con datos EEG y sus bandas de frecuencia.
Encapsula la lógica de PoblarOnTEPT_EEG.py para integrarse con el menú principal.

@author: AleJo
"""

import os
import pandas as pd
from owlready2 import onto_path, get_ontology


# Funciones auxiliares

def _cargar_ontologia(ruta_ontologia: str, archivo: str):
    """Carga la ontología desde la ruta indicada."""
    if ruta_ontologia not in onto_path:
        onto_path.append(ruta_ontologia)
    return get_ontology(os.path.join(ruta_ontologia, archivo)).load()


def _obtener_o_crear_paciente(onto, Patient, participant_id, dataset_id="DS3"):
    """Busca el individuo Paciente; si no existe, lo crea."""
    nombre_paciente = f"Patient_{int(participant_id):02d}_{dataset_id}"
    paciente_inst = onto.search_one(iri="*" + nombre_paciente)
    return paciente_inst if paciente_inst else Patient(nombre_paciente)


def _obtener_o_crear_segmento(onto, EEG_segment, nombre_segmento):
    """Busca el individuo EEG_segment; si no existe, lo crea."""
    segmento_inst = onto.search_one(iri="*" + nombre_segmento)
    return segmento_inst if segmento_inst else EEG_segment(nombre_segmento)


def _relacionar_hasEEGRecording(paciente, instancia, hasEEGRecording):
    """Relaciona un segmento EEG con su paciente mediante hasEEGRecording."""
    if instancia not in getattr(paciente, hasEEGRecording.name):
        getattr(paciente, hasEEGRecording.name).append(instancia)


def _poblar_segmentos(df, onto, dataset_id, rhythm=None):
    """
    Crea individuos EEG_segment y asigna propiedades y relaciones.
    """

    Patient = getattr(onto, "Patient")
    EEG_segment = getattr(onto, "EEG_segment")
    hasEEGRecording = getattr(onto, "hasEEGRecording")

    # Validación de columnas esperadas
    columnas_requeridas = ["paciente", "canal", "segmento"]
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"Falta la columna requerida: {col}")

    # Clase de ritmo
    rhythm_class = None
    if rhythm:
        class_name = f"{rhythm}_EEG_rhythm"
        if hasattr(onto, class_name):
            rhythm_class = getattr(onto, class_name)
        else:
            print(f"Advertencia: la clase '{class_name}' no existe en la ontología.")

    # Propiedades de datos disponibles
    data_properties = {prop.name: prop for prop in onto.data_properties()}

    # Mapeo dataset → ontología
    mapeo = {
        "areaBajoLaCurva": "areaUnderCurve",
        "media": "mean",
        "raizCuadradaMedia": "rootMeanSquare",
        "varianza": "variance",
        "desviacionEstandar": "standardDeviation",
        "entropiaEnergiaLogaritmica": "logEnergyEntropy",
        "integralCuadrada": "squaredIntegral",
        "curtosis": "kurtosis",
        "covarianza": "covariance",
        "entropiaShannon": "shannonEntropy",
        "cambioMedioAmplitud": "meanAmplitudeChange",
        "raizSumaCuadradosRSSQ": "RSSQ",
        "integralCuadradaSimpleSSI": "SSI",
        "potenciaSSI2": "SSI2Power",
        "varianzaEEG": "eegVariance",
        "indiceAsimetriaDecay": "asymmetryIndexDecay",
        "numeroPicosCorrelacion": "correlationPeakCount",
        "energia1_3Correlacion": "correlationEnergy13",
        "energia2_3Correlacion": "correlationEnergy23",
        "cocienteIntegral": "integralRatio",
        "curtosisEnvolvente": "envelopeKurtosis",
        "curtosisSenal": "signalKurtosis",
        "maximoFFT": "fftMaximum",
        "mediaFFT": "fftMean",
        "medianaFFT": "fftMedian",
        "cocienteMaximoMedia": "maxToMeanRatio",
        "cocienteMaximoMediana": "maxToMedianRatio",
        "varianzaFFT": "fftVariance",
        "mediana": "median",
        "entropiaHistograma": "histogramEntropy",
        "asimetriaEnvolvente": "envelopeAsymmetry",
        "asimetriaSenal": "signalAsymmetry",
        "frecuenciaMaximaFFT": "fftPeakFrequency",
        "maximoP1": "P1Maximum",
        "mediaP1": "P1Mean",
        "potenciaP1": "P1Power",
    }

    for _, row in df.iterrows():

        participant_id = row["paciente"]
        canal = str(row["canal"]).strip()
        segmento_id = int(row["segmento"])

        # Paciente
        paciente = _obtener_o_crear_paciente(onto, Patient, participant_id, dataset_id)

        # Nombre del segmento
        if rhythm:
            nombre_segmento = (
                f"EEG_Rhythm{rhythm}_Chn{canal}_Segment_{segmento_id:03d}"
                f"_Pat{int(participant_id):02d}_{dataset_id}"
            )
        else:
            nombre_segmento = (
                f"EEG_Chn{canal}_Segment_{segmento_id:03d}"
                f"_Pat{int(participant_id):02d}_{dataset_id}"
            )

        # Crear/obtener individuo
        segmento_inst = _obtener_o_crear_segmento(onto, EEG_segment, nombre_segmento)

        # Relación paciente-segmento
        _relacionar_hasEEGRecording(paciente, segmento_inst, hasEEGRecording)

        # Clase de ritmo
        if rhythm_class and rhythm_class not in segmento_inst.is_a:
            segmento_inst.is_a.append(rhythm_class)

        # Propiedades base (ontología en inglés)
        if "channel" in data_properties:
            segmento_inst.channel = [canal]
        if "segment" in data_properties:
            segmento_inst.segment = [str(segmento_id)]
        if rhythm and "rhythm" in data_properties:
            segmento_inst.rhythm = [rhythm]

        # Features
        for col_df in df.columns:
            base_col = col_df.replace(rhythm, "") if rhythm else col_df
            if base_col in mapeo:
                prop_name = mapeo[base_col]
                if prop_name in data_properties:
                    valor = row[col_df]
                    if pd.notna(valor):

                        val = float(valor)

                        try:
                            getattr(segmento_inst, prop_name).append(val)
                        except AttributeError:
                            setattr(segmento_inst, prop_name, val)


# Función principal

def poblar_EEG(ruta_ontologia: str, nombre_ontologia: str,
               ruta_datos: str = None, dataset_id: str = "DS3") -> None:

    # Ruta de datos
    if ruta_datos is None:
        ruta_datos = input("Ingrese la ruta de los archivos EEG: ").strip()

    if not os.path.isdir(ruta_datos):
        raise ValueError(f"La ruta no existe: {ruta_datos}")

    # Archivos HDF5
    archivos = {
        "EEG": "df20s_EEG_Feats.h5",
        "D4": "df20s_bandaD4_Feats.h5",
        "A4": "df20s_bandaA4_Feats.h5",
        "D3": "df20s_bandaD3_Feats.h5",
        "D2": "df20s_bandaD2_Feats.h5",
        "D1": "df20s_bandaD1_Feats.h5",
    }

    dfs = {}
    for clave, archivo in archivos.items():
        ruta_archivo = os.path.join(ruta_datos, archivo)

        if not os.path.isfile(ruta_archivo):
            raise FileNotFoundError(f"No se encontró: {ruta_archivo}")

        print(f"Cargando {archivo} ...")
        dfs[clave] = pd.read_hdf(ruta_archivo, key="dataset")

    # Cargar ontología
    print(f"\nCargando ontología '{nombre_ontologia}' ...")
    onto = _cargar_ontologia(ruta_ontologia, nombre_ontologia)

    # Poblar EEG general
    print("Poblando segmentos EEG generales ...")
    _poblar_segmentos(dfs["EEG"], onto, dataset_id=dataset_id)

    # Poblar bandas
    for banda in ["D1", "D2", "D3", "D4", "A4"]:
        print(f"Poblando banda {banda} ...")
        _poblar_segmentos(dfs[banda], onto, dataset_id=dataset_id, rhythm=banda)

    # Guardar ontología
    nombre_copia = nombre_ontologia.replace(".rdf", "-EEG+Bands.rdf")
    ruta_salida = os.path.join(ruta_ontologia, nombre_copia)

    onto.save(file=ruta_salida, format="rdfxml")
    print(f"\nOntología guardada en: {ruta_salida}")