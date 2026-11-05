# Deber 5 — Preparación para subir

**Estado: código y comprobaciones listos; falta una captura obligatoria.**
No se ha hecho push ni abierto un pull request.

La copia de entrega está en:

```text
C:\Users\XCORP\.codex\worktrees\deber5-entrega\Clasepasisapps26
```

Se preparó la rama `deber5` desde `origin/main`. Fue necesario usar una copia
aislada porque la carpeta original tiene cambios de otros trabajos y un historial
sin ancestro común con el `main` remoto. Los trabajos anteriores se conservaron.

## Ya comprobado

- [x] Repositorio público: https://github.com/Soaks2112/Clasepasisapps26.
- [x] Datos idénticos al bloque JSON de la consigna.
- [x] SDK MCP 2.3.0; tres herramientas, tipos y docstrings en español.
- [x] Ruta de datos basada en `__file__`; sin `print()` en el servidor.
- [x] Validaciones de caso, nivel, motivo y duplicado antes de guardar.
- [x] 16 pruebas pytest pasan, incluyendo comunicación real por stdio.
- [x] D1–D7 ejecutados en la interfaz de MCP Inspector.
- [x] Alerta duplicada rechazada y aceptada después de reiniciar el proceso.
- [x] Investigación en chat nuevo mediante herramientas MCP reales.
- [x] Respuestas e instrucciones de instalación y conexión redactadas.
- [x] Cuatro de las cinco capturas obligatorias disponibles.
- [ ] Capturar las llamadas del chat nuevo en `evidencias/agente_tools.png`.
- [ ] Leer el código y ajustar `respuestas.md` a tus propias palabras.
- [ ] Subir `deber5` y abrir el pull request hacia `main`.

## Completar y subir

1. Guardar la captura pendiente en la copia de entrega. Las instrucciones están
   en `evidencias/README.md`.
2. Revisar `respuestas.md` y el código.
3. Ejecutar desde la **copia de entrega**:

```powershell
Set-Location 'C:\Users\XCORP\.codex\worktrees\deber5-entrega\Clasepasisapps26'
if (-not (Test-Path 'evidencias/agente_tools.png')) {
    throw 'Falta la captura obligatoria agente_tools.png. No subir todavía.'
}
git add mcp-detective/ respuestas.md evidencias/ ENTREGA_DEBER5.md
git commit -m 'deber5: completa evidencia del agente y revisión personal'
git push -u origin deber5
```

4. Abrir [la comparación para crear el pull request](https://github.com/Soaks2112/Clasepasisapps26/compare/main...deber5?expand=1),
   con base `main` y rama `deber5`. El enlace funcionará después del push.
5. Entregar en el aula **solo el enlace del pull request**. No entregar el ZIP
   ni las capturas por separado.

## Texto sugerido del pull request

**Título:** Deber 5: MCP Detective, pruebas y evidencias

Implementa el servidor MCP de Centinela por stdio con las herramientas
listar_casos, consultar_eventos y registrar_alerta. Valida casos, niveles,
motivos y alertas duplicadas; conserva las alertas únicamente en memoria.

Validación: 16 pruebas pytest, D1–D7 en MCP Inspector, reinicio del proceso e
investigación en un chat nuevo de Codex mediante herramientas MCP reales.
Incluye respuestas y evidencias en el repositorio.

Antes de publicar este texto, comprobar que ya existe la captura pendiente.

## Entorno local ya preparado

La conexión `detective` de Codex apunta al Python y servidor de la carpeta
original. Ambos contienen el mismo código que esta entrega. Para repetir
pruebas sobre esta copia sin reinstalar dependencias:

```powershell
& 'C:\Users\XCORP\Documentsc\Programasrepos\Clasepasisapps26\mcp-detective\.venv\Scripts\python.exe' -m pytest mcp-detective -q
```

Para instalar y conectar en otro computador, seguir `respuestas.md`.
El entorno virtual y las herramientas temporales no se incluyen en la entrega.
