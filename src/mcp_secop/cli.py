"""Interfaz de línea de comandos (CLI) para el servidor MCP SECOP II y el Puente SCRAPPING."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys

from .mcp_server import bridge_client, mcp
from .web_app import run_web_server


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos CLI."""
    parser = argparse.ArgumentParser(
        prog="mcp-secop",
        description=(
            "Servidor MCP (Model Context Protocol) para SECOP II Colombia conectado al proyecto SCRAPPING."
        ),
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transporte MCP a ejecutar (por defecto: stdio para Claude Desktop / Cursor / Antigravity).",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Inicia el Centro de Control Web Suizo y Pasarela HTTP en http://127.0.0.1:8020.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host para el servidor web (--web).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8020,
        help="Puerto para el servidor web (--web).",
    )
    parser.add_argument(
        "--check-bridge",
        action="store_true",
        help="Imprime el diagnóstico JSON del puente con el proyecto SCRAPPING y termina.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada principal de `mcp-secop`."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.check_bridge:
        status = asyncio.run(bridge_client.check_status())
        sys.stdout.write(json.dumps(status.model_dump(), ensure_ascii=False, indent=2) + "\n")
        return 0

    if args.web:
        run_web_server(host=args.host, port=args.port)
        return 0

    mcp.run(transport=args.transport)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
