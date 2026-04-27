# -*- coding: utf-8 -*-
"""
validators.py — Validación de datos de entrada antes de poblar la ontología.
"""

def validar_fila_pcl5(fila: dict, id_col: str = "patient_id") -> tuple[bool, list]:
    """
    Valida una fila del PCL-5.
    Retorna (valida: bool, errores: list[str]).
    """
    errores = []
    for i in range(1, 21):
        col = f"item_{i}"
        val = fila.get(col)
        if val is None:
            errores.append(f"Columna '{col}' ausente")
        else:
            try:
                v = int(val)
                if not (0 <= v <= 4):
                    errores.append(f"'{col}'={v} fuera de rango [0-4]")
            except ValueError:
                errores.append(f"'{col}'='{val}' no es entero")
    return (len(errores) == 0), errores


def validar_fila_pcptsd5(fila: dict) -> tuple[bool, list]:
    """Valida una fila del PC-PTSD-5 (ítems binarios 0/1)."""
    errores = []
    for i in range(1, 6):
        col = f"item_{i}"
        val = fila.get(col)
        if val is None:
            errores.append(f"Columna '{col}' ausente")
        else:
            try:
                v = int(val)
                if v not in (0, 1):
                    errores.append(f"'{col}'={v} debe ser 0 o 1")
            except ValueError:
                errores.append(f"'{col}'='{val}' no es entero")
    return (len(errores) == 0), errores


def validar_fila_caps5(fila: dict) -> tuple[bool, list]:
    """Valida una fila del CAPS-5 (ítems 1-30, escala 0-4)."""
    errores = []
    for i in range(1, 31):
        col = f"caps_item_{i}"
        val = fila.get(col)
        if val is None:
            errores.append(f"Columna '{col}' ausente")
        else:
            try:
                v = int(val)
                if not (0 <= v <= 4):
                    errores.append(f"'{col}'={v} fuera de rango [0-4]")
            except ValueError:
                errores.append(f"'{col}'='{val}' no es entero")
    return (len(errores) == 0), errores
