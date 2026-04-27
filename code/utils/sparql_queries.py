# -*- coding: utf-8 -*-
"""
sparql_queries.py — Consultas SPARQL predefinidas para OnTEPT.
Importar y usar con ontology_utils.ejecutar_sparql().
"""
NS = "http://www.semanticweb.org/alejo/ontologies/2025/0/OnTEPT#"
PFX = f"PREFIX : <{NS}>\n"

# Consultas estructurales (sin razonador)
PACIENTES_CON_TRAUMA = PFX + """
SELECT DISTINCT ?p WHERE {
    ?p a :Patient . ?p :hasEvent ?ev . ?ev :TraumaticEventProperty true .
} ORDER BY ?p"""

PACIENTES_CON_INTRUSION = PFX + """
SELECT DISTINCT ?p WHERE {
    ?p a :Patient . ?p :hasSymptom ?s . ?s a :IntrusionSymptom .
} ORDER BY ?p"""

ONSET_DEMORADO = PFX + """
SELECT ?p ?s ?meses WHERE {
    ?p a :Patient . ?p :hasSymptom ?s . ?s :onsetDelayInMonths ?meses .
} ORDER BY ?p"""

MAPEO_ITEMS_CRITERIOS = PFX + """
SELECT ?item ?criterio WHERE {
    ?item :evaluatesSymptomCluster ?criterio .
} ORDER BY ?item"""

# Consultas diagnósticas (requieren razonador en Protégé)
TEPT_DSM5       = PFX + "SELECT ?p WHERE { ?p a :Patient_meetsPTSD_DSM5 . }"
TEPT_ICD11      = PFX + "SELECT ?p WHERE { ?p a :Patient_meetsPTSD_ICD11 . }"
TEPT_DISOCIATIVO= PFX + "SELECT ?p WHERE { ?p a :Patient_meetsPTSD_WithDissociative_DSM5 . }"
TEPT_COMPLEJO   = PFX + "SELECT ?p WHERE { ?p a :Patient_meetsPTSD_Complex_ICD11 . }"
TEPT_PROBABLE   = PFX + "SELECT ?p WHERE { ?p a :Patient_probablyMeets_PTSD_byAssesmentInstrument . }"

INTEROP_ICD11_NO_DSM5 = PFX + """
SELECT DISTINCT ?p WHERE {
    ?p a :Patient_meetsPTSD_ICD11 .
    FILTER NOT EXISTS { ?p a :Patient_meetsPTSD_DSM5 . }
    FILTER NOT EXISTS { ?p a :Patient_meetsPTSD_WithDissociative_DSM5 . }
}"""
