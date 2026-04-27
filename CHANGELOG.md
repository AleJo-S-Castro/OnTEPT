# Historial de cambios — OnTEPT

Todos los cambios relevantes de cada versión se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).
El versionado sigue [Semantic Versioning](https://semver.org/lang/es/).

---

## [1.0] — 2025-XX-XX — *Primera versión pública*

### Añadido
- Criterios diagnósticos DSM-5 completos (A–H), incluyendo subtipo disociativo (`Patient_meetsPTSD_WithDissociative_DSM5`).
- Criterios diagnósticos CIE-11 completos (1–6), incluyendo TEPT complejo (`Patient_meetsPTSD_Complex_ICD11`) con los tres clústeres de alteración de la autoorganización: `AffectDysregulation`, `NegativeSelfConcept`, `RelationalDisturbance`.
- Axioma de interoperabilidad formal: `Patient_meetsPTSD_DSM5 SubClassOf Patient_meetsPTSD_ICD11`.
- Annotation property `evaluatesSymptomCluster` para mapear ítems de instrumentos a subcriterios DSM-5.
- Modelo completo de CAPS-5 (30 ítems, `CAPSProperty`, `CAPS_totalScore`), con anotaciones `evaluatesSymptomCluster` en ítems 1–20.
- `PCL5Property` con dominio restringido a `PTSD_Checklist_PCL5`; ítems PCL_Item1–20 redirigidos a `PCL5Property` para evitar conflictos semánticos con PCL-C (DSM-IV).
- Propiedad de datos `onsetDelayInMonths` para modelar inicio demorado de síntomas.
- Subclases de `SelfOrganizationDisturbance` con `rdfs:label` y `rdfs:comment` bilingües.
- Propiedades de objeto `hasComplexSymptom`/`isComplexSymptomOf` e `isDissociativeSymptomOf` como inversas especializadas.
- Tres nuevas clases de diagnóstico en la jerarquía de PTSD: `PTSD_Classic`, `PTSD_Complex` (con descripción clínica completa de CIE-11).
- `AllDisjointClasses` entre `PTSD_Classic`, `PTSD_Complex` y `PTSD_withDissociativeSymptom`.
- Versión bilingüe (ES/EN) en todos los axiomas de anotación.
- `owl:versionIRI` 1.1 y `owl:versionInfo` V1.3 (número interno de desarrollo; versión pública: 1.0).

### Modificado
- Umbral de `Patient_probablyMeets_PTSD_byAssesmentInstrument` para PCL-5 ajustado de ≥33 a **≥31** (literatura: Weathers et al., 2013).
- `Patient_probablyMeets_PTSD_byAssesmentInstrument`: rama PCL-C eliminada de la equivalencia (PCL-C mapea a DSM-IV, no a DSM-5); rama CAPS-5 (≥31) añadida.
- `isASymptomOf` rango actualizado de `PTSD_classic` a `PTSD_Classic`.
- `ClinicianAdministeredInstrument`, `ClinicianAdministeredPTSDScale_(CAPS)`: `rdfs:comment` y `rdfs:label` actualizados con descripción clínica completa de CAPS-5.
- Corrección de labels invertidos en `PTSD_Checklist_PCL` (EN/ES estaban permutados).

### Corregido
- `Patient_meetsICD11_5` y `Patient_meetsICD11_6`: eliminada la dependencia de `AffectiveCognitiveAlteration` (Criterio D del DSM-5 no existe en CIE-11); se usan solo `IntrusionSymptom`, `AvoidanceSymptom` y `ThreatArousalSymptom`.
- `ICD11_Criterion_Complex`: `rdfs:comment` corregido (antes contenía el placeholder "Definition of ICD11_Criterion_Dissociative").
- `Patient_meetsICD11_Dissociative`: clase eliminada (el subtipo disociativo no existe en CIE-11; confusión resuelta).
- `AffectDysregulation`, `NegativeSelfConcept`, `RelationalDisturbance`: añadidos `rdfs:label` y `rdfs:comment` bilingües (antes estaban vacíos).
- `onsetDelayInMonths`: añadidos `rdfs:range xsd:integer`, `rdfs:domain Symptom`, `rdfs:label` en ambos idiomas y `rdfs:comment` en inglés.

---

## [Pre-release] — Versiones de desarrollo (no públicas)

Las versiones v2.9 a v2.12 son versiones internas de desarrollo disponibles en
[`ontology/versions/`](ontology/versions/) para trazabilidad del proceso de diseño.
No se documentan aquí en detalle; sus diferencias respecto a v1.0 se pueden
explorar mediante comparación de archivos RDF.
