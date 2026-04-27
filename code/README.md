# Código fuente — OnTEPT

Este directorio contiene los scripts Python para poblar la ontología OnTEPT con distintos tipos de datos.

## Estructura

```
code/
├── MenuPrincipal.py            ← Punto de entrada (menú interactivo)
├── population/                 ← Scripts de población
│   ├── poblar_PCL5.py
│   ├── poblar_PCLC.py
│   ├── poblar_PCPTSD5.py
│   ├── poblar_CAPS5.py
│   ├── poblar_EEG.py
│   └── poblar_sinteticos.py
├── interface/                  ← Interfaz gráfica
│   └── app.py
└── utils/                      ← Utilidades compartidas
    ├── ontology_utils.py
    ├── validators.py
    └── sparql_queries.py
```

## Uso básico

### Menú principal

```bash
cd code
python MenuPrincipal.py
```

El menú presenta las siguientes opciones:

```
╔════════════════════════════════════════╗
║  OnTEPT — Menú de Población           ║
╠════════════════════════════════════════╣
║  1. Poblar con datos PCL-5            ║
║  2. Poblar con datos PCL-C (DSM-IV)   ║
║  3. Poblar con datos PC-PTSD-5        ║
║  4. Poblar con datos CAPS-5           ║
║  5. Poblar con datos EEG              ║
║  6. Generar datos sintéticos          ║
║  7. Abrir interfaz gráfica            ║
║  0. Salir                             ║
╚════════════════════════════════════════╝
```

### Uso directo de módulos

Cada script puede importarse o ejecutarse de forma independiente:

```python
# Población desde PCL-5
from population.poblar_PCL5 import poblar_desde_PCL5
poblar_desde_PCL5(
    ruta_ontologia="ruta/a/onTEPT_v1.0.rdf",
    archivo_datos="datos/pcl5_pacientes.csv",
    archivo_salida="onTEPT_v1.0_PCL5.rdf"
)
```

## Formato de datos de entrada

### PCL-5 / PCL-C / PC-PTSD-5

Los scripts esperan un archivo CSV con una fila por paciente y columnas nombradas según los ítems del instrumento:

```
patient_id, item_1, item_2, ..., item_N, total_score
P001, 2, 3, 1, 0, 2, 3, 1, 0, 2, 1, 3, 2, 1, 0, 2, 3, 1, 0, 2, 3, 36
```

### EEG

El script `poblar_EEG.py` espera un CSV con una fila por segmento/canal y columnas correspondientes a las características extraídas:

```
patient_id, channel, rhythm, mean, variance, kurtosis, ...
P001, Fp1, alpha, 0.012, 0.003, 1.45, ...
```

### Datos sintéticos

El script `poblar_sinteticos.py` es completamente paramétrico. Ver su documentación interna para detalles.

## Seguridad y privacidad

Los scripts **no incluyen datos reales de pacientes**. Los archivos de datos (CSV, etc.) deben ser anonimizados antes de su uso y **no deben subirse al repositorio** (están excluidos en `.gitignore`).

## Requisitos

Ver [`../requirements.txt`](../requirements.txt).
