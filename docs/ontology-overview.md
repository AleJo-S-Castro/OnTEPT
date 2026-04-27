# Descripción de clases y propiedades — OnTEPT v1.0

Este documento ofrece una referencia completa de los elementos de la ontología, organizados por módulo temático.

---

## 1. Jerarquía de clases principales

```
owl:Thing
├── Person
│   └── Patient
│       ├── Patient_meetsDSM5_A          (Criterio A)
│       ├── Patient_meetsDSM5_B          (Criterio B)
│       ├── Patient_meetsDSM5_C          (Criterio C)
│       ├── Patient_meetsDSM5_D          (Criterio D, ≥2 AffCogAlt)
│       ├── Patient_meetsDSM5_E          (Criterio E, ≥2 ThreatArousal)
│       ├── Patient_meetsDSM5_F          (Criterio F, duración)
│       ├── Patient_meetsDSM5_G          (Criterio G, deterioro funcional)
│       ├── Patient_meetsDSM5_H          (Criterio H, exclusión sustancias)
│       ├── Patient_meetsDSM5_XDissociative
│       ├── Patient_meetsPTSD_DSM5        ← Diagnóstico TEPT DSM-5 completo
│       ├── Patient_meetsPTSD_WithDissociative_DSM5
│       ├── Patient_meetsICD11_1–6        (Criterios individuales CIE-11)
│       ├── Patient_meetsICD11_XComplex
│       ├── Patient_meetsPTSD_ICD11       ← Diagnóstico TEPT CIE-11 completo
│       ├── Patient_meetsPTSD_Complex_ICD11
│       └── Patient_probablyMeets_PTSD_byAssesmentInstrument
│
├── Event
│   ├── TraumaticEvent
│   └── NonTraumaticEvent
│
├── Symptom
│   ├── IntrusionSymptom
│   ├── AvoidanceSymptom
│   ├── AffectiveCognitiveAlteration
│   ├── ThreatArousalSymptom
│   ├── DissociativeSymptom
│   │   ├── DepersonalizationSymptom
│   │   └── DerealizationSymptom
│   └── SelfOrganizationDisturbance
│       ├── AffectDysregulation
│       ├── NegativeSelfConcept
│       └── RelationalDisturbance
│
├── DiagnosticCriterion
│   ├── PTSD_DSM_5_DiagnosticCriterion
│   │   ├── DSM5_CriterionA_Exposure
│   │   │   ├── DSM5_CriterionA1_DirectExposure
│   │   │   ├── DSM5_CriterionA2_Witnessing
│   │   │   ├── DSM5_CriterionA3_IndirectExposure
│   │   │   └── DSM5_CriterionA4_XtremeOrRepeatedExposure
│   │   ├── DSM5_CriterionB_IntrusionSymptoms (B1–B5)
│   │   ├── DSM5_CriterionC_AvoidanceSymptoms (C1–C2)
│   │   ├── DSM5_CriterionD_AffectiveCognitiveAlteration (D1–D7)
│   │   ├── DSM5_CriterionE_ThreatArousalSymptom (E1–E6)
│   │   ├── DSM5_CriterionF_SymptomsDuration
│   │   ├── DSM5_CriterionG_DisturbanceSignificant
│   │   ├── DSM5_CriterionH_AttributableSubstance
│   │   └── DSM5_CriterionX_Dissociative
│   └── PTSD_ICD_11_DiagnosticCriterion
│       ├── ICD11_Criterion1_Exposure
│       ├── ICD11_Criterion2_IntrusionSymptom
│       ├── ICD11_Criterion3_AvoidanceSymptom
│       ├── ICD11_Criterion4_ThreatArousalSymptom
│       ├── ICD11_Criterion5_SymptomsDuration
│       ├── ICD11_Criterion6_DisturbanceSignificant
│       └── ICD11_Criterion_Complex
│
├── TraumaAndStressorRelatedDisorders
│   └── TraumaticStressDisorders
│       └── PTSD_subtype
│           ├── PTSD_Classic
│           ├── PTSD_Complex
│           └── PTSD_withDissociativeSymptom
│
├── AssessmentInstrument
│   └── PsychometricAssessmentInstrument
│       ├── Self-ReportInstrument
│       │   ├── PTSD_Checklist_PCL
│       │   │   ├── PTSD_Checklist_PCL5
│       │   │   └── PTSD_Checklist_PCL-C
│       │   └── Evaluación_Global_de_Estrés_Postraumático_(EGEP-5)
│       ├── ScreeningInstrument
│       │   ├── PrimaryCarePTSD_Screen_PC-PTSD-5
│       │   ├── Screen_for_Posttraumatic_Stress_Symptoms_(SPTSS)
│       │   └── Trauma_Screening_Questionnaire_(TSQ)
│       └── ClinicianAdministeredInstrument
│           ├── Clinician_Administered_PTSD_Scale_(CAPS)
│           ├── Mini_International_Neuropsychiatric_Interview_(MINI)
│           └── Structured_Clinical_Interview_for_DSM_Disorders_(SCID-5)
│
└── SignalRecording
    └── EEG_Recording
        ├── EEG_rhythm
        │   ├── A4_EEG_rhythm  (Delta)
        │   ├── D1_EEG_rhythm  (Gamma)
        │   ├── D2_EEG_rhythm  (Beta)
        │   ├── D3_EEG_rhythm  (Alpha)
        │   └── D4_EEG_rhythm  (Theta)
        └── EEG_segment
```

---

## 2. Propiedades de objeto principales

| Propiedad | Dominio | Rango | Descripción |
|---|---|---|---|
| `hasEvent` | Patient | Event | Vincula paciente con evento experimentado |
| `hasTraumaticEvent` | Patient | TraumaticEvent | Especialización para eventos traumáticos |
| `hasSymptom` | Patient | Symptom | Vincula paciente con síntomas |
| `hasDissociativeSymptom` | Patient | DissociativeSymptom | Síntomas disociativos |
| `hasComplexSymptom` | Patient | SelfOrganizationDisturbance | Síntomas DSO (TEPT complejo) |
| `meetsCriterionDSM` | Patient | PTSD_DSM_5_DiagnosticCriterion | Relación paciente–criterio DSM-5 |
| `meetsCriterionICD` | Patient | PTSD_ICD_11_DiagnosticCriterion | Relación paciente–criterio CIE-11 |
| `meetsDiagnosis` | Patient | TraumaAndStressorRelatedDisorders | Diagnóstico formal |
| `isAssessedBy` | Patient | PsychometricAssessmentInstrument | Instrumento usado |
| `assesses` | PsychometricAssessmentInstrument | Patient | Inversa de `isAssessedBy` |
| `hasEEGRecording` | Patient | EEG_Recording | Registro EEG asociado |
| `isExperiencedBy` | Event | Person | Inversa de `hasEvent` |

---

## 3. Propiedades de datos principales

| Propiedad | Dominio | Rango | Criterio | Descripción |
|---|---|---|---|---|
| `TraumaticEventProperty` | Event | boolean | A / 1 | `true` = evento traumático |
| `duration` | Symptom | integer | F / 5 | Duración en meses (≥1 para TEPT) |
| `disturbanceClinicallySignificant` | Symptom | boolean | G / 6 | Deterioro funcional significativo |
| `attributableEffectsSubstance` | Symptom | boolean | H | Atribuible a sustancias (false para cumplir H) |
| `onsetDelayInMonths` | Symptom | integer | — | Latencia en meses (inicio demorado) |
| `PCL_totalScore` | PTSD_Checklist_PCL | integer | — | Puntuación total del PCL |
| `PCL_Item1`–`PCL_Item20` | PTSD_Checklist_PCL5 | integer | B–E | Ítems individuales PCL-5 (0–4) |
| `CAPS_totalScore` | CAPS | integer | — | Puntuación total CAPS-5 (ítems 1–20) |
| `CAPS_Item1`–`CAPS_Item30` | CAPS | integer | B–G | Ítems individuales CAPS-5 (0–4) |
| `PC-PTSD_ItemtotalScore` | PC-PTSD-5 | integer | — | Puntuación total PC-PTSD-5 (0–5) |
| `PC-PTSD_Item1`–`Item5` | PC-PTSD-5 | integer | — | Ítems binarios PC-PTSD-5 (0/1) |

---

## 4. Annotation property

| Propiedad | Descripción |
|---|---|
| `evaluatesSymptomCluster` | Vincula un ítem de instrumento psicométrico con el subcriterio DSM-5 que evalúa. Rango: clase de criterio diagnóstico. Añadida en v1.0 para resolver la brecha instrumental. |

### Ejemplo de uso

```
PCL_Item1  evaluatesSymptomCluster  DSM5_CriterionB1:IntrusiveMemories
PCL_Item6  evaluatesSymptomCluster  DSM5_CriterionC1:AvoidanceOfThoughts
CAPS_Item8 evaluatesSymptomCluster  DSM5_CriterionD1:MemoryImpairment
```
