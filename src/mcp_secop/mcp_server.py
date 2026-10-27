"""Servidor oficial Model Context Protocol (MCP) para SECOP II Colombia + Puente SCRAPPING."""

from __future__ import annotations

import json
from typing import Any, Literal

from mcp.server.mcpserver import MCPServer

from .models import (
    CustomAPIFeedCreateRequest,
    SecopFilterParams,
    SpiderCrawlRequest,
)
from .scrapping_bridge import ScrappingBridgeClient

mcp = MCPServer(
    "mcp-secop-colombia",
    instructions=(
        "Servidor MCP oficial para el Sistema Electrónico para la Contratación Pública (SECOP II) "
        "y Colombia Compra Eficiente, conectado en puente bidireccional con el proyecto SCRAPPING. "
        "Permite consultar licitaciones y contratos por SODA SoQL, ejecutar el Spider asíncrono sobre "
        "portales ASP.NET Vortal, inspeccionar expedientes OpportunityDetail y generar chunks RAG."
    ),
)

bridge_client = ScrappingBridgeClient()


@mcp.tool()
async def secop_search_processes(
    dataset: Literal["procesos", "contratos"] = "procesos",
    keyword: str | None = None,
    entidad: str | None = None,
    nit_entidad: str | None = None,
    departamento: str | None = None,
    ciudad: str | None = None,
    modalidad: str | None = None,
    estado: str | None = None,
    cuantia_min: float | None = None,
    cuantia_max: float | None = None,
    unspsc_code: str | None = None,
    limit: int = 10,
    spider_enrich_top_n: int = 0,
) -> dict[str, Any]:
    """Busca procesos de contratación o contratos electrónicos en SECOP II (SODA SoQL + Puente SCRAPPING)."""
    filters = SecopFilterParams(
        dataset=dataset,
        keyword=keyword,
        entidad=entidad,
        nit_entidad=nit_entidad,
        departamento=departamento,
        ciudad=ciudad,
        modalidad=modalidad,
        estado=estado,
        cuantia_min=cuantia_min,
        cuantia_max=cuantia_max,
        unspsc_code=unspsc_code,
        limit=max(1, min(limit, 50)),
        spider_enrich_top_n=max(0, min(spider_enrich_top_n, 5)),
    )
    res = await bridge_client.search_processes(filters)
    return res.model_dump()


@mcp.tool()
async def secop_spider_crawl(
    seed_url: str = "https://www.colombiacompra.gov.co/secop-ii",
    max_links: int = 30,
    follow_internal_depth: int = 1,
    category_filter: str | None = None,
) -> dict[str, Any]:
    """Ejecuta el Spider web asíncrono sobre SECOP II / Colombia Compra Eficiente clasificando enlaces y __VIEWSTATE."""
    req = SpiderCrawlRequest(
        seed_url=seed_url,
        max_links=max(5, min(max_links, 100)),
        follow_internal_depth=max(1, min(follow_internal_depth, 2)),
        category_filter=category_filter,
    )
    res = await bridge_client.crawl_portal(req)
    return res.model_dump()


@mcp.tool()
async def secop_inspect_opportunity(
    process_url: str = "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.6184920",
) -> dict[str, Any]:
    """Inspecciona en profundidad una URL OpportunityDetail de SECOP II (tablas DOM, __VIEWSTATE y pliegos anexos)."""
    return await bridge_client.inspect_opportunity(process_url)


@mcp.tool()
async def secop_generate_rag_chunks(
    dataset: Literal["procesos", "contratos"] = "procesos",
    keyword: str | None = "software",
    entidad: str | None = None,
    departamento: str | None = None,
    modalidad: str | None = None,
    estado: str | None = None,
    cuantia_min: float | None = None,
    limit: int = 8,
    chunk_size_chars: int = 1400,
) -> dict[str, Any]:
    """Genera chunks semánticos en Markdown con cabecera contextual institucional y metadatos para RAG (Qdrant/Chroma)."""
    filters = SecopFilterParams(
        dataset=dataset,
        keyword=keyword,
        entidad=entidad,
        departamento=departamento,
        modalidad=modalidad,
        estado=estado,
        cuantia_min=cuantia_min,
        limit=max(1, min(limit, 50)),
    )
    res = await bridge_client.generate_rag_chunks(
        filters=filters,
        chunk_size_chars=max(400, min(chunk_size_chars, 4000)),
    )
    return res.model_dump()


@mcp.tool()
async def secop_get_taxonomy_map(category_code: str | None = None) -> dict[str, Any]:
    """Devuelve el mapa taxonómico de 6 dominios y 11 enlaces principales de SECOP II y Colombia Compra Eficiente."""
    catalog = bridge_client.get_taxonomy()
    if category_code:
        code_upper = category_code.strip().upper()
        catalog = [c for c in catalog if c.code.upper() == code_upper]
    return {
        "total_categories": len(catalog),
        "total_links": sum(len(c.links) for c in catalog),
        "categories": [c.model_dump() for c in catalog],
    }


@mcp.tool()
async def secop_manage_rag_feeds(
    action: Literal["list", "create"] = "list",
    name: str | None = None,
    slug: str | None = None,
    keyword: str | None = None,
    departamento: str | None = None,
    modalidad: str | None = None,
    chunk_size_chars: int = 1400,
) -> dict[str, Any]:
    """Lista o crea feeds dinámicos de API RAG sincronizados con el proyecto SCRAPPING."""
    if action == "create":
        feed_name = name or f"Feed SECOP II ({keyword or 'General'})"
        req = CustomAPIFeedCreateRequest(
            name=feed_name,
            slug=slug,
            filters=SecopFilterParams(
                dataset="procesos",
                keyword=keyword,
                departamento=departamento,
                modalidad=modalidad,
                limit=15,
            ),
            chunk_size_chars=chunk_size_chars,
        )
        created = await bridge_client.create_feed(req)
        return {
            "action": "created",
            "feed": created.model_dump(),
        }

    feeds = await bridge_client.list_feeds()
    return {
        "action": "listed",
        "total_feeds": len(feeds),
        "feeds": [f.model_dump() for f in feeds],
    }


@mcp.tool()
async def secop_bridge_status() -> dict[str, Any]:
    """Diagnostica el estado en vivo del puente bidireccional entre MCP-SECOP y el proyecto SCRAPPING."""
    status = await bridge_client.check_status()
    return status.model_dump()


@mcp.tool()
async def secop_analyze_procurement_budget(
    dataset: Literal["procesos", "contratos"] = "procesos",
    keyword: str | None = None,
    departamento: str | None = None,
    modalidad: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Ejecuta un análisis financiero y de concentración contractual en COP sobre procesos o contratos de SECOP II."""
    filters = SecopFilterParams(
        dataset=dataset,
        keyword=keyword,
        departamento=departamento,
        modalidad=modalidad,
        limit=max(1, min(limit, 50)),
    )
    search_res = await bridge_client.search_processes(filters)
    top_processes = sorted(
        search_res.records,
        key=lambda r: r.base_price_cop,
        reverse=True,
    )[:5]
    return {
        "dataset": dataset,
        "records_analyzed": search_res.total_returned,
        "data_source": search_res.data_source,
        "soql_executed": search_res.soql_query_executed,
        "financial_summary_cop": search_res.summary_metrics,
        "top_5_highest_value_processes": [
            {
                "process_id": r.process_id,
                "reference": r.reference,
                "entity_name": r.entity_name,
                "title": r.title,
                "modality": r.modality,
                "status": r.status,
                "base_price_cop": r.base_price_cop,
                "process_url": r.process_url,
            }
            for r in top_processes
        ],
    }


@mcp.resource("secop://taxonomy/catalog")
def resource_taxonomy_catalog() -> str:
    """Recurso MCP con la taxonomía completa de SECOP II y Colombia Compra Eficiente."""
    catalog = [c.model_dump() for c in bridge_client.get_taxonomy()]
    return json.dumps(catalog, ensure_ascii=False, indent=2)


@mcp.resource("secop://bridge/scrapping-status")
async def resource_scrapping_status() -> str:
    """Recurso MCP con el estado de vinculación al proyecto hermano SCRAPPING."""
    status = await bridge_client.check_status()
    return json.dumps(status.model_dump(), ensure_ascii=False, indent=2)


@mcp.resource("secop://rag/default-feeds")
async def resource_default_feeds() -> str:
    """Recurso MCP con los feeds RAG activos y sus snippets para LangChain y LlamaIndex."""
    feeds = await bridge_client.list_feeds()
    return json.dumps([f.model_dump() for f in feeds], ensure_ascii=False, indent=2)


@mcp.resource("secop://schemas/soql-dictionary")
def resource_soql_dictionary() -> str:
    """Diccionario oficial de campos Socrata SODA SoQL para SECOP II Procesos y Contratos."""
    dictionary = {
        "procesos_endpoint": "https://www.datos.gov.co/resource/p6dx-8zbt.json",
        "contratos_endpoint": "https://www.datos.gov.co/resource/jbjy-vk9h.json",
        "fields": {
            "id_del_proceso": "Identificador único transaccional (ej. CO1.PCCNTR.6184920)",
            "referencia_del_proceso": "Código institucional del proceso asignado por la entidad",
            "entidad": "Nombre oficial de la Entidad Estatal compradora",
            "nit_entidad": "NIT de la Entidad Estatal",
            "departamento_entidad": "Departamento de ejecución o sede de la entidad",
            "modalidad_de_contratacion": "Licitación pública, Selección abreviada, Concurso de méritos, Mínima cuantía, Contratación directa",
            "precio_base": "Presupuesto oficial estimado en pesos colombianos (COP)",
            "estado_del_procedimiento": "Abierto, Publicado, Evaluación, Adjudicado, Celebrado",
            "codigo_principal_de_categoria": "Clasificador de Bienes y Servicios UNSPSC (ej. V1.43232400)",
            "urlproceso": "Enlace directo a OpportunityDetail en community.secop.gov.co",
        },
    }
    return json.dumps(dictionary, ensure_ascii=False, indent=2)


@mcp.prompt()
def auditoria_licitacion_secop2(
    keyword: str = "inteligencia artificial",
    departamento: str = "Distrito Capital de Bogotá",
) -> str:
    """Plantilla de prompt para auditar licitaciones públicas en SECOP II usando las herramientas MCP."""
    return (
        f"Actúa como un Auditor Senior en Contratación Estatal Colombiana (Ley 80 de 1993, Ley 1150 de 2007 "
        f"y Decreto 1082 de 2015).\n"
        f"1. Ejecuta la herramienta `secop_search_processes` con `keyword='{keyword}'` y `departamento='{departamento}'`.\n"
        f"2. Analiza las cuantías en COP, las modalidades de selección, los códigos UNSPSC y las fechas de cierre.\n"
        f"3. Para el proceso de mayor presupuesto, invoca `secop_inspect_opportunity` sobre su `process_url`.\n"
        f"4. Entrega un dictamen ejecutivo estructurado con riesgos, requisitos habilitantes y enlaces verificados."
    )


@mcp.prompt()
def ingesta_rag_contratacion(
    sector_keyword: str = "software",
    feed_slug: str = "licitaciones-software-ia-colombia",
) -> str:
    """Plantilla de prompt para construir e ingerir un pipeline RAG conectado al proyecto SCRAPPING."""
    return (
        f"Actúa como un Arquitecto de Sistemas RAG conectado al servidor MCP SECOP II y al proyecto SCRAPPING.\n"
        f"1. Verifica el estado del puente con `secop_bridge_status`.\n"
        f"2. Genera los fragmentos vectoriales con `secop_generate_rag_chunks` para `keyword='{sector_keyword}'`.\n"
        f"3. Consulta o registra el feed `{feed_slug}` usando `secop_manage_rag_feeds`.\n"
        f"4. Presenta el resumen de tokens, hashes SHA-256 y el código de ingesta para Qdrant/LangChain."
    )


MCP_TOOLS_CATALOG: list[dict[str, Any]] = [
    {
        "name": "secop_search_processes",
        "code": "TOOL-01",
        "title": "Búsqueda Híbrida SODA SoQL + SCRAPPING Bridge",
        "description": "Filtra procesos de contratación (p6dx-8zbt) y contratos electrónicos (jbjy-vk9h) por palabra clave, entidad, NIT, departamento, modalidad, cuantía COP y código UNSPSC.",
        "default_args": {
            "dataset": "procesos",
            "keyword": "software",
            "departamento": "Distrito Capital de Bogotá",
            "limit": 6,
        },
    },
    {
        "name": "secop_spider_crawl",
        "code": "TOOL-02",
        "title": "Motor Spider Asíncrono & Detector __VIEWSTATE",
        "description": "Rastrea portales de Colombia Compra Eficiente y community.secop.gov.co, detectando sesiones ASP.NET Vortal y clasificando enlaces según su utilidad RAG.",
        "default_args": {
            "seed_url": "https://www.colombiacompra.gov.co/secop-ii",
            "max_links": 25,
            "follow_internal_depth": 1,
        },
    },
    {
        "name": "secop_inspect_opportunity",
        "code": "TOOL-03",
        "title": "Inspector Profundo de Expediente (OpportunityDetail)",
        "description": "Inspecciona el DOM de un proceso individual en SECOP II (noticeUID), extrayendo tablas contractuales, tokens __VIEWSTATE y anexos descargables.",
        "default_args": {
            "process_url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.6184920",
        },
    },
    {
        "name": "secop_generate_rag_chunks",
        "code": "TOOL-04",
        "title": "Sintetizador de Chunks Semánticos para RAG",
        "description": "Transforma expedientes de SECOP II en fragmentos Markdown con cabecera contextual institucional inyectada, hash SHA-256 y metadatos para Qdrant/Chroma/pgvector.",
        "default_args": {
            "dataset": "procesos",
            "keyword": "inteligencia artificial",
            "limit": 5,
            "chunk_size_chars": 1400,
        },
    },
    {
        "name": "secop_get_taxonomy_map",
        "code": "TOOL-05",
        "title": "Mapa Taxonómico SECOP II (6 Dominios / 11 Enlaces)",
        "description": "Devuelve la arquitectura documental ordenada de Colombia Compra Eficiente: Procesos, Contratos, Documentos Tipo, TVEC, Plan Anual PAA y OCDS.",
        "default_args": {},
    },
    {
        "name": "secop_manage_rag_feeds",
        "code": "TOOL-06",
        "title": "Gestor de Feeds Dinámicos RAG (Sincronizado con SCRAPPING)",
        "description": "Lista o publica endpoints personalizados (/api/v1/feeds/{slug}/rag y .jsonl) con snippets automáticos para LangChain y LlamaIndex.",
        "default_args": {
            "action": "list",
        },
    },
    {
        "name": "secop_bridge_status",
        "code": "TOOL-07",
        "title": "Diagnóstico del Puente Bidireccional SCRAPPING",
        "description": "Verifica la conexión en tiempo real con el proyecto hermano SCRAPPING (:8010 y workspace local ../SCRAPPING) y reporta telemetría del servidor MCP.",
        "default_args": {},
    },
    {
        "name": "secop_analyze_procurement_budget",
        "code": "TOOL-08",
        "title": "Analítica Presupuestal y Concentración en COP",
        "description": "Calcula presupuesto total, promedio, distribución por modalidad/departamento y el Top 5 de procesos de mayor cuantía en pesos colombianos.",
        "default_args": {
            "dataset": "procesos",
            "limit": 10,
        },
    },
]


async def dispatch_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Ejecuta una herramienta MCP por nombre desde la pasarela HTTP o pruebas."""
    handlers = {
        "secop_search_processes": secop_search_processes,
        "secop_spider_crawl": secop_spider_crawl,
        "secop_inspect_opportunity": secop_inspect_opportunity,
        "secop_generate_rag_chunks": secop_generate_rag_chunks,
        "secop_get_taxonomy_map": secop_get_taxonomy_map,
        "secop_manage_rag_feeds": secop_manage_rag_feeds,
        "secop_bridge_status": secop_bridge_status,
        "secop_analyze_procurement_budget": secop_analyze_procurement_budget,
    }
    handler = handlers.get(tool_name)
    if not handler:
        raise ValueError(f"Herramienta MCP desconocida: '{tool_name}'")
    clean_args = {k: v for k, v in arguments.items() if v is not None and v != ""}
    return await handler(**clean_args)
