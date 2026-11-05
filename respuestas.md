# Deber 5 — MCP Detective

## 1. Arquitectura

El LLM eligió qué herramientas llamar e interpretó los resultados. Codex, como
host, mostró la conversación y coordinó las llamadas. El cliente MCP descubrió
las herramientas, envió sus argumentos y recibió las respuestas por stdio.
El proceso del servidor ejecutó realmente Python: leyó los casos, validó los
argumentos y almacenó las alertas en memoria. El LLM no ejecutó esa lógica por sí solo.

## 2. Evidencia

INC-003 muestra cuatro fallos de inicio de sesión de `admin` entre 03:00 y 03:03,
seguidos de un acceso exitoso a las 03:04 desde la misma IP, `192.0.2.50`, en el
panel de administración. Es un patrón que merece revisión prioritaria y motivó
una alerta de nivel alto. No demuestra una intrusión: estos registros no indican
quién estaba detrás del acceso, si era legítimo ni qué hizo después. También
podrían corresponder a errores de contraseña de una persona autorizada.

## 3. Validación y seguridad

El servidor rechaza los casos inexistentes, los niveles fuera de `bajo`, `medio`
y `alto`, los motivos que no son texto o están en blanco y las alertas duplicadas.
El SDK también verifica los tipos de los argumentos. No basta con confiar en el
modelo: puede equivocarse o recibir instrucciones que lo induzcan a enviar
argumentos inválidos. Las reglas del servidor se aplican en cada llamada, antes
de modificar el estado, independientemente de lo que sugiera el LLM.

Las validaciones de la lógica lanzan `ValueError`. En MCP 2.3.0 las herramientas
convierten esos errores esperados en `ToolError` para conservar el mensaje ante
el cliente; el SDK oculta el detalle de excepciones inesperadas. No se devuelve
una confirmación falsa ante un error.

## Agente y comprobación de conexión

Se usó **Codex de escritorio**. La implementación y la investigación se hicieron
en chats distintos. En el chat «Deber 5 — investigación mediante MCP» se
descubrieron las tres herramientas del servidor `detective`, se llamó a
`listar_casos`, se consultaron los tres casos, se registró la alerta de INC-003 y
se consultó INC-999. El servidor respondió:

> Error executing tool consultar_eventos: El caso 'INC-999' no existe.

La investigación usó únicamente herramientas MCP para obtener los eventos.
El relato de las llamadas está en `evidencias/investigacion_agente.md`; la traza
original está en el chat nuevo. Un relato por sí solo no sustituye la captura
obligatoria de esa interfaz.

## Instalación y ejecución

Requisitos: Python 3.11 o superior y Node.js con npm/npx. Ejecutar desde la raíz:

```powershell
python -m venv mcp-detective/.venv
.\mcp-detective\.venv\Scripts\python.exe -m pip install -r mcp-detective/requirements.txt
.\mcp-detective\.venv\Scripts\mcp.exe version
.\mcp-detective\.venv\Scripts\python.exe -m pytest mcp-detective -q
```

La versión fijada del SDK es **2.3.0**, sin mezclar SDK v1. Se verificó con
Python 3.13.9. Las 16 pruebas cubren la lógica aislada, errores, discovery por
stdio, respuestas reales y pérdida de las alertas al iniciar otro proceso.

Iniciar el Inspector:

```powershell
.\mcp-detective\.venv\Scripts\mcp.exe dev mcp-detective/server.py
```

Alternativa que utiliza directamente el Python del entorno ya instalado:

```powershell
$pythonDetective = (Resolve-Path 'mcp-detective/.venv/Scripts/python.exe').Path
$servidorDetective = (Resolve-Path 'mcp-detective/server.py').Path
npx.cmd --yes @modelcontextprotocol/inspector@2.14.0 --web $pythonDetective $servidorDetective
```

Conectar el servidor en Codex:

```powershell
codex mcp add detective -- $pythonDetective $servidorDetective
codex mcp get detective
```

Abrir un chat nuevo para que descubra el servidor. Pedirle que liste los casos,
consulte sus eventos, registre la alerta justificada de INC-003 y consulte
INC-999. No abrir `casos.json`, el código ni evidencias previas durante esa
investigación. El Inspector y Codex inician procesos distintos: sus alertas no
se comparten. Al reiniciar cada proceso se pierde su memoria.

## Referencias consultadas

- [SDK de Python MCP v2](https://py.sdk.modelcontextprotocol.io/whats-new/).
- [Errores comprensibles con ToolError](https://py.sdk.modelcontextprotocol.io/servers/handling-errors/).
- [Conexión MCP en Codex](https://learn.chatgpt.com/docs/extend/mcp).

Las respuestas anteriores son un borrador preparado con asistencia de Codex;
el estudiante debe leerlas, verificar el código y ajustar la redacción a sus palabras.
