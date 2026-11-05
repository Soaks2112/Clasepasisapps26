"""Servidor stdio de Centinela: consulta datos y registra alertas en memoria."""

import json
from copy import deepcopy
from pathlib import Path
from threading import Lock

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError


class RegistroCasos:
    """Lógica determinista; cada instancia mantiene sus propias alertas."""

    def __init__(self) -> None:
        ruta = Path(__file__).resolve().with_name("casos.json")
        self._casos = json.loads(ruta.read_text(encoding="utf-8"))
        self._alertas: dict[str, dict] = {}
        self._lock = Lock()

    def _validar_caso(self, caso_id: str) -> None:
        if not isinstance(caso_id, str) or caso_id not in self._casos:
            raise ValueError(f"El caso {caso_id!r} no existe.")

    def listar(self) -> list[dict]:
        """Devuelve identificadores, sistemas y cantidades, sin interpretaciones."""
        return [
            {"id": caso_id, "sistema": caso["sistema"],
             "cantidad_eventos": len(caso["eventos"])}
            for caso_id, caso in self._casos.items()
        ]

    def consultar(self, caso_id: str) -> list[dict]:
        """Devuelve una copia exacta de los eventos o lanza ValueError."""
        self._validar_caso(caso_id)
        return deepcopy(self._casos[caso_id]["eventos"])

    def registrar(self, caso_id: str, nivel: str, motivo: str) -> dict:
        """Valida todos los argumentos y guarda una única alerta por caso."""
        self._validar_caso(caso_id)
        if not isinstance(nivel, str) or nivel not in ("bajo", "medio", "alto"):
            raise ValueError("El nivel debe ser bajo, medio o alto.")
        if not isinstance(motivo, str) or not motivo.strip():
            raise ValueError("El motivo debe ser texto y no puede estar vacío.")
        with self._lock:
            if caso_id in self._alertas:
                raise ValueError(f"Alerta duplicada: ya existe una alerta para {caso_id}.")
            alerta = {"caso_id": caso_id, "nivel": nivel,
                      "motivo": motivo.strip(), "estado": "registrada"}
            self._alertas[caso_id] = alerta
            return alerta.copy()


mcp = MCPServer("MCP Detective")
registro = RegistroCasos()


@mcp.tool()
def listar_casos() -> list[dict]:
    """Lista el id, sistema y cantidad de eventos de cada caso; solo lectura."""
    return registro.listar()


@mcp.tool()
def consultar_eventos(caso_id: str) -> list[dict]:
    """Consulta los eventos exactos de un caso; falla si no existe; solo lectura."""
    try:
        return registro.consultar(caso_id)
    except ValueError as error:
        # SDK 2.3: ToolError conserva el mensaje de validación para el cliente.
        raise ToolError(str(error)) from error


@mcp.tool()
def registrar_alerta(caso_id: str, nivel: str, motivo: str) -> dict[str, str]:
    """Registra en memoria una alerta única: nivel bajo/medio/alto y motivo no vacío."""
    try:
        return registro.registrar(caso_id, nivel, motivo)
    except ValueError as error:
        raise ToolError(str(error)) from error


if __name__ == "__main__":
    mcp.run(transport="stdio")
