# Ontología OnTEPT — Versión actual

Este directorio contiene la versión estable y pública de OnTEPT.

## Archivo

| Archivo | Versión | Descripción |
|---|---|---|
| `onTEPT_v1.0.rdf` | 1.0 | Versión pública inicial. OWL 2 DL, RDF/XML. |

## Cómo usar este archivo

**En Protégé:**
1. `File → Open → onTEPT_v1.0.rdf`
2. `Reasoner → Fact++ → Start Reasoner`

**En Python (owlready2):**
```python
from owlready2 import *
onto = get_ontology("ruta/a/onTEPT_v1.0.rdf").load()
```

**En Python (rdflib):**
```python
from rdflib import Graph
g = Graph()
g.parse("ruta/a/onTEPT_v1.0.rdf", format="xml")
```

## IRI base

```
http://www.semanticweb.org/alejo/ontologies/2025/0/OnTEPT
```

## Estadísticas (v1.0)

| Métrica | Valor |
|---|---|
| Clases | 111 |
| Propiedades de objeto | 16 |
| Propiedades de datos | 65+ |
| Propiedades de anotación | 1 (`evaluatesSymptomCluster`) |
| Axiomas de equivalencia (clases de paciente) | 22 |
| Triples RDF totales | ~2454 |
