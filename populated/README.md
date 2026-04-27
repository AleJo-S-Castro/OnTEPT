# Ontologías pobladas — OnTEPT

Este directorio contiene versiones de la ontología OnTEPT ya pobladas con distintos tipos de instancias, a modo de ejemplos reproducibles para la validación del razonamiento.

> ⚠ **Importante:** Ningún archivo en este directorio contiene datos reales identificables de pacientes. Todos los archivos aquí presentes se basan en datos sintéticos o datos anonimizados de ejemplo.

## Estructura

```
populated/
├── instruments/          ← Pobladas con datos psicométricos (sintéticos/ejemplo)
│   ├── onTEPT_v1.0_PCL5.rdf
│   ├── onTEPT_v1.0_CAPS5.rdf
│   └── onTEPT_v1.0_PCPTSD5.rdf
│
├── synthetic/            ← Pobladas con datos sintéticos para validación
│   ├── onTEPT_v1.0_sinteticos_consistente.rdf
│   └── onTEPT_v1.0_sinteticos_inconsistentes.rdf
│
└── eeg/                  ← Pobladas con características EEG de ejemplo
    └── onTEPT_v1.0_EEG.rdf
```

## Descripción de los archivos

### `synthetic/onTEPT_v1.0_sinteticos_consistente.rdf`

Contiene 26 pacientes sintéticos organizados en 7 grupos funcionales para la validación del razonamiento:

| Grupo | n | Perfil | Clasificación inferida esperada |
|---|---|---|---|
| G1 | 3 | DSM-5 A–H completo | `Patient_meetsPTSD_DSM5` ∩ `Patient_meetsPTSD_ICD11` |
| G2 | 10 | Falla un criterio DSM-5 | ningún diagnóstico de TEPT |
| G3 | 2 | DSM-5 A–H + subtipo disociativo | `Patient_meetsPTSD_WithDissociative_DSM5` |
| G4 | 1 | DSM-5 A–H + DSO | `Patient_meetsPTSD_DSM5` ∩ `Patient_meetsPTSD_Complex_ICD11` |
| G5 | 2 | CIE-11 1–6, falla D (solo 1 AffCogAlt) | `Patient_meetsPTSD_ICD11` (no DSM-5) |
| G6 | 2 | CIE-11 1–6, falla H (atrib. sustancias) | `Patient_meetsPTSD_ICD11` (no DSM-5) |
| G9 | 6 | Falla un criterio CIE-11 | ningún diagnóstico de TEPT |

### `synthetic/onTEPT_v1.0_sinteticos_inconsistentes.rdf`

Contiene 6 pacientes con inconsistencias lógicas intencionales (Grupos 7 y 8). Al ejecutar el razonador sobre este archivo, debe reportar **ontología inconsistente**. No abrir junto con el archivo consistente.

### `instruments/` y `eeg/`

Ejemplos de estructura con instancias generadas a partir de datos sintéticos que siguen el formato de los instrumentos reales. Útiles para verificar la ejecución de los scripts de población.

## Cómo ejecutar el razonador sobre estos archivos

```
1. Abrir el archivo en Protégé 5.x
2. Reasoner → Fact++ → Start Reasoner
3. Explorar clasificaciones en la pestaña Classes
4. Para consultas: Tools → SPARQL Query
```

Consultas de ejemplo disponibles en [`../docs/sparql-examples.md`](../docs/sparql-examples.md).
