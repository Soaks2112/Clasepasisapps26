"""Pruebas de lógica aislada y de las herramientas a través de MCP real."""

import asyncio
import sys
from pathlib import Path

import pytest
from mcp import Client, StdioServerParameters

from server import RegistroCasos


@pytest.fixture
def registro():
    """Cada prueba obtiene memoria nueva; no depende del orden de ejecución."""
    return RegistroCasos()


def test_lista_exacta_sin_conclusiones(registro):
    assert registro.listar() == [
        {"id": "INC-001", "sistema": "portal_acceso", "cantidad_eventos": 2},
        {"id": "INC-002", "sistema": "portal_acceso", "cantidad_eventos": 6},
        {"id": "INC-003", "sistema": "panel_administracion", "cantidad_eventos": 5},
    ]


def test_consulta_seis_fallos_exactos(registro):
    assert registro.consultar("INC-002") == [
        {"hora": f"02:{minuto}", "usuario": "admin", "ip": "203.0.113.25",
         "evento": "LOGIN_FAILED"} for minuto in range(10, 16)
    ]


def test_caso_desconocido_es_error(registro):
    with pytest.raises(ValueError, match="INC-999.*no existe"):
        registro.consultar("INC-999")


def test_registro_valido(registro):
    assert registro.registrar("INC-003", "alto", " Requiere revisión ") == {
        "caso_id": "INC-003", "nivel": "alto", "motivo": "Requiere revisión",
        "estado": "registrada",
    }


def test_duplicado_rechazado(registro):
    registro.registrar("INC-003", "alto", "Revisar")
    with pytest.raises(ValueError, match="duplicada.*INC-003"):
        registro.registrar("INC-003", "medio", "Otro motivo")


@pytest.mark.parametrize("caso,nivel,motivo,mensaje", [
    ("INC-999", "alto", "Revisar", "no existe"),
    ("INC-002", "critico", "Revisar", "bajo, medio o alto"),
    ("INC-002", "ALTO", "Revisar", "bajo, medio o alto"),
    ("INC-002", "medio", "   ", "no puede estar vacío"),
    ("INC-002", "medio", "\t\n", "no puede estar vacío"),
    ("INC-002", "medio", "", "no puede estar vacío"),
    ("INC-002", "medio", 123, "debe ser texto"),
])
def test_parametros_invalidos_no_modifican_estado(registro, caso, nivel, motivo, mensaje):
    with pytest.raises(ValueError, match=mensaje):
        registro.registrar(caso, nivel, motivo)
    assert registro.registrar("INC-002", "medio", "Válido")["estado"] == "registrada"


def test_respuestas_no_permiten_modificar_datos(registro):
    registro.consultar("INC-001")[0]["evento"] = "ALTERADO"
    assert registro.consultar("INC-001")[0]["evento"] == "LOGIN_FAILED"
    registro.registrar("INC-003", "alto", "Revisar")["caso_id"] = "INC-001"
    with pytest.raises(ValueError, match="duplicada"):
        registro.registrar("INC-003", "alto", "Revisar")


def test_carga_desde_otro_directorio(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    assert len(RegistroCasos().listar()) == 3


def test_instancias_no_comparten_alertas(registro):
    registro.registrar("INC-003", "alto", "Revisar")
    assert RegistroCasos().registrar("INC-003", "alto", "Revisar")["estado"] == "registrada"


def test_mcp_stdio_discovery_validaciones_y_reinicio(tmp_path):
    """Ejecuta D1–D7 por stdio y comprueba el reinicio en otro proceso."""
    async def comprobar():
        parametros = StdioServerParameters(
            command=sys.executable,
            args=[str(Path(__file__).with_name("server.py").resolve())],
            cwd=str(tmp_path),
        )
        alerta = {"caso_id": "INC-003", "nivel": "alto", "motivo": "Revisar patrón"}
        async with Client(parametros) as cliente:
            tools = await cliente.list_tools()
            assert {t.name for t in tools.tools} == {
                "listar_casos", "consultar_eventos", "registrar_alerta"}
            lista = await cliente.call_tool("listar_casos", {})
            assert not lista.is_error
            assert lista.structured_content["result"] == RegistroCasos().listar()
            eventos = await cliente.call_tool("consultar_eventos", {"caso_id": "INC-002"})
            assert not eventos.is_error
            assert eventos.structured_content["result"] == RegistroCasos().consultar("INC-002")
            valida = await cliente.call_tool("registrar_alerta", alerta)
            assert not valida.is_error
            assert valida.structured_content == {**alerta, "estado": "registrada"}
            for tool, argumentos, mensaje in [
                ("consultar_eventos", {"caso_id": "INC-999"}, "no existe"),
                ("registrar_alerta", alerta, "duplicada"),
                ("registrar_alerta", {**alerta, "caso_id": "INC-002", "nivel": "critico"}, "bajo, medio o alto"),
                ("registrar_alerta", {**alerta, "caso_id": "INC-002", "motivo": "   "}, "no puede estar vacío"),
            ]:
                error = await cliente.call_tool(tool, argumentos)
                assert error.is_error
                assert mensaje in " ".join(c.text for c in error.content if c.type == "text")
                assert error.structured_content is None
            tipo_invalido = await cliente.call_tool(
                "registrar_alerta", {**alerta, "caso_id": "INC-002", "motivo": 123})
            assert tipo_invalido.is_error
        async with Client(parametros) as reiniciado:
            nueva = await reiniciado.call_tool("registrar_alerta", alerta)
            assert not nueva.is_error
            assert nueva.structured_content["estado"] == "registrada"
    asyncio.run(comprobar())
