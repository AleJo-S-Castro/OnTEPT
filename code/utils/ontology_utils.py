# -*- coding: utf-8 -*-
"""
ontology_utils.py — Utilidades compartidas para manejar la ontología OnTEPT.
Todos los módulos de población importan desde aquí para garantizar consistencia.
"""
import os, shutil
from owlready2 import get_ontology, onto_path

NS = "http://www.semanticweb.org/alejo/ontologies/2025/0/OnTEPT#"


def cargar_ontologia(ruta: str):
    """Carga la ontología desde un archivo RDF/XML."""
    directorio = os.path.dirname(os.path.abspath(ruta))
    if directorio not in onto_path:
        onto_path.append(directorio)
    return get_ontology(os.path.abspath(ruta)).load()


def guardar_ontologia(onto, ruta_salida: str, backup: bool = True):
    """Guarda la ontología; opcionalmente crea un _backup.rdf."""
    if backup and os.path.exists(ruta_salida):
        bk = ruta_salida.replace(".rdf", "_backup.rdf")
        shutil.copy2(ruta_salida, bk)
        print(f"  [✔] Backup: {bk}")
    onto.save(file=ruta_salida, format="rdfxml")
    print(f"  [✔] Guardada: {ruta_salida}")


def crear_evento(onto, nombre: str, traumatico: bool):
    """Crea un TraumaticEvent o NonTraumaticEvent y asigna TraumaticEventProperty."""
    cls = onto.TraumaticEvent if traumatico else onto.NonTraumaticEvent
    ev  = cls(nombre)
    onto.TraumaticEventProperty[ev] = [traumatico]
    return ev


def crear_sintoma(onto, clase: str, nombre: str,
                  dur=None, cs=None, atr=None, onset=None):
    """Crea un síntoma con las data properties indicadas."""
    s = getattr(onto, clase)(nombre)
    if dur   is not None: onto.duration[s]                         = [dur]
    if cs    is not None: onto.disturbanceClinicallySignificant[s] = [cs]
    if atr   is not None: onto.attributableEffectsSubstance[s]     = [atr]
    if onset is not None: onto.onsetDelayInMonths[s]               = [onset]
    return s


def ejecutar_sparql(ruta_onto: str, query: str) -> list:
    """Ejecuta una consulta SPARQL con rdflib (sin razonador)."""
    try:
        from rdflib import Graph
        g = Graph()
        g.parse(ruta_onto, format="xml")
        return list(g.query(query))
    except ImportError:
        print("  [!] rdflib no instalado. pip install rdflib")
        return []
