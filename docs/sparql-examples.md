# Consultas SPARQL de referencia — OnTEPT

Todas las consultas de esta página asumen el prefijo:

```sparql
PREFIX : <http://www.semanticweb.org/alejo/ontologies/2025/0/OnTEPT#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
```

Deben ejecutarse en **Protégé → Tools → SPARQL Query** con el razonador activo (Fact++), salvo las marcadas como *sin razonador*.

---

## Bloque 1 — Criterios individuales DSM-5

### Q1.1 Pacientes con evento traumático válido (Criterio A)
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient .
    ?paciente :hasEvent ?ev .
    ?ev :TraumaticEventProperty true .
} ORDER BY ?paciente
```

### Q1.2 Pacientes con al menos un síntoma de intrusión (Criterio B)
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient .
    ?paciente :hasSymptom ?s .
    ?s a :IntrusionSymptom .
} ORDER BY ?paciente
```

### Q1.3 Pacientes con al menos un síntoma de evitación (Criterio C)
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient .
    ?paciente :hasSymptom ?s .
    ?s a :AvoidanceSymptom .
} ORDER BY ?paciente
```

### Q1.4 Pacientes con ≥2 alteraciones cognitivo-afectivas (Criterio D)
```sparql
SELECT DISTINCT ?paciente WHERE {
    { SELECT ?paciente (COUNT(DISTINCT ?s) AS ?n) WHERE {
        ?paciente :hasSymptom ?s .
        ?s a :AffectiveCognitiveAlteration .
    } GROUP BY ?paciente }
    FILTER(?n >= 2)
} ORDER BY ?paciente
```

### Q1.5 Pacientes con ≥2 síntomas de hiperactivación (Criterio E)
```sparql
SELECT DISTINCT ?paciente WHERE {
    { SELECT ?paciente (COUNT(DISTINCT ?s) AS ?n) WHERE {
        ?paciente :hasSymptom ?s .
        ?s a :ThreatArousalSymptom .
    } GROUP BY ?paciente }
    FILTER(?n >= 2)
} ORDER BY ?paciente
```

---

## Bloque 2 — Clasificación diagnóstica completa (requiere razonador)

### Q2.1 Pacientes con TEPT según DSM-5
```sparql
SELECT DISTINCT ?paciente WHERE {
    { ?paciente a :Patient_meetsPTSD_DSM5 . }
    UNION
    { ?paciente a :Patient_meetsPTSD_WithDissociative_DSM5 . }
} ORDER BY ?paciente
```

### Q2.2 Pacientes con TEPT clásico DSM-5 (sin subtipo disociativo)
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient_meetsPTSD_DSM5 .
} ORDER BY ?paciente
```

### Q2.3 Pacientes con TEPT subtipo disociativo DSM-5
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient_meetsPTSD_WithDissociative_DSM5 .
} ORDER BY ?paciente
```

### Q2.4 Pacientes con TEPT según CIE-11 (clásico)
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient_meetsPTSD_ICD11 .
} ORDER BY ?paciente
```

### Q2.5 Pacientes con TEPT complejo CIE-11
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient_meetsPTSD_Complex_ICD11 .
} ORDER BY ?paciente
```

### Q2.6 Pacientes con TEPT probable según instrumentos psicométricos
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient_probablyMeets_PTSD_byAssesmentInstrument .
} ORDER BY ?paciente
```

---

## Bloque 3 — Interoperabilidad DSM-5 / CIE-11

### Q3.1 Concordancia: pacientes con TEPT según ambos sistemas
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient_meetsPTSD_ICD11 .
    { ?paciente a :Patient_meetsPTSD_DSM5 . }
    UNION
    { ?paciente a :Patient_meetsPTSD_WithDissociative_DSM5 . }
} ORDER BY ?paciente
```

### Q3.2 Divergencia: pacientes con TEPT CIE-11 pero NO DSM-5
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient_meetsPTSD_ICD11 .
    FILTER NOT EXISTS { ?paciente a :Patient_meetsPTSD_DSM5 . }
    FILTER NOT EXISTS { ?paciente a :Patient_meetsPTSD_WithDissociative_DSM5 . }
} ORDER BY ?paciente
```

### Q3.3 Tabla de clasificación cruzada por paciente
```sparql
SELECT ?paciente ?criterio WHERE {
    ?paciente a :Patient .
    ?paciente a ?criterio .
    VALUES ?criterio {
        :Patient_meetsPTSD_DSM5
        :Patient_meetsPTSD_WithDissociative_DSM5
        :Patient_meetsPTSD_ICD11
        :Patient_meetsPTSD_Complex_ICD11
    }
} ORDER BY ?paciente ?criterio
```

---

## Bloque 4 — Mapeo ítem–criterio (sin razonador)

### Q4.1 Ítems del PCL-5 y los criterios que evalúan
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?item ?etiqueta ?criterio WHERE {
    ?item a owl:DatatypeProperty .
    ?item :evaluatesSymptomCluster ?criterio .
    OPTIONAL { ?item rdfs:label ?etiqueta . FILTER(LANG(?etiqueta)="en") }
} ORDER BY ?item
```

### Q4.2 Ítems de CAPS-5 que evalúan el Criterio B (intrusión)
```sparql
SELECT ?item WHERE {
    ?item :evaluatesSymptomCluster :DSM5_CriterionB_IntrusionSymptoms .
} ORDER BY ?item
```

---

## Bloque 5 — Validación y control de calidad (sin razonador)

### Q5.1 Pacientes sin evento traumático
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient .
    FILTER NOT EXISTS {
        ?paciente :hasEvent ?ev .
        ?ev :TraumaticEventProperty true .
    }
} ORDER BY ?paciente
```

### Q5.2 Pacientes con síntomas nucleares pero sin evento traumático
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient .
    ?paciente :hasSymptom ?s . ?s a :IntrusionSymptom .
    FILTER NOT EXISTS {
        ?paciente :hasEvent ?ev .
        ?ev :TraumaticEventProperty true .
    }
} ORDER BY ?paciente
```

### Q5.3 Pacientes con síntomas atribuibles a sustancias
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient .
    ?paciente :hasSymptom ?s .
    ?s :attributableEffectsSubstance true .
} ORDER BY ?paciente
```

### Q5.4 Pacientes con síntomas disociativos
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient .
    ?paciente :hasSymptom ?s .
    { ?s a :DepersonalizationSymptom . } UNION { ?s a :DerealizationSymptom . }
} ORDER BY ?paciente
```

### Q5.5 Pacientes con síntomas DSO (TEPT complejo)
```sparql
SELECT DISTINCT ?paciente WHERE {
    ?paciente a :Patient .
    ?paciente :hasSymptom ?s .
    ?s a :SelfOrganizationDisturbance .
} ORDER BY ?paciente
```

### Q5.6 Pacientes con inicio demorado de síntomas
```sparql
SELECT ?paciente ?sintoma ?meses WHERE {
    ?paciente a :Patient .
    ?paciente :hasSymptom ?sintoma .
    ?sintoma :onsetDelayInMonths ?meses .
} ORDER BY ?paciente
```
