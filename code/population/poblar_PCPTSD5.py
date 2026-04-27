# -*- coding: utf-8 -*-
"""
poblar_PCPTSD5.py
Pobla la ontología OnTEPT con datos del PC-PTSD-5 (5 ítems binarios).

Implementación pendiente. Ver poblar_PCL5.py para la estructura de referencia.
"""
import sys


def poblar_desde_PCPTSD5(ruta_onto: str,
                              ruta_datos: str,
                              ruta_salida: str):
    """Pobla la ontología desde los datos del instrumento correspondiente."""
    raise NotImplementedError(
        "Este módulo está pendiente de implementación. "
        "Ver poblar_PCL5.py para la estructura de referencia.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Uso: python poblar_PCPTSD5.py <ontologia.rdf> <datos.csv> <salida.rdf>")
        sys.exit(1)
