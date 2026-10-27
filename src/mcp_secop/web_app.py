"""Pasarela HTTP FastAPI y Centro de Control Web Suizo para el servidor MCP SECOP II."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse

from .mcp_server import MCP_TOOLS_CATALOG, bridge_client, dispatch_mcp_tool
from .models import (
    CustomAPIFeedCreateRequest,
    CustomAPIFeedSpec,
    InformationCategorySummary,
    MCPToolCallRequest,
    RAGPipelineResponse,
    ScrappingBridgeStatus,
)
from .secop_engine import CUSTOM_FEEDS_REGISTRY, seed_default_feeds
from .ui_template import SWISS_LIGHT_MCP_UI_HTML

app = FastAPI(
    title="MCP SECOP II Colombia — Gateway & Puente SCRAPPING",
    version="1.0.0",
    description=(
        "Pasarela HTTP, Inspector de Herramientas MCP y Puente Bidireccional con el proyecto "
        "SCRAPPING para el Sistema Electrónico para la Contratación Pública (SECOP II)."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

seed_default_feeds()


@app.get("/", response_class=HTMLResponse)
async def serve_swiss_control_center() -> HTMLResponse:
    """Sirve la interfaz web en Minimalismo Suizo Institucional de tonalidades claras."""
    return HTMLResponse(content=SWISS_LIGHT_MCP_UI_HTML)


@app.get("/arquitectura.html", response_class=HTMLResponse)
async def serve_archify_diagram() -> HTMLResponse:
    """Sirve el diagrama interactivo generado con Archify desde docs/arquitectura.html."""
    repo_root = Path(__file__).resolve().parents[2]
    arch_file = repo_root / "docs" / "arquitectura.html"
    if arch_file.exists():
        return HTMLResponse(content=arch_file.read_text(encoding="utf-8"))
    return HTMLResponse(
        content="<h1>Diagrama Archify en generación (docs/arquitectura.html)</h1>",
        status_code=404,
    )


@app.get("/api/v1/health")
async def health_check() -> dict[str, Any]:
    """Devuelve el estado operativo del servidor MCP SECOP II y su puente SCRAPPING."""
    bridge_st = await bridge_client.check_status()
    return {
        "status": "OPERATIONAL",
        "server": "mcp-secop-colombia",
        "version": "1.0.0",
        "mcp_tools_count": len(MCP_TOOLS_CATALOG),
        "mcp_resources_count": 4,
        "mcp_prompts_count": 2,
        "bridge_mode": bridge_st.bridge_mode,
        "scrapping_workspace_detected": bridge_st.scrapping_workspace_detected,
        "scrapping_http_reachable": bridge_st.scrapping_http_reachable,
        "active_rag_feeds": len(CUSTOM_FEEDS_REGISTRY),
    }


@app.get("/api/v1/bridge/status", response_model=ScrappingBridgeStatus)
async def get_bridge_status() -> ScrappingBridgeStatus:
    """Diagnostica en vivo el puente con el proyecto SCRAPPING."""
    return await bridge_client.check_status()


@app.get("/api/v1/mcp/tools")
async def list_mcp_tools() -> dict[str, Any]:
    """Lista las 8 herramientas registradas en el servidor MCP con sus argumentos por defecto."""
    return {
        "server": "mcp-secop-colombia",
        "total": len(MCP_TOOLS_CATALOG),
        "tools": MCP_TOOLS_CATALOG,
    }


@app.post("/api/v1/mcp/call")
async def call_mcp_tool(req: MCPToolCallRequest) -> dict[str, Any]:
    """Invoca cualquiera de las 8 herramientas MCP y devuelve la carga útil estructurada."""
    try:
        result = await dispatch_mcp_tool(req.tool_name, req.arguments)
        return {
            "jsonrpc": "2.0",
            "tool": req.tool_name,
            "status": "SUCCESS",
            "result": result,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/v1/taxonomy", response_model=list[InformationCategorySummary])
async def get_taxonomy() -> list[InformationCategorySummary]:
    """Devuelve las 6 categorías taxonómicas y 11 enlaces principales de SECOP II."""
    return bridge_client.get_taxonomy()


@app.get("/api/v1/feeds", response_model=list[CustomAPIFeedSpec])
async def get_feeds() -> list[CustomAPIFeedSpec]:
    """Lista los feeds RAG sincronizados con el proyecto SCRAPPING."""
    return await bridge_client.list_feeds()


@app.post("/api/v1/feeds", response_model=CustomAPIFeedSpec)
async def create_feed(req: CustomAPIFeedCreateRequest) -> CustomAPIFeedSpec:
    """Crea un nuevo feed RAG y lo sincroniza con SCRAPPING."""
    return await bridge_client.create_feed(req)


@app.get("/api/v1/feeds/{slug}/rag", response_model=RAGPipelineResponse)
async def execute_feed_rag(slug: str) -> RAGPipelineResponse:
    """Ejecuta un feed RAG por su slug y devuelve los chunks semánticos con metadatos."""
    await bridge_client.list_feeds()
    feed = CUSTOM_FEEDS_REGISTRY.get(slug)
    if not feed:
        raise HTTPException(status_code=404, detail=f"Feed RAG '{slug}' no encontrado.")
    return await bridge_client.generate_rag_chunks(
        filters=feed.filters,
        chunk_size_chars=feed.chunk_size_chars,
    )


@app.get("/api/v1/feeds/{slug}/jsonl", response_class=PlainTextResponse)
async def execute_feed_jsonl(slug: str) -> PlainTextResponse:
    """Exporta un feed RAG en formato JSONL (application/x-ndjson) para Qdrant/Chroma/pgvector."""
    await bridge_client.list_feeds()
    feed = CUSTOM_FEEDS_REGISTRY.get(slug)
    if not feed:
        raise HTTPException(status_code=404, detail=f"Feed RAG '{slug}' no encontrado.")
    pipeline = await bridge_client.generate_rag_chunks(
        filters=feed.filters,
        chunk_size_chars=feed.chunk_size_chars,
    )
    lines = [json.dumps(c.model_dump(), ensure_ascii=False) for c in pipeline.chunks]
    return PlainTextResponse(
        content="\n".join(lines) + "\n",
        media_type="application/x-ndjson",
        headers={"Content-Disposition": f'attachment; filename="{slug}.jsonl"'},
    )


def run_web_server(host: str = "127.0.0.1", port: int = 8020) -> None:
    """Inicia el servidor FastAPI del Centro de Control Web MCP SECOP II."""
    uvicorn.run("mcp_secop.web_app:app", host=host, port=port, reload=False)
