# Parte 3 del Deber 5 — Investigación nueva de Centinela

La evidencia procede exclusivamente de llamadas reales a las herramientas MCP del servidor detective en este chat. La primera búsqueda del catálogo no devolvió herramientas; tras habilitarse el espacio mcp__detective, una segunda búsqueda encontró las tres herramientas. No se consultaron archivos de casos, código, consigna ni evidencias previas.

## Llamadas y resultados

1. `listar_casos({})` devolvió:

```json
{
  "result": [
    {
      "id": "INC-001",
      "sistema": "portal_acceso",
      "cantidad_eventos": 2
    },
    {
      "id": "INC-002",
      "sistema": "portal_acceso",
      "cantidad_eventos": 6
    },
    {
      "id": "INC-003",
      "sistema": "panel_administracion",
      "cantidad_eventos": 5
    }
  ]
}
```

2. `consultar_eventos({"caso_id":"INC-001"})` devolvió:

```json
{
  "result": [
    {
      "hora": "08:41",
      "usuario": "ana",
      "ip": "198.51.100.10",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "08:42",
      "usuario": "ana",
      "ip": "198.51.100.10",
      "evento": "LOGIN_SUCCESS"
    }
  ]
}
```

3. `consultar_eventos({"caso_id":"INC-002"})` devolvió:

```json
{
  "result": [
    {
      "hora": "02:10",
      "usuario": "admin",
      "ip": "203.0.113.25",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "02:11",
      "usuario": "admin",
      "ip": "203.0.113.25",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "02:12",
      "usuario": "admin",
      "ip": "203.0.113.25",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "02:13",
      "usuario": "admin",
      "ip": "203.0.113.25",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "02:14",
      "usuario": "admin",
      "ip": "203.0.113.25",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "02:15",
      "usuario": "admin",
      "ip": "203.0.113.25",
      "evento": "LOGIN_FAILED"
    }
  ]
}
```

4. `consultar_eventos({"caso_id":"INC-003"})` devolvió:

```json
{
  "result": [
    {
      "hora": "03:00",
      "usuario": "admin",
      "ip": "192.0.2.50",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "03:01",
      "usuario": "admin",
      "ip": "192.0.2.50",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "03:02",
      "usuario": "admin",
      "ip": "192.0.2.50",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "03:03",
      "usuario": "admin",
      "ip": "192.0.2.50",
      "evento": "LOGIN_FAILED"
    },
    {
      "hora": "03:04",
      "usuario": "admin",
      "ip": "192.0.2.50",
      "evento": "LOGIN_SUCCESS"
    }
  ]
}
```

## Valoración

INC-001: un fallo y luego un acceso exitoso de ana desde la misma IP; por sí solos no prueban actividad maliciosa. INC-002: seis fallos consecutivos de admin desde la misma IP justifican revisar posibles intentos repetidos de acceso; no consta acceso exitoso entre los eventos recibidos. INC-003: cuatro fallos de admin seguidos de éxito desde la misma IP en el panel de administración justifican nivel alto y revisión prioritaria. No se afirma una intrusión confirmada.

5. `registrar_alerta` recibió estos argumentos:

```json
{
  "caso_id": "INC-003",
  "nivel": "alto",
  "motivo": "En panel_administracion, admin registra cuatro LOGIN_FAILED a las 03:00, 03:01, 03:02 y 03:03 desde 192.0.2.50, seguidos de LOGIN_SUCCESS a las 03:04 desde la misma IP. La secuencia sobre una cuenta administrativa justifica revisión prioritaria de la legitimidad del acceso; es compatible con intentos de adivinar credenciales, pero no confirma una intrusión."
}
```

Resultado:

```json
{
  "caso_id": "INC-003",
  "nivel": "alto",
  "motivo": "En panel_administracion, admin registra cuatro LOGIN_FAILED a las 03:00, 03:01, 03:02 y 03:03 desde 192.0.2.50, seguidos de LOGIN_SUCCESS a las 03:04 desde la misma IP. La secuencia sobre una cuenta administrativa justifica revisión prioritaria de la legitimidad del acceso; es compatible con intentos de adivinar credenciales, pero no confirma una intrusión.",
  "estado": "registrada"
}
```

6. Por último, `consultar_eventos({"caso_id":"INC-999"})` devolvió `isError: true` y el texto exacto:

```text
Error executing tool consultar_eventos: El caso 'INC-999' no existe.
```

No se recibieron ni se inventaron eventos para INC-999. La alerta quedó registrada en memoria según la herramienta. Este relato complementa la traza visible de llamadas del chat; no sustituye su captura. No se realizó commit ni push.
