# OnTEPT — Ontología Multimodal para la Identificación del Trastorno de Estrés Postraumático

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![OWL Version](https://img.shields.io/badge/OWL-2%20DL-blue)](https://www.w3.org/TR/owl2-profiles/)
[![Ontology Version](https://img.shields.io/badge/version-1.0-green)](ontology/current/onTEPT_v1.0.rdf)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

**OnTEPT** (*Ontología para la identificación del Trastorno de Estrés Postraumático*) es una ontología OWL 2 DL multimodal que integra los criterios diagnósticos del DSM-5 y la CIE-11, instrumentos psicométricos estandarizados y datos electrofisiológicos (EEG) para la identificación automatizada del TEPT mediante razonamiento ontológico.

> **Nota sobre el idioma:** Esta ontología es bilingüe (español/inglés). Todos los elementos contienen `rdfs:label` y `rdfs:comment` en ambos idiomas. Esta documentación se ofrece principalmente en español para reflejar el contexto de desarrollo; la documentación técnica en inglés está disponible en [`docs/technical-guide.md`](docs/technical-guide.md).

---

## Índice

1. [¿Qué es OnTEPT?](#qué-es-ontept)
2. [Características principales](#características-principales)
3. [Estructura del repositorio](#estructura-del-repositorio)
4. [Inicio rápido](#inicio-rápido)
5. [Cobertura diagnóstica](#cobertura-diagnóstica)
6. [Instrumentos psicométricos modelados](#instrumentos-psicométricos-modelados)
7. [Datos EEG](#datos-eeg)
8. [Razonamiento e inferencia](#razonamiento-e-inferencia)
9. [Población con datos reales](#población-con-datos-reales)
10. [Citación](#citación)
11. [Licencia](#licencia)
12. [Contacto](#contacto)

---

## ¿Qué es OnTEPT?

El TEPT es un trastorno cuyo diagnóstico depende de la convergencia de criterios clínicos heterogéneos distribuidos en múltiples sistemas de clasificación (DSM-5, CIE-11) y evaluados mediante instrumentos dispares (PCL-5, CAPS-5, PC-PTSD-5). Esta dispersión dificulta la reproducibilidad diagnóstica y la interoperabilidad entre sistemas.

OnTEPT formaliza ese conocimiento en una ontología OWL 2 DL que permite:

- **Clasificación automática** de pacientes en subclases diagnósticas mediante razonadores estándar (Fact++, HermiT).
- **Interoperabilidad formal** entre DSM-5 y CIE-11, axiomatizada mediante `SubClassOf` y reglas de equivalencia.
- **Mapeo explícito** entre ítems de instrumentos psicométricos y subcriterios diagnósticos, eliminando reglas de puntuación implícitas.
- **Detección de inconsistencias** lógicas en los datos de pacientes.
- **Integración de biomarcadores EEG** mediante más de 20 características extraídas de señales electrofisiológicas.

La ontología fue desarrollada como parte de una investigación doctoral en la Universidad de Nariño (Colombia) y ha sido validada con datos de pacientes reales y conjuntos sintéticos.

---

## Características principales

| Característica | Detalle |
|---|---|
| Perfil OWL | OWL 2 DL |
| Idiomas | Español / Inglés (bilingüe) |
| Criterios cubiertos | DSM-5 (A–H, subtipo disociativo) · CIE-11 (1–6, TEPT complejo) |
| Instrumentos modelados | PCL-5 (20 ítems) · CAPS-5 (30 ítems) · PC-PTSD-5 (5 ítems) · PCL-C (17 ítems, DSM-IV) |
| Características EEG | > 20 propiedades por canal y segmento |
| Razonadores compatibles | Fact++ · HermiT · Pellet |
| Editor recomendado | Protégé 5.x |
| Formato | RDF/XML (`.rdf`) |
| Versión actual | 1.0 |
| Alineamiento externo | MESH (referencia en `rdfs:comment`) |

---

## Estructura del repositorio

```
onTEPT/
│
├── README.md                          ← Este archivo
├── LICENSE                            ← CC BY 4.0
├── CITATION.cff                       ← Metadatos de citación (formato CFF)
├── CHANGELOG.md                       ← Historial de versiones
├── .gitignore
│
├── ontology/                          ← Archivos OWL de la ontología
│   ├── current/
│   │   └── onTEPT_v1.0.rdf            ← Versión estable actual
│   └── versions/                      ← Versiones anteriores (historial)
│       ├── onTEPT_v0.9.rdf
│       └── ...
│
├── code/                              ← Código fuente Python
│   ├── README.md                      ← Documentación de los scripts
│   ├── MenuPrincipal.py               ← Punto de entrada principal (menú interactivo)
│   │
│   ├── population/                    ← Scripts de población con datos reales
│   │   ├── poblar_PCL5.py             ← Población desde PCL-5
│   │   ├── poblar_PCLC.py             ← Población desde PCL-C (DSM-IV)
│   │   ├── poblar_PCPTSD5.py          ← Población desde PC-PTSD-5
│   │   ├── poblar_CAPS5.py            ← Población desde CAPS-5
│   │   ├── poblar_EEG.py              ← Población desde registros EEG
│   │   └── poblar_sinteticos.py       ← Generación de datos sintéticos
│   │
│   ├── interface/                     ← Interfaz gráfica de usuario
│   │   ├── app.py                     ← Aplicación principal (GUI)
│   │   └── README.md
│   │
│   └── utils/                         ← Utilidades compartidas
│       ├── ontology_utils.py          ← Carga, guardado y consultas SPARQL
│       ├── validators.py              ← Validación de datos de entrada
│       └── sparql_queries.py          ← Consultas SPARQL predefinidas
│
├── populated/                         ← Ontologías pobladas (ejemplos)
│   ├── README.md
│   ├── instruments/                   ← Pobladas con datos psicométricos
│   │   ├── onTEPT_v1.0_PCL5.rdf
│   │   ├── onTEPT_v1.0_CAPS5.rdf
│   │   └── onTEPT_v1.0_PCPTSD5.rdf
│   ├── synthetic/                     ← Pobladas con datos sintéticos
│   │   ├── onTEPT_v1.0_sinteticos_consistente.rdf
│   │   └── onTEPT_v1.0_sinteticos_inconsistentes.rdf
│   └── eeg/                           ← Pobladas con datos EEG
│       └── onTEPT_v1.0_EEG.rdf
│
├── docs/                              ← Documentación extendida
│   ├── technical-guide.md             ← Guía técnica completa (EN)
│   ├── guia-tecnica.md                ← Guía técnica completa (ES)
│   ├── sparql-examples.md             ← Ejemplos de consultas SPARQL
│   ├── ontology-overview.md           ← Descripción de clases y propiedades
│   └── figures/                       ← Figuras y diagramas
│       ├── class-hierarchy.png
│       └── diagnostic-flow.png
│
└── tests/                             ← Pruebas automatizadas
    ├── README.md
    ├── test_consistency.py            ← Pruebas de consistencia lógica
    ├── test_inference.py              ← Pruebas de inferencia
    └── test_interoperability.py       ← Pruebas de interoperabilidad DSM-5/CIE-11
```

---

## Inicio rápido

### Requisitos

- Python 3.9 o superior
- Java 11 o superior (necesario para los razonadores OWL)
- [Protégé 5.x](https://protege.stanford.edu/) (recomendado para exploración visual)

### Instalación

```bash
git clone https://github.com/TU_USUARIO/onTEPT.git
cd onTEPT
pip install -r requirements.txt
```

### Explorar la ontología en Protégé

1. Abrir Protégé 5.x.
2. `File → Open → ontology/current/onTEPT_v1.0.rdf`.
3. `Reasoner → Fact++ → Start Reasoner`.
4. Explorar la jerarquía de clases en la pestaña `Classes`.

### Usar el menú principal (Python)

```bash
cd code
python MenuPrincipal.py
```

El menú guía la selección del tipo de datos (instrumentos, EEG, sintéticos) y la ruta de la ontología base.

### Consulta mínima SPARQL

```sparql
PREFIX : <http://www.semanticweb.org/alejo/ontologies/2025/0/OnTEPT#>

SELECT ?paciente WHERE {
    ?paciente a :Patient_meetsPTSD_DSM5 .
}
```

Esta consulta (ejecutada en Protégé con razonador activo) retorna todos los pacientes clasificados como TEPT según DSM-5.

---

## Cobertura diagnóstica

OnTEPT modela los criterios diagnósticos de dos sistemas de clasificación principales.

### DSM-5 (American Psychiatric Association, 2013)

| Criterio | Clase OnTEPT | Restricción lógica |
|---|---|---|
| A – Exposición al trauma | `Patient_meetsDSM5_A` | `hasEvent some TraumaticEvent` |
| B – Intrusión (≥1) | `Patient_meetsDSM5_B` | `hasSymptom some IntrusionSymptom` |
| C – Evitación (≥1) | `Patient_meetsDSM5_C` | `hasSymptom some AvoidanceSymptom` |
| D – Alteraciones cogn./ánimo (≥2) | `Patient_meetsDSM5_D` | `hasSymptom min 2 AffectiveCognitiveAlteration` |
| E – Hiperactivación (≥2) | `Patient_meetsDSM5_E` | `hasSymptom min 2 ThreatArousalSymptom` |
| F – Duración (>1 mes) | `Patient_meetsDSM5_F` | `duration some integer[≥1]` |
| G – Deterioro funcional | `Patient_meetsDSM5_G` | `disturbanceClinicallySignificant value true` |
| H – Exclusión etiológica | `Patient_meetsDSM5_H` | `attributableEffectsSubstance value false` |
| Subtipo disociativo | `Patient_meetsPTSD_WithDissociative_DSM5` | `+Patient_meetsDSM5_XDissociative` |

### CIE-11 (OMS, 2022)

| Criterio | Clase OnTEPT | Restricción lógica |
|---|---|---|
| 1 – Exposición al trauma | `Patient_meetsICD11_1` | `hasEvent some TraumaticEvent` |
| 2 – Re-experimentación (≥1) | `Patient_meetsICD11_2` | `hasSymptom some IntrusionSymptom` |
| 3 – Evitación (≥1) | `Patient_meetsICD11_3` | `hasSymptom some AvoidanceSymptom` |
| 4 – Amenaza persistente (≥1) | `Patient_meetsICD11_4` | `hasSymptom some ThreatArousalSymptom` |
| 5 – Duración | `Patient_meetsICD11_5` | `duration some integer[≥1]` |
| 6 – Deterioro funcional | `Patient_meetsICD11_6` | `disturbanceClinicallySignificant value true` |
| TEPT complejo (DSO) | `Patient_meetsPTSD_Complex_ICD11` | `+AffectDysregulation +NegativeSelfConcept +RelationalDisturbance` |

### Interoperabilidad formal

```
Patient_meetsPTSD_DSM5 SubClassOf Patient_meetsPTSD_ICD11
```

Este axioma, añadido en la versión 1.0, garantiza que todo paciente diagnosticado bajo DSM-5 sea también inferido como TEPT según CIE-11. La relación inversa no se axiomatiza porque la CIE-11 no exige el Criterio D.

---

## Instrumentos psicométricos modelados

| Instrumento | Ítems | Escala | Umbral probable | Clase OnTEPT |
|---|---|---|---|---|
| PCL-5 | 20 | 0–4 | ≥31 | `PTSD_Checklist_PCL5` |
| CAPS-5 | 30 | 0–4 | ≥31 (ítems 1–20) | `Clinician_Administered_PTSD_Scale_(CAPS)` |
| PC-PTSD-5 | 5 | 0/1 | ≥3 | `PrimaryCarePTSD_Screen_PC-PTSD-5` |
| PCL-C | 17 | 1–5 | ≥44 | `PTSD_Checklist_PCL-C` |

Cada ítem del PCL-5 y la CAPS-5 lleva una anotación `evaluatesSymptomCluster` que lo vincula al subcriterio DSM-5 que evalúa (p. ej., `PCL_Item1 evaluatesSymptomCluster DSM5_CriterionB1:IntrusiveMemories`). Esta anotación hace el mapeo ítem–criterio explícito y consultable mediante SPARQL, sin comprometer la decidibilidad del perfil OWL 2 DL.

**Nota:** El PCL-C está modelado para compatibilidad histórica con datos DSM-IV, pero no participa en la clase `Patient_probablyMeets_PTSD_byAssesmentInstrument`, que solo incluye instrumentos alineados con DSM-5.

---

## Datos EEG

OnTEPT integra más de 20 características EEG extraídas de señales electrofisiológicas, organizadas en cuatro ritmos cerebrales (Delta/A4, Gamma/D1, Beta/D2, Alpha/D3, Theta/D4). Las propiedades de datos incluyen:

`mean` · `median` · `variance` · `standardDeviation` · `kurtosis` · `rootMeanSquare` · `RSSQ` · `SSI` · `areaUnderCurve` · `shannonEntropy` · `logEnergyEntropy` · `histogramEntropy` · `fftMean` · `fftMaximum` · `fftVariance` · `fftMedian` · `fftPeakFrequency` · `P1Mean` · `P1Maximum` · `P1Power` · `correlationEnergy13` · `correlationEnergy23` · `correlationPeakCount` · `envelopeAsymmetry` · `envelopeKurtosis` · `asymmetryIndexDecay`

Cada instancia de `EEG_Recording` se vincula al paciente mediante `hasEEGRecording` y puede especificar `channel` (nombre del electrodo) y `rhythm` (banda de frecuencia).

---

## Razonamiento e inferencia

La clasificación diagnóstica se obtiene mediante razonamiento OWL 2 DL. No es necesario declarar explícitamente la clase diagnóstica de un paciente: el razonador la infiere a partir de las propiedades del individuo.

### Razonadores compatibles

| Razonador | Velocidad | Notas |
|---|---|---|
| **Fact++** | Rápido | Recomendado para ABox con muchos individuos |
| HermiT | Medio | Más detallado en explicaciones de inconsistencias |
| Pellet | Compatible | Soporta SWRL si se requieren reglas externas |

### Ejecución en Protégé

```
Reasoner → Fact++ → Start Reasoner
```

Una vez activo el razonador, las clases inferidas aparecen resaltadas en la jerarquía. Para consultas, usar `Tools → SPARQL Query`.

### Ejecución programática (owlready2)

```python
from owlready2 import *

onto = get_ontology("ontology/current/onTEPT_v1.0.rdf").load()
with onto:
    sync_reasoner_pellet(infer_property_values=True)

for ind in onto.Patient_meetsPTSD_DSM5.instances():
    print(ind.name)
```

---

## Población con datos reales

El directorio `code/population/` contiene scripts modulares para poblar la ontología con datos de diferentes fuentes. El punto de entrada es `MenuPrincipal.py`.

```
code/
└── MenuPrincipal.py     ← Menú interactivo; llama a los módulos siguientes
    ├── poblar_PCL5.py       Datos del cuestionario PCL-5
    ├── poblar_PCLC.py       Datos del cuestionario PCL-C (DSM-IV)
    ├── poblar_PCPTSD5.py    Datos del cribado PC-PTSD-5
    ├── poblar_CAPS5.py      Datos de la entrevista CAPS-5
    ├── poblar_EEG.py        Características extraídas de señales EEG
    └── poblar_sinteticos.py Generación paramétrica de instancias sintéticas
```

Cada script recibe como argumentos la ruta de la ontología base, el archivo de datos (CSV o similar) y el archivo de salida. Todos los scripts preservan el archivo original y generan un `_backup.rdf` antes de modificar la ontología.

Para instrucciones detalladas, ver [`code/README.md`](code/README.md).

---

## Versiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0 | 2025-XX | Versión inicial pública. DSM-5 (A–H), CIE-11 (1–6), TEPT complejo, subtipo disociativo, CAPS-5 (30 ítems), interoperabilidad formal, annotation property `evaluatesSymptomCluster`. |

El historial completo de cambios está en [`CHANGELOG.md`](CHANGELOG.md).

Las versiones anteriores al lanzamiento público están disponibles en [`ontology/versions/`](ontology/versions/).

---

## Citación

Si OnTEPT es útil para tu investigación, por favor cita el artículo asociado:

```
[Referencia pendiente de publicación]
```

El archivo [`CITATION.cff`](CITATION.cff) contiene los metadatos en formato Citation File Format para gestores de referencias compatibles (Zotero, GitHub, etc.).

Para citar el repositorio directamente:

```
Apellido, A. (2025). OnTEPT: Ontología Multimodal para la Identificación
del Trastorno de Estrés Postraumático (v1.0) [Software].
GitHub. https://github.com/TU_USUARIO/onTEPT
DOI: 10.5281/zenodo.XXXXXXX
```

---

## Licencia

La ontología (archivos `.rdf`) y la documentación se distribuyen bajo la licencia [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). El código fuente Python se distribuye bajo la licencia [MIT](LICENSE).

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor consultar [`CONTRIBUTING.md`](CONTRIBUTING.md) antes de abrir un *pull request*. Para reportar errores o sugerir mejoras, usar la sección [Issues](https://github.com/TU_USUARIO/onTEPT/issues).

---

## Contacto

- **Desarrollo y mantenimiento:** Alejandro [Apellido] — Universidad de Nariño, Colombia
- **Correo:** [correo@udenar.edu.co]
- **ORCID:** [https://orcid.org/XXXX-XXXX-XXXX-XXXX]

---

*OnTEPT forma parte de una investigación doctoral en ingeniería biomédica centrada en el apoyo computacional al diagnóstico de trastornos de estrés postraumático.*
