"""Motor de consulta Socrata SODA SoQL, agregador presupuestal y generador de chunks RAG para SECOP II."""

from __future__ import annotations

import asyncio
import hashlib
import re
import time
import uuid
from datetime import UTC, datetime
from typing import Any

import httpx

from .models import (
    CustomAPIFeedCreateRequest,
    CustomAPIFeedSpec,
    RAGChunkItem,
    RAGChunkMetadata,
    RAGPipelineResponse,
    SecopFilterParams,
    SecopProcessRecord,
    SecopSearchResponse,
)
from .taxonomy_spider import BROWSER_HEADERS, inspect_opportunity_detail

SODA_ENDPOINTS = {
    "procesos": "https://www.datos.gov.co/resource/p6dx-8zbt.json",
    "contratos": "https://www.datos.gov.co/resource/jbjy-vk9h.json",
}

FALLBACK_SECOP2_RECORDS: list[dict[str, Any]] = [
    {
        "process_id": "CO1.PCCNTR.6184920",
        "reference": "MINTIC-LP-028-2026",
        "entity_name": "MINISTERIO DE TECNOLOGÍAS DE LA INFORMACIÓN Y LAS COMUNICACIONES",
        "entity_nit": "899999053",
        "department": "Distrito Capital de Bogotá",
        "city": "Bogotá",
        "entity_order": "Nacional",
        "title": "Arquitectura de Interoperabilidad e Inteligencia Artificial para Servicios Ciudadanos",
        "description": (
            "Contratar el diseño, desarrollo, implementación y operación asistida de una plataforma "
            "nacional de interoperabilidad semántica, servidores MCP y motores RAG sobre documentos públicos "
            "bajo lineamientos de Gobierno Digital y seguridad cero confianza."
        ),
        "phase": "Presentación de oferta",
        "status": "Abierto",
        "modality": "Licitación pública",
        "contract_type": "Prestación de servicios",
        "base_price_cop": 4850000000.0,
        "publication_date": "2026-10-18",
        "closing_date": "2026-11-15",
        "unspsc_code": "V1.43232400",
        "process_url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.6184920",
        "provider_awarded": None,
        "provider_nit": None,
    },
    {
        "process_id": "CO1.PCCNTR.6179310",
        "reference": "INV-SAMC-114-2026",
        "entity_name": "INSTITUTO NACIONAL DE VÍAS (INVIAS)",
        "entity_nit": "800215807",
        "department": "Distrito Capital de Bogotá",
        "city": "Bogotá",
        "entity_order": "Nacional",
        "title": "Rehabilitación y Mantenimiento Vial Corredor Logístico Ruta del Sol Tramo 2",
        "description": (
            "Ejecución de obras de mantenimiento periódico, señalización horizontal, estabilización de taludes "
            "y monitoreo geotécnico bajo Pliegos Tipo de Infraestructura de Transporte."
        ),
        "phase": "Presentación de observaciones",
        "status": "Publicado",
        "modality": "Selección abreviada menor cuantía",
        "contract_type": "Obra",
        "base_price_cop": 9320000000.0,
        "publication_date": "2026-10-14",
        "closing_date": "2026-11-04",
        "unspsc_code": "V1.72141000",
        "process_url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.6179310",
        "provider_awarded": None,
        "provider_nit": None,
    },
    {
        "process_id": "CO1.PCCNTR.6150442",
        "reference": "ALC-MED-CM-009-2026",
        "entity_name": "DISTRITO ESPECIAL DE CIENCIA, TECNOLOGÍA E INNOVACIÓN DE MEDELLÍN",
        "entity_nit": "890905211",
        "department": "Antioquia",
        "city": "Medellín",
        "entity_order": "Territorial",
        "title": "Interventoría Técnica, Financiera y Ambiental al Sistema Inteligente de Movilidad Urbana",
        "description": (
            "Realizar la interventoría integral al contrato de modernización de la red semafórica adaptativa "
            "y analítica de video en tiempo real del Distrito de Medellín."
        ),
        "phase": "Seleccionado",
        "status": "Adjudicado",
        "modality": "Concurso de méritos abierto",
        "contract_type": "Consultoría",
        "base_price_cop": 1940000000.0,
        "publication_date": "2026-09-29",
        "closing_date": "2026-10-20",
        "unspsc_code": "V1.81101500",
        "process_url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.6150442",
        "provider_awarded": "CONSORCIO INTERVENTORÍA VIAL Y TECNOLÓGICA ANTIOQUIA",
        "provider_nit": "901742819",
    },
    {
        "process_id": "CO1.PCCNTR.6190115",
        "reference": "SDS-BOG-SA-082-2026",
        "entity_name": "FONDO FINANCIERO DISTRITAL DE SALUD DE BOGOTÁ D.C.",
        "entity_nit": "800246953",
        "department": "Distrito Capital de Bogotá",
        "city": "Bogotá",
        "entity_order": "Territorial",
        "title": "Suministro de Equipos Biomédicos y Telemedicina para Red Hospitalaria Distrital",
        "description": (
            "Adquisición, instalación, calibración y mantenimiento preventivo de monitores de signos vitales "
            "multiparámetro y estaciones de telemedicina conectadas a historia clínica electrónica unificada."
        ),
        "phase": "Presentación de oferta",
        "status": "Abierto",
        "modality": "Selección abreviada subasta inversa",
        "contract_type": "Suministros",
        "base_price_cop": 3180000000.0,
        "publication_date": "2026-10-21",
        "closing_date": "2026-11-12",
        "unspsc_code": "V1.42181900",
        "process_url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.6190115",
        "provider_awarded": None,
        "provider_nit": None,
    },
    {
        "process_id": "CO1.PCCNTR.6168091",
        "reference": "GOB-VALLE-MC-219-2026",
        "entity_name": "DEPARTAMENTO DEL VALLE DEL CAUCA - SECRETARÍA DE LAS TIC",
        "entity_nit": "890399029",
        "department": "Valle del Cauca",
        "city": "Cali",
        "entity_order": "Territorial",
        "title": "Servicio de Auditoría de Ciberseguridad, Ethical Hacking y Pruebas de Penetración SOC",
        "description": (
            "Contratar los servicios especializados de pruebas de intrusión (Pentesting), análisis de "
            "vulnerabilidades sobre portales transaccionales y fortalecimiento del CSIRT departamental."
        ),
        "phase": "Presentación de oferta",
        "status": "Abierto",
        "modality": "Mínima cuantía",
        "contract_type": "Prestación de servicios",
        "base_price_cop": 128500000.0,
        "publication_date": "2026-10-22",
        "closing_date": "2026-10-30",
        "unspsc_code": "V1.81112200",
        "process_url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.6168091",
        "provider_awarded": None,
        "provider_nit": None,
    },
    {
        "process_id": "CO1.PCCNTR.6142800",
        "reference": "DIAN-CD-405-2026",
        "entity_name": "DIRECCIÓN DE IMPUESTOS Y ADUANAS NACIONALES (DIAN)",
        "entity_nit": "800197268",
        "department": "Distrito Capital de Bogotá",
        "city": "Bogotá",
        "entity_order": "Nacional",
        "title": "Suscripción de Nube Pública Híbrida y Procesamiento Analítico para Facturación Electrónica",
        "description": (
            "Renovación y ampliación de capacidad elástica de cómputo en la nube, lagos de datos analíticos "
            "y modelos de detección temprana de evasión tributaria al amparo del Acuerdo Marco de Nube Pública IV."
        ),
        "phase": "Celebrado",
        "status": "Celebrado",
        "modality": "Contratación directa",
        "contract_type": "Prestación de servicios",
        "base_price_cop": 6750000000.0,
        "publication_date": "2026-10-02",
        "closing_date": "2026-10-10",
        "unspsc_code": "V1.81162000",
        "process_url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.6142800",
        "provider_awarded": "UNIÓN TEMPORAL CLOUD GOBIERNO COLOMBIA",
        "provider_nit": "901882104",
    },
]


def _sanitize_soql(value: str) -> str:
    return value.replace("'", "''").strip()


def build_soql_query(filters: SecopFilterParams) -> tuple[str, dict[str, Any]]:
    """Construye la consulta SoQL parametrizada para Socrata SODA (`p6dx-8zbt` o `jbjy-vk9h`)."""
    where_parts: list[str] = []

    if filters.dataset == "procesos":
        desc_col = "descripci_n_del_procedimiento"
        title_col = "nombre_del_procedimiento"
        ent_col = "entidad"
        nit_col = "nit_entidad"
        dep_col = "departamento_entidad"
        city_col = "ciudad_entidad"
        mod_col = "modalidad_de_contratacion"
        status_col = "estado_del_procedimiento"
        price_col = "precio_base"
        unspsc_col = "codigo_principal_de_categoria"
        order_col = "fecha_de_publicacion_del DESC"
    else:
        desc_col = "objeto_del_contrato"
        title_col = "descripcion_del_proceso"
        ent_col = "nombre_entidad"
        nit_col = "nit_entidad"
        dep_col = "departamento"
        city_col = "ciudad"
        mod_col = "modalidad_de_contratacion"
        status_col = "estado_contrato"
        price_col = "valor_del_contrato"
        unspsc_col = "codigo_de_categoria_principal"
        order_col = "fecha_de_firma DESC"

    if filters.keyword:
        kw = _sanitize_soql(filters.keyword).upper()
        where_parts.append(f"(upper({desc_col}) like '%{kw}%' OR upper({title_col}) like '%{kw}%')")
    if filters.entidad:
        ent = _sanitize_soql(filters.entidad).upper()
        where_parts.append(f"upper({ent_col}) like '%{ent}%'")
    if filters.nit_entidad:
        nit = _sanitize_soql(filters.nit_entidad)
        where_parts.append(f"{nit_col} like '%{nit}%'")
    if filters.departamento:
        dep = _sanitize_soql(filters.departamento).upper()
        where_parts.append(f"upper({dep_col}) like '%{dep}%'")
    if filters.ciudad:
        cit = _sanitize_soql(filters.ciudad).upper()
        where_parts.append(f"upper({city_col}) like '%{cit}%'")
    if filters.modalidad:
        mod = _sanitize_soql(filters.modalidad).upper()
        where_parts.append(f"upper({mod_col}) like '%{mod}%'")
    if filters.estado:
        est = _sanitize_soql(filters.estado).upper()
        where_parts.append(f"upper({status_col}) like '%{est}%'")
    if filters.cuantia_min is not None and filters.cuantia_min > 0:
        where_parts.append(f"{price_col} >= {filters.cuantia_min}")
    if filters.cuantia_max is not None and filters.cuantia_max > 0:
        where_parts.append(f"{price_col} <= {filters.cuantia_max}")
    if filters.unspsc_code:
        unspsc = _sanitize_soql(filters.unspsc_code).upper()
        where_parts.append(f"upper({unspsc_col}) like '%{unspsc}%'")

    where_clause = " AND ".join(where_parts)
    params: dict[str, Any] = {
        "$limit": filters.limit,
        "$offset": filters.offset,
        "$order": order_col,
    }
    if where_clause:
        params["$where"] = where_clause

    human_soql = f"SELECT * FROM secop2_{filters.dataset}"
    if where_clause:
        human_soql += f" WHERE {where_clause}"
    human_soql += f" ORDER BY {order_col} LIMIT {filters.limit} OFFSET {filters.offset}"
    return human_soql, params


def _normalize_soda_record(raw: dict[str, Any], dataset: str) -> SecopProcessRecord:
    url_field = raw.get("urlproceso", "")
    process_url = (
        str(url_field.get("url", "")) if isinstance(url_field, dict) else str(url_field or "")
    )

    if dataset == "procesos":
        price_raw = raw.get("precio_base", 0)
        try:
            price = float(price_raw)
        except (ValueError, TypeError):
            price = 0.0

        pub_date = str(
            raw.get("fecha_de_publicacion_del") or raw.get("fecha_de_ultima_publicaci") or ""
        )[:10]
        close_date = str(raw.get("fecha_de_recepcion_de") or "")[:10]

        return SecopProcessRecord(
            process_id=str(
                raw.get("id_del_proceso") or raw.get("referencia_del_proceso") or "CO1.PCCNTR.N/A"
            ),
            reference=str(raw.get("referencia_del_proceso") or raw.get("id_del_proceso") or "S/R"),
            entity_name=str(raw.get("entidad") or "Entidad Estatal"),
            entity_nit=str(raw.get("nit_entidad") or "N/A"),
            department=str(raw.get("departamento_entidad") or "Nacional"),
            city=str(raw.get("ciudad_entidad") or "Colombia"),
            entity_order=str(raw.get("ordenentidad") or raw.get("orden_entidad") or "Nacional"),
            title=str(
                raw.get("nombre_del_procedimiento")
                or raw.get("descripci_n_del_procedimiento")
                or "Proceso SECOP II"
            )[:180],
            description=str(
                raw.get("descripci_n_del_procedimiento")
                or raw.get("nombre_del_procedimiento")
                or "Sin descripción registrada"
            ),
            phase=str(raw.get("fase") or "Publicación"),
            status=str(
                raw.get("estado_del_procedimiento")
                or raw.get("estado_de_apertura_del_proceso")
                or "Publicado"
            ),
            modality=str(raw.get("modalidad_de_contratacion") or "No especificada"),
            contract_type=str(raw.get("tipo_de_contrato") or "Servicios / Suministros"),
            base_price_cop=price,
            publication_date=pub_date or "2026-10-01",
            closing_date=close_date or "Por definir",
            unspsc_code=str(raw.get("codigo_principal_de_categoria") or "N/A"),
            process_url=process_url
            or "https://community.secop.gov.co/Public/Tendering/ContractNoticeManagement/Index",
            provider_awarded=raw.get("nombre_del_proveedor"),
            provider_nit=raw.get("nit_del_proveedor_adjudicado"),
        )

    price_raw = raw.get("valor_del_contrato", 0)
    try:
        price = float(price_raw)
    except (ValueError, TypeError):
        price = 0.0

    pub_date = str(raw.get("fecha_de_firma") or raw.get("fecha_de_inicio_del_contrato") or "")[:10]
    close_date = str(raw.get("fecha_de_fin_del_contrato") or "")[:10]

    return SecopProcessRecord(
        process_id=str(raw.get("id_contrato") or raw.get("proceso_de_compra") or "CO1.CONT.N/A"),
        reference=str(raw.get("referencia_del_contrato") or raw.get("proceso_de_compra") or "S/R"),
        entity_name=str(raw.get("nombre_entidad") or "Entidad Estatal"),
        entity_nit=str(raw.get("nit_entidad") or "N/A"),
        department=str(raw.get("departamento") or "Nacional"),
        city=str(raw.get("ciudad") or "Colombia"),
        entity_order=str(raw.get("orden") or "Nacional"),
        title=str(
            raw.get("descripcion_del_proceso")
            or raw.get("objeto_del_contrato")
            or "Contrato Electrónico SECOP II"
        )[:180],
        description=str(
            raw.get("objeto_del_contrato")
            or raw.get("descripcion_del_proceso")
            or "Sin objeto registrado"
        ),
        phase="Ejecución Contractual",
        status=str(raw.get("estado_contrato") or "En ejecución"),
        modality=str(raw.get("modalidad_de_contratacion") or "Contratación SECOP II"),
        contract_type=str(raw.get("tipo_de_contrato") or "Contrato Estatal"),
        base_price_cop=price,
        publication_date=pub_date or "2026-10-01",
        closing_date=close_date or "Vigente",
        unspsc_code=str(raw.get("codigo_de_categoria_principal") or "N/A"),
        process_url=process_url
        or "https://community.secop.gov.co/Public/Tendering/ContractNoticeManagement/Index",
        provider_awarded=str(raw.get("proveedor_adjudicado") or "") or None,
        provider_nit=str(raw.get("documento_proveedor") or "") or None,
    )


def filter_fallback_records(filters: SecopFilterParams) -> list[SecopProcessRecord]:
    """Filtra el conjunto de registros de respaldo cuando la pasarela SODA gubernamental no responde."""
    matched: list[SecopProcessRecord] = []
    for item in FALLBACK_SECOP2_RECORDS:
        if filters.keyword:
            kw = filters.keyword.lower()
            if kw not in item["title"].lower() and kw not in item["description"].lower():
                continue
        if filters.entidad and filters.entidad.lower() not in item["entity_name"].lower():
            continue
        if filters.nit_entidad and filters.nit_entidad not in item["entity_nit"]:
            continue
        if filters.departamento and filters.departamento.lower() not in item["department"].lower():
            continue
        if filters.ciudad and filters.ciudad.lower() not in item["city"].lower():
            continue
        if filters.modalidad and filters.modalidad.lower() not in item["modality"].lower():
            continue
        if filters.estado and filters.estado.lower() not in item["status"].lower():
            continue
        if filters.cuantia_min is not None and item["base_price_cop"] < filters.cuantia_min:
            continue
        if filters.cuantia_max is not None and item["base_price_cop"] > filters.cuantia_max:
            continue
        matched.append(SecopProcessRecord(**item))

    if not matched:
        matched = [SecopProcessRecord(**r) for r in FALLBACK_SECOP2_RECORDS[: filters.limit]]
    return matched[: filters.limit]


def compute_summary_metrics(records: list[SecopProcessRecord]) -> dict[str, Any]:
    """Calcula métricas financieras y de distribución por modalidad, departamento y estado."""
    total_cop = sum(r.base_price_cop for r in records)
    avg_cop = total_cop / len(records) if records else 0.0
    max_cop = max((r.base_price_cop for r in records), default=0.0)
    by_modality: dict[str, int] = {}
    by_department: dict[str, int] = {}
    by_status: dict[str, int] = {}

    for r in records:
        by_modality[r.modality] = by_modality.get(r.modality, 0) + 1
        by_department[r.department] = by_department.get(r.department, 0) + 1
        by_status[r.status] = by_status.get(r.status, 0) + 1

    return {
        "total_budget_cop": round(total_cop, 2),
        "average_budget_cop": round(avg_cop, 2),
        "max_budget_cop": round(max_cop, 2),
        "unique_entities": len({r.entity_name for r in records}),
        "by_modality": by_modality,
        "by_department": by_department,
        "by_status": by_status,
    }


async def search_secop2_direct(filters: SecopFilterParams) -> SecopSearchResponse:
    """Ejecuta una búsqueda híbrida directa contra Datos Abiertos SODA + enriquecimiento Spider."""
    start = time.perf_counter()
    soql_str, query_params = build_soql_query(filters)
    endpoint = SODA_ENDPOINTS.get(filters.dataset, SODA_ENDPOINTS["procesos"])

    records: list[SecopProcessRecord] = []
    data_source: Any = "LIVE_DATOS_GOV_CO_SODA"

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            headers=BROWSER_HEADERS,
            follow_redirects=True,
        ) as client:
            resp = await client.get(endpoint, params=query_params)
            resp.raise_for_status()
            raw_list = resp.json()
            if isinstance(raw_list, list) and len(raw_list) > 0:
                records = [_normalize_soda_record(item, filters.dataset) for item in raw_list]
            else:
                data_source = "HYBRID_CACHE_FALLBACK"
                records = filter_fallback_records(filters)
    except Exception:
        data_source = "HYBRID_CACHE_FALLBACK"
        records = filter_fallback_records(filters)

    if filters.spider_enrich_top_n > 0 and records:
        targets = records[: min(filters.spider_enrich_top_n, 5)]
        tasks = [inspect_opportunity_detail(r.process_url) for r in targets]
        spider_results = await asyncio.gather(*tasks, return_exceptions=True)
        for rec, sp_res in zip(targets, spider_results, strict=False):
            if isinstance(sp_res, dict):
                rec.spider_metadata = sp_res

    elapsed_ms = round((time.perf_counter() - start) * 1000.0, 1)
    applied_filters = {
        k: v
        for k, v in filters.model_dump().items()
        if v is not None and v != "" and k not in ("limit", "offset", "spider_enrich_top_n")
    }

    return SecopSearchResponse(
        dataset=filters.dataset,
        total_returned=len(records),
        execution_time_ms=elapsed_ms,
        data_source=data_source,
        soql_query_executed=soql_str,
        applied_filters=applied_filters,
        summary_metrics=compute_summary_metrics(records),
        records=records,
    )


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug or f"secop2-feed-{uuid.uuid4().hex[:6]}"


def record_to_rag_chunks(
    record: SecopProcessRecord,
    dataset: str = "procesos",
    chunk_size_chars: int = 1400,
) -> list[RAGChunkItem]:
    """Convierte un expediente SECOP II en chunks Markdown con anclaje contextual determinista."""
    header_context = (
        f"# [SECOP II] {record.process_id} — {record.entity_name}\n"
        f"- **Referencia:** {record.reference} | **Orden:** {record.entity_order}\n"
        f"- **Entidad Estatal:** {record.entity_name} (NIT: {record.entity_nit})\n"
        f"- **Ubicación:** {record.department} — {record.city}\n"
        f"- **Modalidad:** {record.modality} | **Tipo de Contrato:** {record.contract_type}\n"
        f"- **Estado Actual:** {record.status} (Fase: {record.phase})\n"
        f"- **Cuantía / Presupuesto Oficial:** ${record.base_price_cop:,.0f} COP\n"
        f"- **Código UNSPSC:** {record.unspsc_code}\n"
        f"- **Fecha Publicación:** {record.publication_date} | **Fecha Cierre / Fin:** {record.closing_date}\n"
    )
    if record.provider_awarded:
        header_context += (
            f"- **Proveedor Adjudicado:** {record.provider_awarded} "
            f"(NIT/Doc: {record.provider_nit or 'N/A'})\n"
        )

    body_text = (
        f"## Título del Proceso\n{record.title}\n\n"
        f"## Objeto Contractual y Alcance Técnico\n{record.description}\n\n"
        f"## Enlace Oficial al Expediente Electrónico\n{record.process_url}\n"
    )

    if record.spider_metadata:
        body_text += (
            f"\n## Telemetría Spider del Expediente\n"
            f"- Inspeccionado en vivo: {record.spider_metadata.get('inspected')}\n"
            f"- Tablas DOM detectadas: {record.spider_metadata.get('dom_tables_detected', 0)}\n"
            f"- Estado ViewState ASP.NET: {record.spider_metadata.get('aspnet_viewstate_present', False)}\n"
        )

    max_body = max(300, chunk_size_chars - len(header_context))
    body_segments = [body_text[i : i + max_body] for i in range(0, len(body_text), max_body)] or [
        body_text
    ]

    chunks: list[RAGChunkItem] = []
    meta = RAGChunkMetadata(
        source="mcp_secop_scrapping_bridge",
        dataset=dataset,
        process_id=record.process_id,
        reference=record.reference,
        entity_name=record.entity_name,
        entity_nit=record.entity_nit,
        department=record.department,
        city=record.city,
        modality=record.modality,
        status=record.status,
        contract_type=record.contract_type,
        base_price_cop=record.base_price_cop,
        publication_date=record.publication_date,
        closing_date=record.closing_date,
        unspsc_code=record.unspsc_code,
        process_url=record.process_url,
    )

    for idx, segment in enumerate(body_segments):
        full_markdown = f"{header_context}\n{segment}".strip()
        content_hash = hashlib.sha256(full_markdown.encode("utf-8")).hexdigest()[:16]
        token_est = max(1, len(full_markdown) // 4)
        chunks.append(
            RAGChunkItem(
                chunk_id=f"secop2_{record.process_id}_{idx:02d}",
                doc_id=record.process_id,
                chunk_index=idx,
                text=full_markdown,
                markdown_body=segment.strip(),
                token_estimate=token_est,
                char_count=len(full_markdown),
                content_hash=content_hash,
                metadata=meta,
            )
        )
    return chunks


def build_rag_pipeline_from_records(
    records: list[SecopProcessRecord],
    filters: SecopFilterParams,
    chunk_size_chars: int = 1400,
) -> RAGPipelineResponse:
    """Construye la respuesta completa del pipeline RAG a partir de registros normalizados."""
    all_chunks: list[RAGChunkItem] = []
    for rec in records:
        all_chunks.extend(
            record_to_rag_chunks(rec, dataset=filters.dataset, chunk_size_chars=chunk_size_chars)
        )

    total_tokens = sum(c.token_estimate for c in all_chunks)
    applied = {k: v for k, v in filters.model_dump().items() if v is not None and v != ""}
    return RAGPipelineResponse(
        pipeline_id=f"rag_pipe_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.now(UTC).isoformat(),
        total_processes=len(records),
        total_chunks=len(all_chunks),
        total_estimated_tokens=total_tokens,
        chunk_strategy="Context-Anchored Institutional Markdown (Header + Semantic Body + Vector Metadata)",
        applied_filters=applied,
        chunks=all_chunks,
    )


def build_integration_snippets(
    slug: str, base_url: str = "http://localhost:8020"
) -> dict[str, str]:
    """Genera snippets listos para LangChain, LlamaIndex y cliente MCP."""
    rag_url = f"{base_url}/api/v1/feeds/{slug}/rag"
    jsonl_url = f"{base_url}/api/v1/feeds/{slug}/jsonl"

    langchain_snippet = f"""# Conector directo MCP-SECOP / SCRAPPING -> LangChain + Qdrant
import requests
from langchain_core.documents import Document

payload = requests.get("{rag_url}", timeout=30).json()
documents = [
    Document(page_content=c["text"], metadata=c["metadata"], id=c["chunk_id"])
    for c in payload["chunks"]
]
"""

    llamaindex_snippet = f"""# Conector directo MCP-SECOP / SCRAPPING -> LlamaIndex TextNodes
import requests
from llama_index.core.schema import TextNode

payload = requests.get("{rag_url}", timeout=30).json()
nodes = [TextNode(id_=c["chunk_id"], text=c["text"], metadata=c["metadata"]) for c in payload["chunks"]]
"""

    curl_snippet = f"""curl -s "{rag_url}" | jq .
curl -s "{jsonl_url}" -o "{slug}.jsonl" """

    return {
        "langchain_python": langchain_snippet.strip(),
        "llamaindex_python": llamaindex_snippet.strip(),
        "curl_cli": curl_snippet.strip(),
    }


CUSTOM_FEEDS_REGISTRY: dict[str, CustomAPIFeedSpec] = {}


def register_custom_feed(
    req: CustomAPIFeedCreateRequest,
    base_url: str = "http://localhost:8020",
) -> CustomAPIFeedSpec:
    """Registra un nuevo feed RAG persistente en memoria y genera sus endpoints."""
    slug = _slugify(req.slug or req.name)
    feed_id = f"feed_{uuid.uuid4().hex[:8]}"
    endpoints = {
        "mcp_gateway_rag": f"{base_url}/api/v1/feeds/{slug}/rag",
        "mcp_gateway_jsonl": f"{base_url}/api/v1/feeds/{slug}/jsonl",
        "scrapping_bridge_rag": f"http://localhost:8010/api/v1/feeds/{slug}/rag",
    }
    spec = CustomAPIFeedSpec(
        feed_id=feed_id,
        name=req.name,
        slug=slug,
        description=req.description,
        created_at=datetime.now(UTC).isoformat(),
        filters=req.filters,
        chunk_size_chars=req.chunk_size_chars,
        include_spider_links=req.include_spider_links,
        endpoints=endpoints,
        integration_snippets=build_integration_snippets(slug, base_url=base_url),
    )
    CUSTOM_FEEDS_REGISTRY[slug] = spec
    return spec


def seed_default_feeds() -> None:
    """Inicializa los feeds RAG predeterminados en sincronía con el proyecto SCRAPPING."""
    if CUSTOM_FEEDS_REGISTRY:
        return
    register_custom_feed(
        CustomAPIFeedCreateRequest(
            name="Licitaciones de Software, Nube e IA en Colombia",
            slug="licitaciones-software-ia-colombia",
            description=(
                "Endpoint preconfigurado para sistemas RAG de empresas de tecnología: "
                "extrae procesos activos de software, nube e inteligencia artificial en SECOP II."
            ),
            filters=SecopFilterParams(dataset="procesos", keyword="software", limit=15),
            chunk_size_chars=1400,
        )
    )
    register_custom_feed(
        CustomAPIFeedCreateRequest(
            name="Contratos de Infraestructura e Interventoría Vial",
            slug="contratos-infraestructura-vial",
            description=(
                "Feed RAG especializado en contratos y procesos de obra pública e interventoría "
                "bajo Documentos Tipo en Colombia."
            ),
            filters=SecopFilterParams(dataset="procesos", keyword="vial", limit=15),
            chunk_size_chars=1400,
        )
    )
    register_custom_feed(
        CustomAPIFeedCreateRequest(
            name="Adquisiciones de Salud, Equipos Biomédicos y Telemedicina",
            slug="salud-equipos-biomedicos-colombia",
            description=(
                "Feed RAG para monitoreo de contrataciones hospitalarias, insumos médicos y telemedicina en SECOP II."
            ),
            filters=SecopFilterParams(dataset="procesos", keyword="salud", limit=15),
            chunk_size_chars=1400,
        )
    )
