# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 19:30:00 2026

@author: AleJo-PC-UMariana

Script v3 para poblar la ontología OnTEPT v2.12 con pacientes sintéticos.

Objetivos:
  1. Validar clasificación por INFERENCIA (razonador) según DSM-5 y CIE-11.
  2. Probar INTEROPERABILIDAD:
     - DSM-5 A-H  →  también clasifica CIE-11 1-6  (inclusión)
     - CIE-11 1-6 ↛  NO clasifica DSM-5 A-H (faltan D y/o H)
  3. Generar instancias INCONSISTENTES a propósito para validar que el
     razonador (HermiT/Pellet) detecte la inconsistencia.
  4. Ejecutar consultas de verificación tras el razonamiento.

Grupos de pacientes creados:
  GRUPO 1  – Cumplen TODOS los criterios DSM-5 (A-H sin disociativo)
             → deben clasificarse en Patient_meetsPTSD_DSM5
             → deben clasificarse TAMBIÉN en Patient_meetsPTSD_ICD11

  GRUPO 2  – Fallan exactamente un criterio DSM-5 cada uno
             → NO deben clasificarse en Patient_meetsPTSD_DSM5

  GRUPO 3  – Cumplen A-H + subtipo disociativo (DSM-5)
             → Patient_meetsPTSD_WithDissociative_DSM5
             → Patient_meetsPTSD_ICD11

  GRUPO 4  – Cumplen A-H + SelfOrganizationDisturbance
             → Patient_meetsPTSD_DSM5 (sin disociativo)
             → Patient_meetsPTSD_ICD11
             → Patient_meetsPTSD_Complex_ICD11

  GRUPO 5  – INTEROPERABILIDAD: cumplen CIE-11 1-6 pero NO DSM-5
             (tienen solo 1 AffectiveCognitiveAlteration → fallan D)
             → Patient_meetsPTSD_ICD11:  SÍ
             → Patient_meetsPTSD_DSM5:   NO

  GRUPO 6  – INTEROPERABILIDAD inversa: solo CIE-11 (sin H de DSM-5)
             (attributableEffectsSubstance=True → fallan H)
             → Patient_meetsPTSD_ICD11:  SÍ
             → Patient_meetsPTSD_DSM5:   NO

  GRUPO 7  – INCONSISTENCIAS DSM-5 (forzadas)
             Pacientes que NO cumplen un criterio, pero se clasifican
             manualmente en Patient_meetsPTSD_DSM5 → el razonador debe
             detectar inconsistencia.

  GRUPO 8  – INCONSISTENCIAS CIE-11 (forzadas)
             Pacientes que NO cumplen un criterio CIE-11, pero se clasifican
             manualmente en Patient_meetsPTSD_ICD11 → inconsistencia.

  GRUPO 9  – Fallan exactamente un criterio CIE-11 cada uno
             → NO deben clasificarse en Patient_meetsPTSD_ICD11

Uso:
  from poblar_sinteticos_ext_v3 import poblar_sinteticos_ext_v3
  poblar_sinteticos_ext_v3(ruta_ontologia, archivo_ontologia)

  O bien ejecutar directamente (ver bloque __main__ al final).
"""

from owlready2 import *
import os
import types as pytypes


def poblar_sinteticos_ext_v3(ruta_ontologia, archivo_ontologia,
                              x_cumple=3,
                              incluir_inconsistencias=True,
                              ejecutar_consultas=True):
    """
    Pobla la ontología OnTEPT v2.12 con pacientes sintéticos para validar
    razonamiento, interoperabilidad e inconsistencias.

    Parámetros
    ----------
    ruta_ontologia : str
        Directorio donde reside la ontología.
    archivo_ontologia : str
        Nombre del archivo .rdf de la ontología base.
    x_cumple : int
        Cantidad de pacientes GRUPO 1 (cumplen todo DSM-5 A-H).
    incluir_inconsistencias : bool
        Si True, crea las instancias de GRUPO 7 y 8 (inconsistentes).
        ⚠ Estas provocarán que el razonador falle por inconsistencia.
        Se guardan en un archivo SEPARADO para que puedan probarse aisladas.
    ejecutar_consultas : bool
        Si True, ejecuta consultas de verificación (sin razonador;
        el razonamiento debe hacerse en Protégé o con sync_reasoner).
    """
    # ─────────────────────────────────────────────────────────────
    # CARGA DE LA ONTOLOGÍA
    # ─────────────────────────────────────────────────────────────
    onto_path.append(ruta_ontologia)
    ruta_completa = os.path.join(ruta_ontologia, archivo_ontologia)
    onto = get_ontology(ruta_completa).load()

    print("=" * 70)
    print("  POBLAR SINTÉTICOS v3 — OnTEPT v2.13")
    print("=" * 70)
    print(f"Ontología cargada: {ruta_completa}")
    print(f"Individuos existentes: {len(list(onto.individuals()))}")

    # ─────────────────────────────────────────────────────────────
    # RECUPERAR CLASES Y PROPIEDADES DE LA ONTOLOGÍA
    # ─────────────────────────────────────────────────────────────
    # Clases de síntomas
    Patient = onto.Patient
    Symptom = onto.Symptom
    IntrusionSymptom = onto.IntrusionSymptom
    AvoidanceSymptom = onto.AvoidanceSymptom
    AffectiveCognitiveAlteration = onto.AffectiveCognitiveAlteration
    ThreatArousalSymptom = onto.ThreatArousalSymptom
    DissociativeSymptom = onto.DissociativeSymptom
    DepersonalizationSymptom = onto.DepersonalizationSymptom
    DerealizationSymptom = onto.DerealizationSymptom
    SelfOrganizationDisturbance = onto.SelfOrganizationDisturbance

    # Clases de eventos
    Event = onto.Event
    TraumaticEvent = onto.TraumaticEvent
    NonTraumaticEvent = onto.NonTraumaticEvent

    # Clases de clasificación (definidas en la ontología)
    Patient_meetsPTSD_DSM5 = onto.Patient_meetsPTSD_DSM5
    Patient_meetsPTSD_ICD11 = onto.Patient_meetsPTSD_ICD11
    Patient_meetsPTSD_WithDissociative_DSM5 = onto.Patient_meetsPTSD_WithDissociative_DSM5
    Patient_meetsPTSD_Complex_ICD11 = onto.Patient_meetsPTSD_Complex_ICD11

    # Propiedades de objeto
    hasSymptom = onto.hasSymptom
    hasDissociativeSymptom = onto.hasDissociativeSymptom
    hasEvent = onto.hasEvent

    # Propiedades de dato
    duration = onto.duration
    attributableEffectsSubstance = onto.attributableEffectsSubstance
    disturbanceClinicallySignificant = onto.disturbanceClinicallySignificant
    TraumaticEventProperty = onto.TraumaticEventProperty

    # ─────────────────────────────────────────────────────────────
    # CONTADOR GLOBAL
    # ─────────────────────────────────────────────────────────────
    contador = {"n": 0}

    def siguiente():
        contador["n"] += 1
        return contador["n"]

    # ─────────────────────────────────────────────────────────────
    # FUNCIONES AUXILIARES
    # ─────────────────────────────────────────────────────────────
    def crear_sintoma(cls_sintoma, id_pac, num, dur, atribuible, clinico):
        """Crea un individuo de síntoma con sus propiedades de dato."""
        nombre = f"Symptom_{id_pac}_{cls_sintoma.__name__}_{num}"
        s = cls_sintoma(nombre)
        s.duration = dur
        s.attributableEffectsSubstance = atribuible
        s.disturbanceClinicallySignificant = clinico
        return s

    def crear_evento(paciente, nro, etiqueta, traumatico=True):
        """Crea un evento y lo asocia al paciente."""
        sufijo = "T" if traumatico else "NT"
        nombre = f"Event_P{nro}_{etiqueta}_{sufijo}"
        if traumatico:
            ev = TraumaticEvent(nombre)
            ev.TraumaticEventProperty = True
        else:
            ev = NonTraumaticEvent(nombre)
            ev.TraumaticEventProperty = False
        hasEvent[paciente].append(ev)
        return ev

    def crear_paciente_completo(nro, etiqueta,
                                n_intrusion=1, n_avoidance=1,
                                n_affective=2, n_threat=2,
                                dur=2, clinico=True, atribuible=False,
                                traumatico=True,
                                dissociative_cls=None,
                                self_org_cls=None):
        """
        Crea un paciente con síntomas y evento según los parámetros dados.

        Criterios DSM-5 mapeados:
          A  → traumático (tipo de evento)
          B  → n_intrusion ≥ 1
          C  → n_avoidance ≥ 1
          D  → n_affective ≥ 2
          E  → n_threat ≥ 2
          F  → dur > 0  (duración en meses)
          G  → clinico = True
          H  → atribuible = False  (NO atribuible a sustancias)

        Criterios CIE-11 mapeados:
          1  → traumático (tipo de evento)
          2  → n_intrusion ≥ 1
          3  → n_avoidance ≥ 1
          4  → n_threat ≥ 2
          5  → dur > 0 para todos los síntomas
          6  → clinico = True para todos los síntomas

        Diferencias clave DSM-5 vs CIE-11:
          - DSM-5 D requiere min 2 AffectiveCognitiveAlteration (CIE-11 no)
          - DSM-5 H requiere attributableEffectsSubstance=False (CIE-11 no)
          - CIE-11 5 y 6 aplican a los 4 tipos de síntomas incluyendo
            AffectiveCognitiveAlteration (solo existencial, no min 2)
        """
        nombre = f"Patient{nro}_{etiqueta}"
        p = Patient(nombre)

        # Crear evento
        crear_evento(p, nro, etiqueta, traumatico=traumatico)

        # Crear síntomas
        idx = 0
        for _ in range(n_intrusion):
            idx += 1
            s = crear_sintoma(IntrusionSymptom, f"P{nro}", idx,
                              dur, atribuible, clinico)
            hasSymptom[p].append(s)

        for _ in range(n_avoidance):
            idx += 1
            s = crear_sintoma(AvoidanceSymptom, f"P{nro}", idx,
                              dur, atribuible, clinico)
            hasSymptom[p].append(s)

        for _ in range(n_affective):
            idx += 1
            s = crear_sintoma(AffectiveCognitiveAlteration, f"P{nro}", idx,
                              dur, atribuible, clinico)
            hasSymptom[p].append(s)

        for _ in range(n_threat):
            idx += 1
            s = crear_sintoma(ThreatArousalSymptom, f"P{nro}", idx,
                              dur, atribuible, clinico)
            hasSymptom[p].append(s)

        # Síntoma disociativo (opcional)
        if dissociative_cls is not None:
            idx += 1
            s_dis = crear_sintoma(dissociative_cls, f"P{nro}", idx,
                                  dur, atribuible, clinico)
            hasSymptom[p].append(s_dis)

        # Alteración en la autoorganización (opcional)
        if self_org_cls is not None:
            idx += 1
            s_sod = crear_sintoma(self_org_cls, f"P{nro}", idx,
                                  dur, atribuible, clinico)
            hasSymptom[p].append(s_sod)

        total_sintomas = (n_intrusion + n_avoidance + n_affective + n_threat
                          + (1 if dissociative_cls else 0)
                          + (1 if self_org_cls else 0))
        ev_tipo = "traumático" if traumatico else "no traumático"
        dis_txt = (f", disociativo: {dissociative_cls.__name__}"
                   if dissociative_cls else "")
        sod_txt = (f", autoorg: {self_org_cls.__name__}"
                   if self_org_cls else "")
        print(f"  {nombre} — {total_sintomas} síntomas, "
              f"evento {ev_tipo}, dur={dur}, G={clinico}, "
              f"H(atrib)={atribuible}{dis_txt}{sod_txt}")

        return p

    # ═════════════════════════════════════════════════════════════
    # GRUPO 1: Cumplen TODOS los criterios DSM-5 (A-H, sin disociativo)
    #   Esperado tras razonar:
    #     → Patient_meetsPTSD_DSM5:  SÍ
    #     → Patient_meetsPTSD_ICD11: SÍ (interoperabilidad DSM→CIE)
    # ═════════════════════════════════════════════════════════════
    print(f"\n{'─'*70}")
    print(f"GRUPO 1: {x_cumple} pacientes que cumplen TODOS los criterios"
          f" DSM-5 (A-H)")
    print(f"  Esperado: Patient_meetsPTSD_DSM5 = SÍ")
    print(f"  Esperado: Patient_meetsPTSD_ICD11 = SÍ (interoperabilidad)")
    print(f"{'─'*70}")
    pacientes_g1 = []
    for _ in range(x_cumple):
        nro = siguiente()
        p = crear_paciente_completo(
            nro, "DSM5_cumple_AH",
            n_intrusion=1, n_avoidance=1,
            n_affective=2, n_threat=2,
            dur=2, clinico=True, atribuible=False,
            traumatico=True
        )
        pacientes_g1.append(p)

    # ═════════════════════════════════════════════════════════════
    # GRUPO 2: Fallan exactamente un criterio DSM-5 cada uno
    #   Esperado: NO clasifican en Patient_meetsPTSD_DSM5
    # ═════════════════════════════════════════════════════════════
    print(f"\n{'─'*70}")
    print("GRUPO 2: Pacientes que fallan exactamente un criterio DSM-5")
    print(f"  Esperado: Patient_meetsPTSD_DSM5 = NO")
    print(f"{'─'*70}")
    pacientes_g2 = []

    # 2a) No cumple A: evento NO traumático
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_A",
        n_intrusion=1, n_avoidance=1,
        n_affective=2, n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=False  # ← falla A
    )
    pacientes_g2.append(("A", p))

    # 2b) No cumple B: 0 síntomas intrusivos
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_B",
        n_intrusion=0,  # ← falla B
        n_avoidance=1,
        n_affective=2, n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g2.append(("B", p))

    # 2c) No cumple C: 0 síntomas de evitación
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_C",
        n_intrusion=1,
        n_avoidance=0,  # ← falla C
        n_affective=2, n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g2.append(("C", p))

    # 2d) No cumple D (0 síntomas): 0 AffectiveCognitiveAlteration
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_D_zero",
        n_intrusion=1, n_avoidance=1,
        n_affective=0,  # ← falla D (0 de 2 requeridos)
        n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g2.append(("D_zero", p))

    # 2e) No cumple D (parcial): solo 1 AffectiveCognitiveAlteration
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_D_partial",
        n_intrusion=1, n_avoidance=1,
        n_affective=1,  # ← falla D (1 de 2 requeridos)
        n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g2.append(("D_partial", p))

    # 2f) No cumple E (0 síntomas): 0 ThreatArousalSymptom
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_E_zero",
        n_intrusion=1, n_avoidance=1,
        n_affective=2,
        n_threat=0,  # ← falla E (0 de 2 requeridos)
        dur=2, clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g2.append(("E_zero", p))

    # 2g) No cumple E (parcial): solo 1 ThreatArousalSymptom
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_E_partial",
        n_intrusion=1, n_avoidance=1,
        n_affective=2,
        n_threat=1,  # ← falla E (1 de 2 requeridos)
        dur=2, clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g2.append(("E_partial", p))

    # 2h) No cumple F: duration = 0
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_F",
        n_intrusion=1, n_avoidance=1,
        n_affective=2, n_threat=2,
        dur=0,  # ← falla F
        clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g2.append(("F", p))

    # 2i) No cumple G: disturbanceClinicallySignificant = False
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_G",
        n_intrusion=1, n_avoidance=1,
        n_affective=2, n_threat=2,
        dur=2,
        clinico=False,  # ← falla G
        atribuible=False,
        traumatico=True
    )
    pacientes_g2.append(("G", p))

    # 2j) No cumple H: attributableEffectsSubstance = True
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_noMeets_H",
        n_intrusion=1, n_avoidance=1,
        n_affective=2, n_threat=2,
        dur=2, clinico=True,
        atribuible=True,  # ← falla H (SÍ atribuible a sustancias)
        traumatico=True
    )
    pacientes_g2.append(("H", p))

    # ═════════════════════════════════════════════════════════════
    # GRUPO 3: Subtipo disociativo DSM-5 (cumplen A-H + disociativo)
    #   Esperado:
    #     → Patient_meetsPTSD_WithDissociative_DSM5: SÍ
    #     → Patient_meetsPTSD_DSM5: NO (disjunto con WithDissociative)
    #     → Patient_meetsPTSD_ICD11: SÍ
    # ═════════════════════════════════════════════════════════════
    print(f"\n{'─'*70}")
    print("GRUPO 3: Pacientes con subtipo disociativo DSM-5")
    print(f"  Esperado: Patient_meetsPTSD_WithDissociative_DSM5 = SÍ")
    print(f"  Esperado: Patient_meetsPTSD_DSM5 = NO (disjuntos)")
    print(f"  Esperado: Patient_meetsPTSD_ICD11 = SÍ")
    print(f"{'─'*70}")
    pacientes_g3 = []

    # Despersonalización
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_dissociative_depersonalization",
        n_intrusion=1, n_avoidance=1,
        n_affective=2, n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=True,
        dissociative_cls=DepersonalizationSymptom
    )
    pacientes_g3.append(p)

    # Desrealización
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "DSM5_dissociative_derealization",
        n_intrusion=1, n_avoidance=1,
        n_affective=2, n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=True,
        dissociative_cls=DerealizationSymptom
    )
    pacientes_g3.append(p)

    # ═════════════════════════════════════════════════════════════
    # GRUPO 4: Cumplen A-H + SelfOrganizationDisturbance
    #   Esperado:
    #     → Patient_meetsPTSD_DSM5: SÍ (sin disociativo)
    #     → Patient_meetsPTSD_ICD11: SÍ
    #     → Patient_meetsPTSD_Complex_ICD11: SÍ
    # ═════════════════════════════════════════════════════════════
    print(f"\n{'─'*70}")
    print("GRUPO 4: Paciente con SelfOrganizationDisturbance (TEPT complejo)")
    print(f"  Esperado: Patient_meetsPTSD_DSM5 = SÍ")
    print(f"  Esperado: Patient_meetsPTSD_ICD11 = SÍ")
    print(f"  Esperado: Patient_meetsPTSD_Complex_ICD11 = SÍ")
    print(f"{'─'*70}")
    pacientes_g4 = []

    nro = siguiente()
    p = crear_paciente_completo(
        nro, "ICD11_complex_selfOrg",
        n_intrusion=1, n_avoidance=1,
        n_affective=2, n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=True,
        self_org_cls=SelfOrganizationDisturbance
    )
    pacientes_g4.append(p)

    # ═════════════════════════════════════════════════════════════
    # GRUPO 5: INTEROPERABILIDAD — CIE-11 SÍ, DSM-5 NO
    #   Pacientes que cumplen CIE-11 criterios 1-6 pero NO DSM-5
    #   porque solo tienen 1 AffectiveCognitiveAlteration (falla D).
    #
    #   Diferencia clave: CIE-11 criterios 5 y 6 requieren
    #   existencial (some) de AffectiveCognitiveAlteration, pero
    #   DSM-5 D requiere min 2. Con solo 1, CIE-11 se cumple,
    #   DSM-5 no.
    #
    #   Esperado:
    #     → Patient_meetsPTSD_ICD11: SÍ
    #     → Patient_meetsPTSD_DSM5: NO (falla D)
    # ═════════════════════════════════════════════════════════════
    print(f"\n{'─'*70}")
    print("GRUPO 5: INTEROPERABILIDAD — CIE-11 SÍ, DSM-5 NO (falla D)")
    print(f"  Solo 1 AffectiveCognitiveAlteration → cumple CIE-11 pero "
          f"no DSM-5 D")
    print(f"  Esperado: Patient_meetsPTSD_ICD11 = SÍ")
    print(f"  Esperado: Patient_meetsPTSD_DSM5 = NO")
    print(f"{'─'*70}")
    pacientes_g5 = []

    for i in range(2):
        nro = siguiente()
        p = crear_paciente_completo(
            nro, f"INTEROP_ICD11_OK_DSM5_NO_failD_{i+1}",
            n_intrusion=1, n_avoidance=1,
            n_affective=1,  # ← solo 1, CIE-11 OK, DSM-5 D falla
            n_threat=2,
            dur=2, clinico=True, atribuible=False,
            traumatico=True
        )
        pacientes_g5.append(p)

    # ═════════════════════════════════════════════════════════════
    # GRUPO 6: INTEROPERABILIDAD — CIE-11 SÍ, DSM-5 NO (falla H)
    #   Pacientes que cumplen CIE-11 1-6 pero NO DSM-5 porque
    #   attributableEffectsSubstance=True (falla H de DSM-5).
    #   CIE-11 no tiene criterio de exclusión por sustancias.
    #
    #   Esperado:
    #     → Patient_meetsPTSD_ICD11: SÍ
    #     → Patient_meetsPTSD_DSM5: NO (falla H)
    # ═════════════════════════════════════════════════════════════
    print(f"\n{'─'*70}")
    print("GRUPO 6: INTEROPERABILIDAD — CIE-11 SÍ, DSM-5 NO (falla H)")
    print(f"  attributableEffectsSubstance=True → CIE-11 OK, DSM-5 H falla")
    print(f"  Esperado: Patient_meetsPTSD_ICD11 = SÍ")
    print(f"  Esperado: Patient_meetsPTSD_DSM5 = NO")
    print(f"{'─'*70}")
    pacientes_g6 = []

    for i in range(2):
        nro = siguiente()
        p = crear_paciente_completo(
            nro, f"INTEROP_ICD11_OK_DSM5_NO_failH_{i+1}",
            n_intrusion=1, n_avoidance=1,
            n_affective=2, n_threat=2,
            dur=2, clinico=True,
            atribuible=True,  # ← CIE-11 no controla esto, DSM-5 H falla
            traumatico=True
        )
        pacientes_g6.append(p)

    # ═════════════════════════════════════════════════════════════
    # GRUPO 9: Fallan exactamente un criterio CIE-11 cada uno
    #   Esperado: NO clasifican en Patient_meetsPTSD_ICD11
    # ═════════════════════════════════════════════════════════════
    print(f"\n{'─'*70}")
    print("GRUPO 9: Pacientes que fallan exactamente un criterio CIE-11")
    print(f"  Esperado: Patient_meetsPTSD_ICD11 = NO")
    print(f"{'─'*70}")
    pacientes_g9 = []

    # 9a) No cumple 1: evento NO traumático
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "ICD11_noMeets_1",
        n_intrusion=1, n_avoidance=1,
        n_affective=1, n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=False  # ← falla criterio 1
    )
    pacientes_g9.append(("1", p))

    # 9b) No cumple 2: 0 síntomas intrusivos
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "ICD11_noMeets_2",
        n_intrusion=0,  # ← falla criterio 2
        n_avoidance=1,
        n_affective=1, n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g9.append(("2", p))

    # 9c) No cumple 3: 0 síntomas de evitación
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "ICD11_noMeets_3",
        n_intrusion=1,
        n_avoidance=0,  # ← falla criterio 3
        n_affective=1, n_threat=2,
        dur=2, clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g9.append(("3", p))

    # 9d) No cumple 4: solo 1 ThreatArousalSymptom (requiere min 2)
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "ICD11_noMeets_4",
        n_intrusion=1, n_avoidance=1,
        n_affective=1,
        n_threat=1,  # ← falla criterio 4 (1 de 2 requeridos)
        dur=2, clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g9.append(("4", p))

    # 9e) No cumple 5: duration = 0
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "ICD11_noMeets_5",
        n_intrusion=1, n_avoidance=1,
        n_affective=1, n_threat=2,
        dur=0,  # ← falla criterio 5
        clinico=True, atribuible=False,
        traumatico=True
    )
    pacientes_g9.append(("5", p))

    # 9f) No cumple 6: disturbanceClinicallySignificant = False
    nro = siguiente()
    p = crear_paciente_completo(
        nro, "ICD11_noMeets_6",
        n_intrusion=1, n_avoidance=1,
        n_affective=1, n_threat=2,
        dur=2,
        clinico=False,  # ← falla criterio 6
        atribuible=False,
        traumatico=True
    )
    pacientes_g9.append(("6", p))

    # ─────────────────────────────────────────────────────────────
    # GUARDAR ONTOLOGÍA CONSISTENTE (sin inconsistencias)
    # ─────────────────────────────────────────────────────────────
    total_individuos = len(list(onto.individuals()))
    nombre_consistente = archivo_ontologia.replace(".rdf", "_PobladaFull.rdf")
    ruta_consistente = os.path.join(ruta_ontologia, nombre_consistente)
    onto.save(file=ruta_consistente, format="rdfxml")
    print(f"\n{'='*70}")
    print(f"Ontología CONSISTENTE guardada: {ruta_consistente}")
    print(f"Total individuos: {total_individuos}")
    print(f"{'='*70}")

    # ═════════════════════════════════════════════════════════════
    # GRUPOS 7 y 8: INCONSISTENCIAS FORZADAS
    # Se guardan en un archivo SEPARADO para poder probarse sin
    # afectar la ontología consistente.
    # ═════════════════════════════════════════════════════════════
    if incluir_inconsistencias:
        print(f"\n{'='*70}")
        print("CREANDO INSTANCIAS INCONSISTENTES (archivo separado)")
        print(f"{'='*70}")

        # Cargar ontología fresca para inconsistencias
        onto_incons = get_ontology(ruta_completa).load()

        with onto_incons:
            # Re-obtener referencias en el nuevo mundo
            Patient_i = onto_incons.Patient
            TraumaticEvent_i = onto_incons.TraumaticEvent
            NonTraumaticEvent_i = onto_incons.NonTraumaticEvent
            IntrusionSymptom_i = onto_incons.IntrusionSymptom
            AvoidanceSymptom_i = onto_incons.AvoidanceSymptom
            AffectiveCogAlt_i = onto_incons.AffectiveCognitiveAlteration
            ThreatArousal_i = onto_incons.ThreatArousalSymptom
            hasSymptom_i = onto_incons.hasSymptom
            hasEvent_i = onto_incons.hasEvent
            Patient_meetsPTSD_DSM5_i = onto_incons.Patient_meetsPTSD_DSM5
            Patient_meetsPTSD_ICD11_i = onto_incons.Patient_meetsPTSD_ICD11

            def crear_sintoma_i(cls_s, id_pac, num, dur, atrib, clin):
                nombre = f"Symptom_{id_pac}_{cls_s.__name__}_{num}"
                s = cls_s(nombre)
                s.duration = dur
                s.attributableEffectsSubstance = atrib
                s.disturbanceClinicallySignificant = clin
                return s

            def crear_evento_i(paciente, nro, etiqueta, traumatico=True):
                sufijo = "T" if traumatico else "NT"
                nombre = f"Event_P{nro}_{etiqueta}_{sufijo}"
                if traumatico:
                    ev = TraumaticEvent_i(nombre)
                    ev.TraumaticEventProperty = True
                else:
                    ev = NonTraumaticEvent_i(nombre)
                    ev.TraumaticEventProperty = False
                hasEvent_i[paciente].append(ev)
                return ev

            # ─────────────────────────────────────────────────────
            # GRUPO 7: INCONSISTENCIAS DSM-5
            # Pacientes que NO cumplen un criterio pero se fuerzan
            # como miembros de Patient_meetsPTSD_DSM5
            # → El razonador DEBE detectar inconsistencia
            # ─────────────────────────────────────────────────────
            print(f"\n{'─'*70}")
            print("GRUPO 7: INCONSISTENCIAS DSM-5 (forzadas)")
            print(f"{'─'*70}")

            # 7a) Cumple B-H pero NO A (evento no traumático)
            #     Forzado en Patient_meetsPTSD_DSM5
            print("  7a: B-H sin A, forzado como TEPT DSM-5")
            p_incons_dsm_a = Patient_i("PatientINCONS_DSM5_noA")
            crear_evento_i(p_incons_dsm_a, "I1", "INCONS_DSM5_noA",
                           traumatico=False)  # ← NO traumático
            idx = 0
            for cls_s in [IntrusionSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI1", idx, 2, False, True)
                hasSymptom_i[p_incons_dsm_a].append(s)
            for cls_s in [AvoidanceSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI1", idx, 2, False, True)
                hasSymptom_i[p_incons_dsm_a].append(s)
            for _ in range(2):
                idx += 1
                s = crear_sintoma_i(AffectiveCogAlt_i, "PI1", idx,
                                    2, False, True)
                hasSymptom_i[p_incons_dsm_a].append(s)
            for _ in range(2):
                idx += 1
                s = crear_sintoma_i(ThreatArousal_i, "PI1", idx,
                                    2, False, True)
                hasSymptom_i[p_incons_dsm_a].append(s)
            # FORZAR clasificación incorrecta
            p_incons_dsm_a.is_a.append(Patient_meetsPTSD_DSM5_i)

            # 7b) Cumple A,C-H pero NO B (sin intrusión)
            #     Forzado en Patient_meetsPTSD_DSM5
            print("  7b: A,C-H sin B, forzado como TEPT DSM-5")
            p_incons_dsm_b = Patient_i("PatientINCONS_DSM5_noB")
            crear_evento_i(p_incons_dsm_b, "I2", "INCONS_DSM5_noB",
                           traumatico=True)
            idx = 0
            # Sin IntrusionSymptom
            for cls_s in [AvoidanceSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI2", idx, 2, False, True)
                hasSymptom_i[p_incons_dsm_b].append(s)
            for _ in range(2):
                idx += 1
                s = crear_sintoma_i(AffectiveCogAlt_i, "PI2", idx,
                                    2, False, True)
                hasSymptom_i[p_incons_dsm_b].append(s)
            for _ in range(2):
                idx += 1
                s = crear_sintoma_i(ThreatArousal_i, "PI2", idx,
                                    2, False, True)
                hasSymptom_i[p_incons_dsm_b].append(s)
            p_incons_dsm_b.is_a.append(Patient_meetsPTSD_DSM5_i)

            # 7c) Cumple A-G pero NO H (atribuible a sustancias)
            #     Forzado en Patient_meetsPTSD_DSM5
            print("  7c: A-G sin H, forzado como TEPT DSM-5")
            p_incons_dsm_h = Patient_i("PatientINCONS_DSM5_noH")
            crear_evento_i(p_incons_dsm_h, "I3", "INCONS_DSM5_noH",
                           traumatico=True)
            idx = 0
            for cls_s in [IntrusionSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI3", idx, 2, True, True)
                # ← atribuible=True → falla H
                hasSymptom_i[p_incons_dsm_h].append(s)
            for cls_s in [AvoidanceSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI3", idx, 2, True, True)
                hasSymptom_i[p_incons_dsm_h].append(s)
            for _ in range(2):
                idx += 1
                s = crear_sintoma_i(AffectiveCogAlt_i, "PI3", idx,
                                    2, True, True)
                hasSymptom_i[p_incons_dsm_h].append(s)
            for _ in range(2):
                idx += 1
                s = crear_sintoma_i(ThreatArousal_i, "PI3", idx,
                                    2, True, True)
                hasSymptom_i[p_incons_dsm_h].append(s)
            p_incons_dsm_h.is_a.append(Patient_meetsPTSD_DSM5_i)

            # ─────────────────────────────────────────────────────
            # GRUPO 8: INCONSISTENCIAS CIE-11
            # Pacientes que NO cumplen un criterio CIE-11 pero se
            # fuerzan como miembros de Patient_meetsPTSD_ICD11
            # → El razonador DEBE detectar inconsistencia
            # ─────────────────────────────────────────────────────
            print(f"\n{'─'*70}")
            print("GRUPO 8: INCONSISTENCIAS CIE-11 (forzadas)")
            print(f"{'─'*70}")

            # 8a) Cumple 2-6 pero NO 1 (evento no traumático)
            #     Forzado en Patient_meetsPTSD_ICD11
            print("  8a: Criterios 2-6 sin 1, forzado como TEPT CIE-11")
            p_incons_icd_1 = Patient_i("PatientINCONS_ICD11_no1")
            crear_evento_i(p_incons_icd_1, "I4", "INCONS_ICD11_no1",
                           traumatico=False)  # ← falla criterio 1
            idx = 0
            for cls_s in [IntrusionSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI4", idx, 2, False, True)
                hasSymptom_i[p_incons_icd_1].append(s)
            for cls_s in [AvoidanceSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI4", idx, 2, False, True)
                hasSymptom_i[p_incons_icd_1].append(s)
            for _ in range(1):
                idx += 1
                s = crear_sintoma_i(AffectiveCogAlt_i, "PI4", idx,
                                    2, False, True)
                hasSymptom_i[p_incons_icd_1].append(s)
            for _ in range(2):
                idx += 1
                s = crear_sintoma_i(ThreatArousal_i, "PI4", idx,
                                    2, False, True)
                hasSymptom_i[p_incons_icd_1].append(s)
            p_incons_icd_1.is_a.append(Patient_meetsPTSD_ICD11_i)

            # 8b) Cumple 1,3-6 pero NO 2 (sin intrusión)
            #     Forzado en Patient_meetsPTSD_ICD11
            print("  8b: Criterios 1,3-6 sin 2, forzado como TEPT CIE-11")
            p_incons_icd_2 = Patient_i("PatientINCONS_ICD11_no2")
            crear_evento_i(p_incons_icd_2, "I5", "INCONS_ICD11_no2",
                           traumatico=True)
            idx = 0
            # Sin IntrusionSymptom
            for cls_s in [AvoidanceSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI5", idx, 2, False, True)
                hasSymptom_i[p_incons_icd_2].append(s)
            for _ in range(1):
                idx += 1
                s = crear_sintoma_i(AffectiveCogAlt_i, "PI5", idx,
                                    2, False, True)
                hasSymptom_i[p_incons_icd_2].append(s)
            for _ in range(2):
                idx += 1
                s = crear_sintoma_i(ThreatArousal_i, "PI5", idx,
                                    2, False, True)
                hasSymptom_i[p_incons_icd_2].append(s)
            p_incons_icd_2.is_a.append(Patient_meetsPTSD_ICD11_i)

            # 8c) Cumple 1-3,5-6 pero NO 4 (solo 1 ThreatArousal)
            #     Forzado en Patient_meetsPTSD_ICD11
            print("  8c: Criterios 1-3,5-6 sin 4, forzado como TEPT CIE-11")
            p_incons_icd_4 = Patient_i("PatientINCONS_ICD11_no4")
            crear_evento_i(p_incons_icd_4, "I6", "INCONS_ICD11_no4",
                           traumatico=True)
            idx = 0
            for cls_s in [IntrusionSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI6", idx, 2, False, True)
                hasSymptom_i[p_incons_icd_4].append(s)
            for cls_s in [AvoidanceSymptom_i]:
                idx += 1
                s = crear_sintoma_i(cls_s, "PI6", idx, 2, False, True)
                hasSymptom_i[p_incons_icd_4].append(s)
            for _ in range(1):
                idx += 1
                s = crear_sintoma_i(AffectiveCogAlt_i, "PI6", idx,
                                    2, False, True)
                hasSymptom_i[p_incons_icd_4].append(s)
            # Solo 1 ThreatArousal → falla criterio 4 (requiere min 2)
            idx += 1
            s = crear_sintoma_i(ThreatArousal_i, "PI6", idx, 2, False, True)
            hasSymptom_i[p_incons_icd_4].append(s)
            p_incons_icd_4.is_a.append(Patient_meetsPTSD_ICD11_i)

        # Guardar ontología con inconsistencias
        nombre_incons = archivo_ontologia.replace(
            ".rdf", "_PobladaIncons.rdf")
        ruta_incons = os.path.join(ruta_ontologia, nombre_incons)
        onto_incons.save(file=ruta_incons, format="rdfxml")
        print(f"\n{'='*70}")
        print(f"Ontología INCONSISTENTE guardada: {ruta_incons}")
        print(f"  ⚠ El razonador (HermiT/Pellet) DEBE reportar "
              f"inconsistencia en este archivo.")
        print(f"{'='*70}")

    # ─────────────────────────────────────────────────────────────
    # CONSULTAS DE VERIFICACIÓN
    # ─────────────────────────────────────────────────────────────
    if ejecutar_consultas:
        print(f"\n{'='*70}")
        print("CONSULTAS DE VERIFICACIÓN (pre-razonamiento)")
        print(f"{'='*70}")
        ejecutar_consultas_verificacion(onto, ruta_consistente)

    # ─────────────────────────────────────────────────────────────
    # RESUMEN FINAL
    # ─────────────────────────────────────────────────────────────
    n_g1 = x_cumple
    n_g2 = 10
    n_g3 = 2
    n_g4 = 1
    n_g5 = 2
    n_g6 = 2
    n_g9 = 6
    total = n_g1 + n_g2 + n_g3 + n_g4 + n_g5 + n_g6 + n_g9

    print(f"\n{'='*70}")
    print("RESUMEN DE PACIENTES CREADOS")
    print(f"{'='*70}")
    print(f"  GRUPO 1 │ DSM-5 A-H completo (→ TEPT DSM-5 + CIE-11): {n_g1}")
    print(f"  GRUPO 2 │ Fallan 1 criterio DSM-5 (→ NO TEPT DSM-5):   {n_g2}")
    print(f"  GRUPO 3 │ Subtipo disociativo DSM-5:                    {n_g3}")
    print(f"  GRUPO 4 │ TEPT complejo (SelfOrganizationDisturbance):  {n_g4}")
    print(f"  GRUPO 5 │ INTEROP: CIE-11 SÍ, DSM-5 NO (falla D):     {n_g5}")
    print(f"  GRUPO 6 │ INTEROP: CIE-11 SÍ, DSM-5 NO (falla H):     {n_g6}")
    print(f"  GRUPO 9 │ Fallan 1 criterio CIE-11 (→ NO TEPT CIE-11): {n_g9}")
    print(f"  {'─'*60}")
    print(f"  TOTAL pacientes en ontología consistente:               {total}")
    if incluir_inconsistencias:
        print(f"\n  GRUPO 7 │ Inconsistencias DSM-5 (archivo separado):    3")
        print(f"  GRUPO 8 │ Inconsistencias CIE-11 (archivo separado):   3")
    print(f"\n  Total individuos en ontología: {total_individuos}")

    return onto


def ejecutar_consultas_verificacion(onto, ruta_onto_guardada):
    """
    Ejecuta consultas para verificar la estructura de los datos creados.

    NOTA: Para verificar INFERENCIAS (clasificación automática), se debe
    ejecutar el razonador (HermiT o Pellet) en Protégé o con sync_reasoner().

    Las consultas aquí son PRE-razonamiento. Las consultas POST-razonamiento
    se listan como referencia para ejecutarlas en Protégé (SPARQL/DL Query).
    """

    print("\n" + "─" * 70)
    print("CONSULTAS PRE-RAZONAMIENTO (owlready2)")
    print("─" * 70)

    # ── Q1: Pacientes con evento traumático ──
    print("\n▶ Q1: Pacientes con al menos un evento traumático (hasEvent)")
    q1 = list(onto.search(type=onto.Patient, hasEvent=onto.search(
        type=onto.TraumaticEvent)))
    # Alternativa más robusta:
    pacientes_trauma = []
    for p in onto.search(type=onto.Patient):
        eventos = p.hasEvent if hasattr(p, 'hasEvent') else []
        for ev in eventos:
            if isinstance(ev, onto.TraumaticEvent):
                pacientes_trauma.append(p)
                break
    print(f"  Encontrados: {len(pacientes_trauma)}")
    for p in pacientes_trauma[:5]:
        print(f"    - {p.name}")
    if len(pacientes_trauma) > 5:
        print(f"    ... y {len(pacientes_trauma)-5} más")

    # ── Q2: Pacientes con evento NO traumático ──
    print("\n▶ Q2: Pacientes con evento NO traumático")
    pacientes_no_trauma = []
    for p in onto.search(type=onto.Patient):
        eventos = p.hasEvent if hasattr(p, 'hasEvent') else []
        for ev in eventos:
            if isinstance(ev, onto.NonTraumaticEvent):
                pacientes_no_trauma.append(p)
                break
    print(f"  Encontrados: {len(pacientes_no_trauma)}")
    for p in pacientes_no_trauma:
        print(f"    - {p.name}")

    # ── Q3: Contar síntomas por tipo por paciente ──
    print("\n▶ Q3: Distribución de síntomas por paciente (primeros 10)")
    for i, p in enumerate(onto.search(type=onto.Patient)[:10]):
        sintomas = p.hasSymptom if hasattr(p, 'hasSymptom') else []
        n_intr = sum(1 for s in sintomas
                     if isinstance(s, onto.IntrusionSymptom))
        n_avoid = sum(1 for s in sintomas
                      if isinstance(s, onto.AvoidanceSymptom))
        n_aff = sum(1 for s in sintomas
                    if isinstance(s, onto.AffectiveCognitiveAlteration))
        n_threat = sum(1 for s in sintomas
                       if isinstance(s, onto.ThreatArousalSymptom))
        print(f"  {p.name}: "
              f"B(intr)={n_intr}, C(avoid)={n_avoid}, "
              f"D(affect)={n_aff}, E(threat)={n_threat}")

    # ── Q4: Pacientes que parecen cumplir DSM-5 D (min 2 AffCog) ──
    print("\n▶ Q4: Pacientes con ≥2 AffectiveCognitiveAlteration "
          "(pre-requisito DSM-5 D)")
    pac_d = []
    for p in onto.search(type=onto.Patient):
        sintomas = p.hasSymptom if hasattr(p, 'hasSymptom') else []
        n_aff = sum(1 for s in sintomas
                    if isinstance(s, onto.AffectiveCognitiveAlteration))
        if n_aff >= 2:
            pac_d.append((p, n_aff))
    print(f"  Encontrados: {len(pac_d)}")

    # ── Q5: Verificar interoperabilidad potencial ──
    print("\n▶ Q5: Pacientes candidatos a interoperabilidad "
          "(CIE-11 SÍ, DSM-5 NO)")
    for p in onto.search(type=onto.Patient):
        if "INTEROP" in p.name:
            sintomas = p.hasSymptom if hasattr(p, 'hasSymptom') else []
            n_aff = sum(1 for s in sintomas
                        if isinstance(s, onto.AffectiveCognitiveAlteration))
            atrib = any(
                getattr(s, 'attributableEffectsSubstance', False)
                for s in sintomas
            )
            print(f"  {p.name}: "
                  f"n_AffCog={n_aff}, hay_atribuible={atrib}")

    # ── CONSULTAS PARA PROTÉGÉ (referencia) ──
    print(f"\n{'═'*70}")
    print("CONSULTAS POST-RAZONAMIENTO (ejecutar en Protégé)")
    print(f"{'═'*70}")

    consultas_protege = """
╔══════════════════════════════════════════════════════════════════════╗
║  INSTRUCCIONES PARA PROTÉGÉ                                        ║
║  1. Abrir la ontología _PobladaFull.rdf en Protégé                 ║
║  2. Ejecutar razonador (Reasoner → HermiT o Pellet → Start)       ║
║  3. Ir a la pestaña "DL Query" o "SPARQL Query"                   ║
║  4. Ejecutar las siguientes consultas:                              ║
╚══════════════════════════════════════════════════════════════════════╝

────────────────────────────────────────────────────────────────────────
DL QUERY 1: Pacientes clasificados como TEPT según DSM-5
────────────────────────────────────────────────────────────────────────
  Patient_meetsPTSD_DSM5

  Esperado: Deben aparecer los pacientes del GRUPO 1 (DSM5_cumple_AH)
  y el GRUPO 4 (ICD11_complex_selfOrg, porque cumple A-H sin disociativo).
  NO deben aparecer pacientes del GRUPO 2, 5, 6.

────────────────────────────────────────────────────────────────────────
DL QUERY 2: Pacientes clasificados como TEPT según CIE-11
────────────────────────────────────────────────────────────────────────
  Patient_meetsPTSD_ICD11

  Esperado: Deben aparecer GRUPO 1, GRUPO 3, GRUPO 4, GRUPO 5, GRUPO 6.
  NO deben aparecer pacientes del GRUPO 9.

────────────────────────────────────────────────────────────────────────
DL QUERY 3: Pacientes con subtipo disociativo DSM-5
────────────────────────────────────────────────────────────────────────
  Patient_meetsPTSD_WithDissociative_DSM5

  Esperado: GRUPO 3 (dissociative_depersonalization y derealization).

────────────────────────────────────────────────────────────────────────
DL QUERY 4: Pacientes con TEPT Complejo CIE-11
────────────────────────────────────────────────────────────────────────
  Patient_meetsPTSD_Complex_ICD11

  Esperado: GRUPO 4 (ICD11_complex_selfOrg).

────────────────────────────────────────────────────────────────────────
DL QUERY 5: INTEROPERABILIDAD DSM-5 → CIE-11
  Pacientes que son TEPT DSM-5 Y TAMBIÉN TEPT CIE-11
────────────────────────────────────────────────────────────────────────
  Patient_meetsPTSD_DSM5 and Patient_meetsPTSD_ICD11

  Esperado: TODOS los del GRUPO 1, GRUPO 4.
  Esto demuestra que DSM-5 → CIE-11 (inclusión).

────────────────────────────────────────────────────────────────────────
DL QUERY 6: INTEROPERABILIDAD CIE-11 ↛ DSM-5
  Pacientes que son TEPT CIE-11 PERO NO TEPT DSM-5
────────────────────────────────────────────────────────────────────────
  Patient_meetsPTSD_ICD11 and not Patient_meetsPTSD_DSM5
      and not Patient_meetsPTSD_WithDissociative_DSM5

  Esperado: GRUPO 5 y GRUPO 6.
  Esto demuestra que CIE-11 ↛ DSM-5 (NO inclusión inversa).

────────────────────────────────────────────────────────────────────────
DL QUERY 7: Pacientes que cumplen criterios individuales DSM-5
────────────────────────────────────────────────────────────────────────
  Patient_meetsDSM5_A
  Patient_meetsDSM5_B
  Patient_meetsDSM5_C
  Patient_meetsDSM5_D
  Patient_meetsDSM5_E
  Patient_meetsDSM5_F
  Patient_meetsDSM5_G
  Patient_meetsDSM5_H

  Verificar individualmente qué pacientes cumplen cada criterio.

────────────────────────────────────────────────────────────────────────
DL QUERY 8: Pacientes que cumplen criterios individuales CIE-11
────────────────────────────────────────────────────────────────────────
  Patient_meetsICD11_1
  Patient_meetsICD11_2
  Patient_meetsICD11_3
  Patient_meetsICD11_4
  Patient_meetsICD11_5
  Patient_meetsICD11_6

  Verificar individualmente cómo difiere de DSM-5.

────────────────────────────────────────────────────────────────────────
SPARQL 1: Pacientes TEPT DSM-5 que también son TEPT CIE-11
────────────────────────────────────────────────────────────────────────
PREFIX ont: <http://www.semanticweb.org/ontologies/onTEPT#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?paciente WHERE {
  ?paciente rdf:type ont:Patient_meetsPTSD_DSM5 .
  ?paciente rdf:type ont:Patient_meetsPTSD_ICD11 .
}

────────────────────────────────────────────────────────────────────────
SPARQL 2: Pacientes TEPT CIE-11 que NO son TEPT DSM-5
────────────────────────────────────────────────────────────────────────
PREFIX ont: <http://www.semanticweb.org/ontologies/onTEPT#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?paciente WHERE {
  ?paciente rdf:type ont:Patient_meetsPTSD_ICD11 .
  FILTER NOT EXISTS {
    ?paciente rdf:type ont:Patient_meetsPTSD_DSM5 .
  }
  FILTER NOT EXISTS {
    ?paciente rdf:type ont:Patient_meetsPTSD_WithDissociative_DSM5 .
  }
}

────────────────────────────────────────────────────────────────────────
SPARQL 3: Resumen de clasificación por paciente
────────────────────────────────────────────────────────────────────────
PREFIX ont: <http://www.semanticweb.org/ontologies/onTEPT#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?paciente
  (IF(EXISTS{?paciente rdf:type ont:Patient_meetsPTSD_DSM5},
      "SÍ", "NO") AS ?TEPT_DSM5)
  (IF(EXISTS{?paciente rdf:type ont:Patient_meetsPTSD_ICD11},
      "SÍ", "NO") AS ?TEPT_ICD11)
  (IF(EXISTS{?paciente rdf:type ont:Patient_meetsPTSD_WithDissociative_DSM5},
      "SÍ", "NO") AS ?TEPT_Disociativo_DSM5)
  (IF(EXISTS{?paciente rdf:type ont:Patient_meetsPTSD_Complex_ICD11},
      "SÍ", "NO") AS ?TEPT_Complejo_ICD11)
WHERE {
  ?paciente rdf:type ont:Patient .
}
ORDER BY ?paciente

════════════════════════════════════════════════════════════════════════
PRUEBAS DE INCONSISTENCIA (archivo _PobladaIncons.rdf)
════════════════════════════════════════════════════════════════════════
  1. Abrir _PobladaIncons.rdf en Protégé.
  2. Ejecutar razonador (Reasoner → HermiT → Start).
  3. El razonador DEBE reportar "Ontology is INCONSISTENT".
  4. Verificar las explicaciones (Explain inconsistency):
     - PatientINCONS_DSM5_noA: tiene evento no traumático pero está
       clasificado como Patient_meetsPTSD_DSM5 (requiere A=traumático)
     - PatientINCONS_DSM5_noB: no tiene IntrusionSymptom pero está
       clasificado como Patient_meetsPTSD_DSM5 (requiere B)
     - PatientINCONS_DSM5_noH: síntomas atribuibles a sustancias pero
       clasificado como Patient_meetsPTSD_DSM5 (requiere H=NOT atribuible)
     - PatientINCONS_ICD11_no1: evento no traumático pero clasificado
       como Patient_meetsPTSD_ICD11 (requiere criterio 1)
     - PatientINCONS_ICD11_no2: sin IntrusionSymptom pero clasificado
       como Patient_meetsPTSD_ICD11 (requiere criterio 2)
     - PatientINCONS_ICD11_no4: solo 1 ThreatArousal pero clasificado
       como Patient_meetsPTSD_ICD11 (requiere criterio 4, min 2)
════════════════════════════════════════════════════════════════════════
"""
    print(consultas_protege)


def intentar_razonamiento(ruta_onto_guardada):
    """
    Intenta ejecutar el razonador con owlready2/HermiT.
    Nota: Requiere Java instalado y accesible en PATH.

    Para la ontología consistente, debería funcionar sin errores.
    Para la inconsistente, lanzará OwlReadyInconsistentOntologyError.
    """
    print(f"\n{'='*70}")
    print("INTENTANDO RAZONAMIENTO CON sync_reasoner (HermiT)")
    print(f"{'='*70}")

    try:
        onto_razonar = get_ontology(ruta_onto_guardada).load()
        with onto_razonar:
            sync_reasoner(infer_property_values=True)
        print("✓ Razonamiento completado sin inconsistencias.")

        # Consultar clasificaciones inferidas
        print("\n  Pacientes clasificados como Patient_meetsPTSD_DSM5:")
        for ind in onto_razonar.Patient_meetsPTSD_DSM5.instances():
            print(f"    ✓ {ind.name}")

        print("\n  Pacientes clasificados como Patient_meetsPTSD_ICD11:")
        for ind in onto_razonar.Patient_meetsPTSD_ICD11.instances():
            print(f"    ✓ {ind.name}")

        print("\n  Pacientes clasificados como "
              "Patient_meetsPTSD_WithDissociative_DSM5:")
        for ind in onto_razonar.Patient_meetsPTSD_WithDissociative_DSM5.instances():
            print(f"    ✓ {ind.name}")

        print("\n  Pacientes clasificados como "
              "Patient_meetsPTSD_Complex_ICD11:")
        for ind in onto_razonar.Patient_meetsPTSD_Complex_ICD11.instances():
            print(f"    ✓ {ind.name}")

        # Verificación de interoperabilidad
        dsm5_set = set(
            onto_razonar.Patient_meetsPTSD_DSM5.instances())
        icd11_set = set(
            onto_razonar.Patient_meetsPTSD_ICD11.instances())
        dsm5_disoc_set = set(
            onto_razonar.Patient_meetsPTSD_WithDissociative_DSM5.instances())

        dsm5_total = dsm5_set | dsm5_disoc_set

        print(f"\n{'─'*70}")
        print("VERIFICACIÓN DE INTEROPERABILIDAD")
        print(f"{'─'*70}")

        # DSM-5 → CIE-11
        dsm5_en_icd11 = dsm5_total & icd11_set
        dsm5_no_en_icd11 = dsm5_total - icd11_set
        print(f"\n  DSM-5 → CIE-11:")
        print(f"    Pacientes DSM-5 que TAMBIÉN son CIE-11: "
              f"{len(dsm5_en_icd11)}")
        print(f"    Pacientes DSM-5 que NO son CIE-11: "
              f"{len(dsm5_no_en_icd11)}")
        if len(dsm5_no_en_icd11) == 0:
            print(f"    ✓ CONFIRMADO: Todo paciente TEPT DSM-5 es también "
                  f"TEPT CIE-11")
        else:
            print(f"    ✗ HAY PACIENTES DSM-5 QUE NO SON CIE-11 "
                  f"(revisar ontología)")

        # CIE-11 → DSM-5
        icd11_en_dsm5 = icd11_set & dsm5_total
        icd11_no_en_dsm5 = icd11_set - dsm5_total
        print(f"\n  CIE-11 → DSM-5:")
        print(f"    Pacientes CIE-11 que TAMBIÉN son DSM-5: "
              f"{len(icd11_en_dsm5)}")
        print(f"    Pacientes CIE-11 que NO son DSM-5: "
              f"{len(icd11_no_en_dsm5)}")
        if len(icd11_no_en_dsm5) > 0:
            print(f"    ✓ CONFIRMADO: Existen pacientes TEPT CIE-11 que "
                  f"NO son TEPT DSM-5")
            print(f"    Pacientes CIE-11 exclusivos:")
            for ind in icd11_no_en_dsm5:
                print(f"      → {ind.name}")
        else:
            print(f"    ✗ TODOS los CIE-11 son DSM-5 (revisar GRUPO 5 y 6)")

        return onto_razonar

    except OwlReadyInconsistentOntologyError:
        print("✗ INCONSISTENCIA DETECTADA por el razonador.")
        print("  Esto es ESPERADO para la ontología _PobladaIncons.rdf")
        return None
    except Exception as e:
        print(f"✗ Error durante el razonamiento: {e}")
        print("  Asegúrese de tener Java instalado y accesible en PATH.")
        return None


# ═════════════════════════════════════════════════════════════════════
# BLOQUE PRINCIPAL
# ═════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Configuración
    RUTA_ONTO = r"d:\Doctorado\Objetivo 2"
    ARCHIVO_ONTO = "onTEPT_v2_13.rdf"

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  POBLAR SINTÉTICOS v3 — Validación de Razonamiento e       ║")
    print("║  Interoperabilidad DSM-5 / CIE-11                         ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Paso 1: Poblar la ontología
    onto = poblar_sinteticos_ext_v3(
        RUTA_ONTO, ARCHIVO_ONTO,
        x_cumple=3,
        incluir_inconsistencias=True,
        ejecutar_consultas=True
    )
    '''
    # Paso 2: Intentar razonamiento con la ontología CONSISTENTE
    ruta_consistente = os.path.join(
        RUTA_ONTO, ARCHIVO_ONTO.replace(".rdf", "_PobladaFull.rdf"))

    print(f"\n{'█'*70}")
    print("PASO 2: Razonamiento sobre ontología CONSISTENTE")
    print(f"{'█'*70}")
    onto_razonada = intentar_razonamiento(ruta_consistente)

    # Paso 3: Intentar razonamiento con la ontología INCONSISTENTE
    ruta_incons = os.path.join(
        RUTA_ONTO, ARCHIVO_ONTO.replace(".rdf", "_PobladaIncons.rdf"))
    if os.path.exists(ruta_incons):
        print(f"\n{'█'*70}")
        print("PASO 3: Razonamiento sobre ontología INCONSISTENTE")
        print("  (Se espera que el razonador reporte INCONSISTENCIA)")
        print(f"{'█'*70}")
        intentar_razonamiento(ruta_incons)
'''