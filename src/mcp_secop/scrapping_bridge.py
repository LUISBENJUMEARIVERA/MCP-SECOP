"""Puente bidireccional entre el servidor MCP SECOP II y el proyecto SCRAPPING."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

import httpx

from .models import (
    CustomAPIFeedCreateRequest,
    CustomAPIFeedSpec,
    InformationCategorySummary,
    RAGPipelineResponse,
    ScrappingBridgeStatus,
    SecopFilterParams,
    SecopSearchResponse,
    SpiderCrawlRequest,
    SpiderCrawlResponse,
)
from .secop_engine import (
    CUSTOM_FEEDS_REGISTRY,
    build_rag_pipeline_from_records,
    register_custom_feed,
    search_secop2_direct,
    seed_default_feeds,
)
from .taxonomy_spider import (
    crawl_secop_portal,
    get_secop2_taxonomy_catalog,
    inspect_opportunity_detail,
)


def _resolve_default_scrapping_workspace() -> Path:
    env_path = os.environ.get("SCRAPPING_WORKSPACE_PATH")
    if env_path:
        return Path(env_path).resolve()
    repo_root = Path(__file__).resolve().parents[2]
    sibling = repo_root.parent / "SCRAPPING"
    return sibling


class ScrappingBridgeClient:
    """Conector inteligente que delega o sincroniza operaciones con el proyecto SCRAPPING."""

    def __init__(
        self,
        api_url: str | None = None,
        workspace_path: Path | None = None,
    ) -> None:
        self.api_url = (
            api_url or os.environ.get("SCRAPPING_API_URL") or "http://127.0.0.1:8010"
        ).rstrip("/")
        self.workspace_path = workspace_path or _resolve_default_scrapping_workspace()
        seed_default_feeds()

    def inspect_local_workspace(self) -> tuple[bool, list[str]]:
        """Verifica la presencia de los módulos clave del proyecto hermano SCRAPPING en disco."""
        if not self.workspace_path.exists():
            return False, []

        expected_files = [
            "backend/app/main.py",
            "backend/app/secop_scraper.py",
            "backend/app/taxonomy_spider.py",
            "backend/app/rag_engine.py",
            "frontend/src/App.tsx",
            ".agents/skills/secop2-hybrid-scraper-rag/SKILL.md",
        ]
        found: list[str] = []
        for rel in expected_files:
            if (self.workspace_path / rel).exists():
                found.append(rel)
        return len(found) > 0, found

    async def check_status(
        self,
        mcp_tools_count: int = 8,
        mcp_resources_count: int = 4,
        mcp_prompts_count: int = 2,
    ) -> ScrappingBridgeStatus:
        """Verifica la conectividad HTTP con SCRAPPING (:8010) y la vinculación en disco."""
        ws_exists, modules = self.inspect_local_workspace()
        start = time.perf_counter()
        reachable = False
        latency_ms: float | None = None

        try:
            async with httpx.AsyncClient(timeout=2.5) as client:
                resp = await client.get(f"{self.api_url}/api/v1/health")
                if resp.status_code == 200:
                    reachable = True
                    latency_ms = round((time.perf_counter() - start) * 1000.0, 1)
        except Exception:
            reachable = False

        mode: Any = "ONLINE_HTTP_BRIDGE" if reachable else "LOCAL_WORKSPACE_HYBRID"
        msg = (
            f"Conectado en vivo con SCRAPPING API ({self.api_url}) en {latency_ms} ms."
            if reachable
            else (
                f"Vinculado al workspace SCRAPPING ({self.workspace_path.name}) con motor "
                "híbrido autónomo activo (SODA SoQL + Spider ASP.NET + Chunker RAG)."
            )
        )

        return ScrappingBridgeStatus(
            bridge_mode=mode,
            scrapping_api_url=self.api_url,
            scrapping_http_reachable=reachable,
            scrapping_http_latency_ms=latency_ms,
            scrapping_workspace_path=str(self.workspace_path),
            scrapping_workspace_detected=ws_exists,
            detected_modules=modules,
            shared_feeds_count=len(CUSTOM_FEEDS_REGISTRY),
            mcp_tools_registered=mcp_tools_count,
            mcp_resources_registered=mcp_resources_count,
            mcp_prompts_registered=mcp_prompts_count,
            status_message=msg,
        )

    async def search_processes(self, filters: SecopFilterParams) -> SecopSearchResponse:
        """Busca procesos/contratos delegando a SCRAPPING si está activo o usando el motor directo."""
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.post(
                    f"{self.api_url}/api/v1/secop/search",
                    json=filters.model_dump(),
                )
                if resp.status_code == 200:
                    payload = resp.json()
                    payload["data_source"] = "SCRAPPING_PROJECT_BRIDGE"
                    return SecopSearchResponse(**payload)
        except Exception:
            pass
        return await search_secop2_direct(filters)

    async def crawl_portal(self, req: SpiderCrawlRequest) -> SpiderCrawlResponse:
        """Ejecuta el Spider delegando al proyecto SCRAPPING o directamente."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(
                    f"{self.api_url}/api/v1/spider/crawl",
                    json=req.model_dump(),
                )
                if resp.status_code == 200:
                    payload = resp.json()
                    payload["execution_mode"] = "SCRAPPING_BRIDGE_SPIDER"
                    return SpiderCrawlResponse(**payload)
        except Exception:
            pass
        return await crawl_secop_portal(req)

    async def inspect_opportunity(self, url: str) -> dict[str, Any]:
        """Inspecciona el expediente OpportunityDetail de SECOP II."""
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.get(
                    f"{self.api_url}/api/v1/spider/inspect",
                    params={"url": url},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    data["bridge_source"] = "SCRAPPING_API"
                    return data
        except Exception:
            pass
        res = await inspect_opportunity_detail(url)
        res["bridge_source"] = "MCP_HYBRID_ENGINE"
        return res

    async def generate_rag_chunks(
        self,
        filters: SecopFilterParams,
        chunk_size_chars: int = 1400,
    ) -> RAGPipelineResponse:
        """Genera chunks semánticos listos para ingesta en bases de datos vectoriales."""
        try:
            async with httpx.AsyncClient(timeout=4.5) as client:
                resp = await client.post(
                    f"{self.api_url}/api/v1/rag/chunks",
                    params={"chunk_size_chars": chunk_size_chars},
                    json=filters.model_dump(),
                )
                if resp.status_code == 200:
                    return RAGPipelineResponse(**resp.json())
        except Exception:
            pass

        search_res = await self.search_processes(filters)
        return build_rag_pipeline_from_records(
            search_res.records,
            filters=filters,
            chunk_size_chars=chunk_size_chars,
        )

    def get_taxonomy(self) -> list[InformationCategorySummary]:
        """Retorna las 6 categorías taxonómicas y 11 enlaces principales de SECOP II."""
        return get_secop2_taxonomy_catalog()

    async def list_feeds(self) -> list[CustomAPIFeedSpec]:
        """Lista los feeds RAG registrados localmente y sincroniza con SCRAPPING si responde."""
        seed_default_feeds()
        try:
            async with httpx.AsyncClient(timeout=2.5) as client:
                resp = await client.get(f"{self.api_url}/api/v1/feeds")
                if resp.status_code == 200:
                    for raw_feed in resp.json():
                        spec = CustomAPIFeedSpec(**raw_feed)
                        CUSTOM_FEEDS_REGISTRY[spec.slug] = spec
        except Exception:
            pass
        return list(CUSTOM_FEEDS_REGISTRY.values())

    async def create_feed(self, req: CustomAPIFeedCreateRequest) -> CustomAPIFeedSpec:
        """Registra un feed RAG en MCP-SECOP y lo replica en SCRAPPING si está en línea."""
        local_spec = register_custom_feed(req)
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                await client.post(
                    f"{self.api_url}/api/v1/feeds",
                    json=req.model_dump(),
                )
        except Exception:
            pass
        return local_spec
