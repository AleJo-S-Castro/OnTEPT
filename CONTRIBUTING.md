# Guía de contribución — OnTEPT

Gracias por tu interés en contribuir a OnTEPT. Las contribuciones pueden tomar distintas formas: correcciones de errores, mejoras en la documentación, nuevos scripts de población, o extensiones de la ontología.

## Formas de contribuir

### 1. Reportar un error o sugerir una mejora

Usa la sección [Issues](https://github.com/TU_USUARIO/onTEPT/issues) de GitHub. Indica:

- **Tipo:** error, mejora, pregunta, documentación.
- **Descripción:** describe el problema o la sugerencia con suficiente detalle.
- **Reproducción** (si es un error): pasos para reproducirlo, versión de la ontología afectada, razonador usado.

### 2. Contribuir código o documentación

1. Haz un *fork* del repositorio.
2. Crea una rama descriptiva: `git checkout -b fix/descripcion-breve` o `feature/descripcion-breve`.
3. Realiza tus cambios y añade una entrada en `CHANGELOG.md`.
4. Abre un *Pull Request* hacia la rama `main` con una descripción clara de los cambios.

### 3. Extensiones de la ontología

Las modificaciones a los archivos OWL (`.rdf`) deben:

- Respetar el perfil **OWL 2 DL** (sin características fuera de perfil).
- Incluir `rdfs:label` y `rdfs:comment` en **español** e **inglés** para cualquier nuevo elemento.
- Verificar que la ontología modificada es **consistente** con Fact++ o HermiT antes de hacer la PR.
- Documentar el cambio en `CHANGELOG.md`.

## Estándares de código Python

- Compatibilidad con Python 3.9+.
- Documentación de funciones con docstrings.
- Nombres de variables y funciones en inglés; comentarios en español o inglés son aceptables.
- Las dependencias nuevas deben añadirse a `requirements.txt`.

## Proceso de revisión

Todas las *pull requests* son revisadas por el equipo de desarrollo. El tiempo de respuesta habitual es de 1–2 semanas.
