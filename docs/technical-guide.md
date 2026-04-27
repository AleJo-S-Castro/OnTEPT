# Technical Guide — OnTEPT v1.0

This document describes the technical design of OnTEPT, intended for researchers who need to extend, align, or integrate the ontology into external systems.

---

## OWL 2 DL Profile

OnTEPT conforms to the **OWL 2 DL** profile, which guarantees decidable reasoning. All class definitions use standard OWL 2 DL constructs:

- `owl:equivalentClass` with `owl:intersectionOf` for diagnostic criteria classes.
- `owl:minQualifiedCardinality` for Criteria D and E (minimum 2 symptoms).
- `owl:hasValue` for boolean data property restrictions (Criteria G and H).
- `owl:someValuesFrom` with `rdfs:Datatype` and `xsd:minInclusive` for duration thresholds (Criterion F).
- `owl:complementOf` to exclude the dissociative subtype from the classic PTSD class.
- `owl:disjointWith` between mutually exclusive diagnostic classes.

**Reasoning is closed-world.** Absence of a required property is treated as failure to meet the corresponding criterion. This is appropriate for diagnostic classification but requires complete data for accurate inference.

---

## IRI Namespace

```
Base IRI: http://www.semanticweb.org/alejo/ontologies/2025/0/OnTEPT#
Prefix:   :
```

For external alignments, `owl:sameAs` or `skos:exactMatch` axioms can be added to map OnTEPT classes to terms in MFO, MDO, HP, or SNOMED CT.

---

## Formal Interoperability Axiom

```
:Patient_meetsPTSD_DSM5 rdfs:subClassOf :Patient_meetsPTSD_ICD11
```

This axiom encodes the semantic relationship between the two classification systems: the DSM-5 criterion set subsumes the ICD-11 criterion set (DSM-5 requires Criterion D, which ICD-11 does not). The converse is not axiomatized, preserving the known asymmetry.

**Entailment:** Any individual inferred as `Patient_meetsPTSD_DSM5` is automatically entailed as `Patient_meetsPTSD_ICD11` without requiring explicit assertion.

---

## Equivalence Axioms for Diagnostic Classes

### Patient_meetsPTSD_DSM5
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

### Patient_meetsPTSD_Complex_ICD11
```manchester
Patient
  and Patient_meetsICD11_1 ... Patient_meetsICD11_6
  and Patient_meetsICD11_XComplex
```
where `Patient_meetsICD11_XComplex ≡ hasSymptom some AffectDysregulation and hasSymptom some NegativeSelfConcept and hasSymptom some RelationalDisturbance`

---

## Extending the Ontology

### Adding a new symptom class

1. Declare the class as a subclass of the appropriate cluster class:
   ```turtle
   :MyNewSymptom a owl:Class ;
       rdfs:subClassOf :IntrusionSymptom ;
       rdfs:label "my new symptom"@en ;
       rdfs:label "mi nuevo síntoma"@es ;
       rdfs:comment "Description in English."@en ;
       rdfs:comment "Descripción en español."@es .
   ```
2. Verify consistency with Fact++ before committing.

### Adding a new instrument

1. Create a subclass of `Self-ReportInstrument`, `ScreeningInstrument`, or `ClinicianAdministeredInstrument`.
2. Add item data properties as functional subproperties of a new parent instrument property.
3. Add `evaluatesSymptomCluster` annotations on each item property.
4. If the instrument has a diagnostic threshold, update `Patient_probablyMeets_PTSD_byAssesmentInstrument` with a new `isAssessedBy some (InstrumentClass and scoreProperty some integer[≥threshold])` branch.

### Aligning with external ontologies

To align a class with an external term, add:
```turtle
:IntrusionSymptom owl:sameAs <http://purl.obolibrary.org/obo/HP_XXXXXXX> .
```
or with `skos:exactMatch` for looser alignment.

---

## Consistency Testing

Run the tests in `tests/` to verify that the ontology remains consistent after modifications:

```bash
python tests/test_consistency.py
python tests/test_inference.py
python tests/test_interoperability.py
```

These scripts use `owlready2` with `sync_reasoner_pellet()`. Java must be installed and accessible in `PATH`.
