"""Suite de pruebas automatizadas para MCP SECOP II Colombia y su puente con SCRAPPING."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from mcp_secop import __version__
from mcp_secop.mcp_server import (
    MCP_TOOLS_CATALOG,
    auditoria_licitacion_secop2,
    dispatch_mcp_tool,
    ingesta_rag_contratacion,
    resource_soql_dictionary,
    resource_taxonomy_catalog,
)
from mcp_secop.models import SecopFilterParams
from mcp_secop.secop_engine import build_soql_query, filter_fallback_records
from mcp_secop.web_app import app

client = TestClient(app)


def test_package_version_and_catalog() -> None:
    # Arrange / Act
    total_tools = len(MCP_TOOLS_CATALOG)

    # Assert
    assert __version__ == "1.0.0"
    assert total_tools == 8


def test_build_soql_query_sanitizes_and_formats() -> None:
    # Arrange
    filters = SecopFilterParams(
        dataset="procesos",
        keyword="inteligencia artificial",
        departamento="Distrito Capital de Bogotá",
        cuantia_min=100_000_000,
        limit=10,
    )

    # Act
    human_soql, params = build_soql_query(filters)

    # Assert
    assert "SELECT * FROM secop2_procesos" in human_soql
    assert "INTELIGENCIA ARTIFICIAL" in params["$where"]
    assert "precio_base >= 100000000" in params["$where"]
    assert params["$limit"] == 10


def test_fallback_records_filtering() -> None:
    # Arrange
    filters = SecopFilterParams(dataset="procesos", keyword="ciberseguridad", limit=5)

    # Act
    records = filter_fallback_records(filters)

    # Assert
    assert len(records) >= 1
    assert "Ciberseguridad" in records[0].title


@pytest.mark.asyncio
async def test_mcp_tools_dispatch_search_and_rag() -> None:
    # Arrange / Act
    search_res = await dispatch_mcp_tool(
        "secop_search_processes",
        {"dataset": "procesos", "keyword": "software", "limit": 4},
    )
    rag_res = await dispatch_mcp_tool(
        "secop_generate_rag_chunks",
        {"dataset": "procesos", "keyword": "software", "limit": 3, "chunk_size_chars": 1200},
    )

    # Assert
    assert search_res["total_returned"] >= 1
    assert "records" in search_res
    assert rag_res["total_chunks"] >= 1
    assert "[SECOP II]" in rag_res["chunks"][0]["text"]


@pytest.mark.asyncio
async def test_mcp_bridge_and_budget_tools() -> None:
    # Arrange / Act
    bridge_st = await dispatch_mcp_tool("secop_bridge_status", {})
    budget_res = await dispatch_mcp_tool(
        "secop_analyze_procurement_budget",
        {"dataset": "procesos", "limit": 6},
    )

    # Assert
    assert bridge_st["mcp_tools_registered"] == 8
    assert bridge_st["scrapping_workspace_detected"] is True
    assert budget_res["financial_summary_cop"]["total_budget_cop"] > 0
    assert len(budget_res["top_5_highest_value_processes"]) >= 1


def test_mcp_resources_and_prompts() -> None:
    # Arrange / Act
    tax_json = resource_taxonomy_catalog()
    soql_json = resource_soql_dictionary()
    prompt_audit = auditoria_licitacion_secop2(keyword="nube", departamento="Antioquia")
    prompt_rag = ingesta_rag_contratacion(sector_keyword="salud")

    # Assert
    assert "CAT-01" in tax_json
    assert "p6dx-8zbt.json" in soql_json
    assert "secop_search_processes" in prompt_audit
    assert "secop_generate_rag_chunks" in prompt_rag


def test_web_gateway_endpoints_and_swiss_ui() -> None:
    # Arrange / Act
    ui_resp = client.get("/")
    health_resp = client.get("/api/v1/health")
    tools_resp = client.get("/api/v1/mcp/tools")
    call_resp = client.post(
        "/api/v1/mcp/call",
        json={"tool_name": "secop_get_taxonomy_map", "arguments": {"category_code": "CAT-01"}},
    )
    feed_jsonl_resp = client.get("/api/v1/feeds/licitaciones-software-ia-colombia/jsonl")

    # Assert
    assert ui_resp.status_code == 200
    assert "MCP SECOP II" in ui_resp.text
    assert health_resp.status_code == 200
    assert health_resp.json()["status"] == "OPERATIONAL"
    assert tools_resp.json()["total"] == 8
    assert call_resp.status_code == 200
    assert call_resp.json()["result"]["total_categories"] == 1
    assert feed_jsonl_resp.status_code == 200
    assert "secop2_" in feed_jsonl_resp.text
