# Guía técnica — OnTEPT v1.0

Esta guía describe el diseño técnico de OnTEPT para investigadores que necesiten extender la ontología, alinearla con otros recursos externos o integrarla en pipelines de análisis clínico.

---

## Perfil OWL y razonamiento

OnTEPT se ajusta al perfil **OWL 2 DL**, que garantiza decidibilidad del razonamiento. El conjunto de constructores empleados se resume a continuación:

| Constructor | Uso en OnTEPT |
|---|---|
| `owl:equivalentClass` con `owl:intersectionOf` | Definición de clases diagnósticas compuestas (p. ej., `Patient_meetsPTSD_DSM5`) |
| `owl:minQualifiedCardinality` | Criterios D (≥2 `AffectiveCognitiveAlteration`) y E (≥2 `ThreatArousalSymptom`) |
| `owl:hasValue` | Restricciones booleanas en criterios G y H |
| `owl:someValuesFrom` + `rdfs:Datatype` / `xsd:minInclusive` | Umbrales de duración (Criterio F) y puntuación psicométrica |
| `owl:complementOf` | Exclusión del subtipo disociativo de la clase TEPT clásico DSM-5 |
| `owl:disjointWith` y `owl:AllDisjointClasses` | Exclusión mutua entre subtipos diagnósticos y entre tipos de síntomas |
| `rdfs:subClassOf` | Interoperabilidad formal DSM-5 → CIE-11 |

El razonamiento es de **mundo cerrado** en el nivel ABox: la ausencia de una propiedad requerida se interpreta como no satisfacción del criterio. Esto es clínicamente apropiado para la clasificación diagnóstica, pero exige que los datos del paciente estén completos para que la inferencia sea correcta.

---

## IRI base y prefijos

```
IRI base: http://www.semanticweb.org/alejo/ontologies/2025/0/OnTEPT
Prefijo:  :  (o onTEPT:)
```

Para consultas SPARQL, usar siempre el prefijo completo:

```sparql
PREFIX : <http://www.semanticweb.org/alejo/ontologies/2025/0/OnTEPT#>
```

Para alineamientos externos se pueden añadir axiomas `owl:sameAs` o `skos:exactMatch`. Las referencias MESH existentes están en `rdfs:comment`; para un alineamiento formal, añadirlas como:

```turtle
:IntrusionSymptom skos:exactMatch <http://purl.bioontology.org/ontology/MESH/D000xxxxx> .
```

---

## Axiomas de equivalencia diagnóstica

### Patient_meetsPTSD_DSM5 (Manchester OWL)

```manchester
Patient
  and Patient_meetsDSM5_A
  and Patient_meetsDSM5_B
  and Patient_meetsDSM5_C
  and Patient_meetsDSM5_D
  and Patient_meetsDSM5_E
  and Patient_meetsDSM5_F
  and Patient_meetsDSM5_G
  and Patient_meetsDSM5_H
  and (not Patient_meetsDSM5_XDissociative)
```

Donde, por ejemplo, `Patient_meetsDSM5_D` se define como:

```manchester
hasSymptom min 2 AffectiveCognitiveAlteration
```

Y `Patient_meetsDSM5_F` como:

```manchester
hasSymptom some (IntrusionSymptom and duration some integer[>=1])
and hasSymptom some (AvoidanceSymptom and duration some integer[>=1])
and hasSymptom some (ThreatArousalSymptom and duration some integer[>=1])
```

### Patient_meetsPTSD_ICD11

```manchester
Patient
  and Patient_meetsICD11_1
  and Patient_meetsICD11_2
  and Patient_meetsICD11_3
  and Patient_meetsICD11_4
  and Patient_meetsICD11_5
  and Patient_meetsICD11_6
  and (not Patient_meetsICD11_XComplex)
```

### Interoperabilidad formal (v1.0)

```manchester
Patient_meetsPTSD_DSM5 SubClassOf Patient_meetsPTSD_ICD11
```

Este axioma axiomatiza la subsunción entre sistemas: todo paciente que satisface A–H del DSM-5 satisface también los Criterios 1–6 de la CIE-11. La relación inversa no se axiomatiza porque la CIE-11 no exige el Criterio D (alteraciones cognitivas y del ánimo).

---

## Propiedad de anotación `evaluatesSymptomCluster`

Esta propiedad de anotación OWL resuelve la brecha instrumental descrita en la literatura: los mapeos ítem–criterio de los instrumentos psicométricos se hacen explícitos y consultables sin comprometer la decidibilidad del perfil OWL 2 DL.

**Definición:**
```turtle
:evaluatesSymptomCluster a owl:AnnotationProperty ;
    rdfs:label "evaluates_symptom_cluster"@en ;
    rdfs:label "evalua_cluster_sintomatico"@es .
```

**Uso:**
```turtle
:PCL_Item1   :evaluatesSymptomCluster  :DSM5_CriterionB1:IntrusiveMemories .
:PCL_Item6   :evaluatesSymptomCluster  :DSM5_CriterionC1:AvoidanceOfThoughts .
:CAPS_Item8  :evaluatesSymptomCluster  :DSM5_CriterionD1:MemoryImpairment .
:CAPS_Item17 :evaluatesSymptomCluster  :DSM5_CriterionE3:Hypervigilance .
```

**Consulta SPARQL para recuperar el mapeo completo:**
```sparql
PREFIX : <http://www.semanticweb.org/alejo/ontologies/2025/0/OnTEPT#>
SELECT ?item ?criterio WHERE {
    ?item :evaluatesSymptomCluster ?criterio .
} ORDER BY ?item
```

---

## Extensión de la ontología

### Añadir una nueva clase de síntoma

```turtle
:MiNuevoSintoma a owl:Class ;
    rdfs:subClassOf :IntrusionSymptom ;
    rdfs:label "my new symptom"@en ;
    rdfs:label "mi nuevo síntoma"@es ;
    rdfs:comment "Description."@en ;
    rdfs:comment "Descripción."@es .
```

Verificar consistencia con Fact++ antes de hacer commit.

### Añadir un nuevo instrumento psicométrico

1. Crear subclase de `Self-ReportInstrument`, `ScreeningInstrument` o `ClinicianAdministeredInstrument`.
2. Añadir propiedades de datos funcionales como subpropiedades de la propiedad padre del instrumento.
3. Añadir anotaciones `evaluatesSymptomCluster` en cada propiedad de ítem.
4. Si el instrumento tiene un umbral diagnóstico, actualizar la equivalencia de `Patient_probablyMeets_PTSD_byAssesmentInstrument` añadiendo una nueva rama `isAssessedBy some (ClaseInstrumento and propPuntuacion some integer[>=umbral])`.

### Añadir un criterio diagnóstico nuevo

1. Crear la clase del criterio como subclase de `PTSD_DSM_5_DiagnosticCriterion` o `PTSD_ICD_11_DiagnosticCriterion`.
2. Crear la clase `Patient_meetsXXX_CriterioNuevo` con el axioma de equivalencia correspondiente.
3. Si el criterio es obligatorio para el diagnóstico completo, actualizar la intersección de `Patient_meetsPTSD_DSM5` o `Patient_meetsPTSD_ICD11`.
4. Verificar que el cambio no introduce inconsistencias con los disjuntos existentes.

---

## Razonadores compatibles y configuración recomendada

| Razonador | Velocidad ABox | Explicaciones | Recomendado para |
|---|---|---|---|
| **Fact++** | Muy rápida | Sí (una) | Clasificación de grandes conjuntos de pacientes |
| HermiT | Media | Sí (múltiples) | Depuración de inconsistencias |
| Pellet | Compatible | Sí | Uso programático con `owlready2` |

**Configuración óptima para ABox grande (>100 individuos):**
En Protégé: `Reasoner → Fact++ → Preferences → Disable timeout`.

**Uso programático con Pellet:**
```python
from owlready2 import *
onto = get_ontology("ontologia.rdf").load()
with onto:
    sync_reasoner_pellet(infer_property_values=True,
                         infer_data_property_values=True)
```

---

## Notas sobre datos reales de pacientes

Los datos de pacientes son información clínica sensible. Al poblar la ontología con datos reales:

1. **Anonimizar** todos los identificadores antes de la carga (usar códigos, no nombres).
2. **No subir** archivos poblados con datos reales al repositorio (están excluidos en `.gitignore`).
3. La ontología **no almacena** información de texto libre; solo propiedades de datos estructuradas (enteros, booleanos, flotantes).
4. Las instancias de `Patient` en la ontología corresponden a registros clínicos abstractos, no a personas identificadas.
