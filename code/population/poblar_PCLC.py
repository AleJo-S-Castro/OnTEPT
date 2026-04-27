# -*- coding: utf-8 -*-
"""
poblar_PCLC.py
Pobla la ontología OnTEPT con datos del PCL-C (DSM-IV, 17 ítems).

Implementación pendiente. Ver poblar_PCL5.py para la estructura de referencia.
"""
import sys


def poblar_desde_PCLC(ruta_onto: str,
                              ruta_datos: str,
                              ruta_salida: str):
    """Pobla la ontología desde los datos del instrumento correspondiente."""
    raise NotImplementedError(
        "Este módulo está pendiente de implementación. "
        "Ver poblar_PCL5.py para la estructura de referencia.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Uso: python poblar_PCLC.py <ontologia.rdf> <datos.csv> <salida.rdf>")
        sys.exit(1)
