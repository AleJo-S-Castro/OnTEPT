# Interfaz gráfica — OnTEPT

Este directorio contiene la interfaz gráfica de usuario (GUI) para poblar la ontología OnTEPT de forma interactiva, sin necesidad de editar código ni archivos CSV manualmente.

## Estado

> **En desarrollo.** La interfaz está en fase de implementación activa.

## Funcionalidades previstas

- Formulario para cargar datos de pacientes individuales desde los instrumentos PCL-5, CAPS-5 y PC-PTSD-5.
- Visualización del perfil diagnóstico inferido (DSM-5 / CIE-11).
- Exportación de la ontología poblada.
- Panel de consultas SPARQL predefinidas.

## Requisitos adicionales

```bash
pip install customtkinter
```

## Uso (cuando esté disponible)

```bash
python app.py
```

o bien desde el menú principal:

```bash
python ../MenuPrincipal.py
# Seleccionar opción 7
```
