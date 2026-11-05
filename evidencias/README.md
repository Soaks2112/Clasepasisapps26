# Evidencias — Deber 5

Verificación realizada el **4 de noviembre de 2026**, hora de Ecuador.
Las trazas exportadas usan UTC (por eso sus marcas corresponden al día 5).

| Archivo | Qué demuestra | Estado |
|---|---|---|
| `parte1_server.png` | Fragmento real de server.py con las tres tools | Listo |
| `inspector_tools.png` | Las tres herramientas descubiertas en MCP Inspector | Listo |
| `inspector_pruebas.png` | Composición de las capturas reales D1–D7 | Listo |
| `pytest.png` | Salida real de pytest: 16 pruebas pasan | Listo |
| `agente_tools.png` | Interfaz del agente con llamadas, argumentos y resultados | **Pendiente de captura manual** |

## Origen de las pruebas

- `inspector_D1.png` a `inspector_D7.png` son capturas originales del navegador
  del Inspector 2.14.0. Se convirtieron de JPEG a PNG sin alterar su contenido.
- `inspector_pruebas.png` reúne las siete capturas con rótulos D1–D7. No se
  inventaron resultados ni se recreó una interfaz.
- `inspector_protocolo.json` es la exportación del Inspector: contiene los
  argumentos completos, las respuestas y `isError` de todas las llamadas.
  Complementa los registros que no caben en la ventana de una captura.
- `inspector_reinicio.json` y `inspector_reinicio.png` corresponden a una nueva
  conexión que lanzó otro proceso stdio: la misma alerta volvió a registrarse.
- `pytest.txt` conserva la salida de la ejecución real. `pytest.png` es una
  captura de esa salida presentada en una página local de lectura, no una
  simulación de una terminal. La prueba stdio inicia y cierra procesos reales.
- `parte1_server.png` muestra el fragmento de registro de herramientas del
  código real, presentado en una página local de lectura.
- `investigacion_agente.md` fue escrito por el chat nuevo después de sus llamadas
  reales al MCP. No sustituye la captura obligatoria de la interfaz.

## Matriz observada en Inspector

| Caso | Resultado |
|---|---|
| D1 | INC-001, INC-002 e INC-003; cantidades 2, 6 y 5 |
| D2 | Seis LOGIN_FAILED de admin desde 203.0.113.25 |
| D3 | INC-999 rechazado; `isError: true` |
| D4 | Alerta de INC-003 registrada con nivel alto |
| D5 | Mismos argumentos, mismo proceso: duplicado rechazado |
| D6 | Nivel `critico` rechazado |
| D7 | Motivo de tres espacios rechazado |
| Reinicio | Misma alerta aceptada en el proceso nuevo |

## Captura pendiente

Abrir el chat **Deber 5 — investigación mediante MCP** creado en Codex
(identificador `01a1a966-b61e-7201-b5a4-6215485e77c5`). Expandir las llamadas de
las herramientas para mostrar sus nombres, argumentos y resultados. Guardar
la captura como `evidencias/agente_tools.png` en la copia de entrega.
Si hacen falta varias capturas, conservarlas también con nombres descriptivos.
No reemplazar esta prueba por una imagen del párrafo final o de este documento.
