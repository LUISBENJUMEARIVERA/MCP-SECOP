<div align="center">

# MCP SECOP II Colombia

**Servidor MCP (Model Context Protocol) e Inspector Web Suizo de Tonalidades Claras para SECOP II y Colombia Compra Eficiente, conectado en puente bidireccional con el proyecto `SCRAPPING` y generador de pipelines RAG.**

[![License: MIT](https://img.shields.io/badge/License-MIT-0D0E11.svg?style=flat-square)](./LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-0D6E52.svg?style=flat-square)](https://www.python.org/downloads/)
[![MCP SDK 2.x](https://img.shields.io/badge/MCP_Protocol-MCPServer_2.x-D9381E.svg?style=flat-square)](https://modelcontextprotocol.io/)
[![Managed with uv](https://img.shields.io/badge/Managed%20with-uv-0D0E11.svg?style=flat-square)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![Archify Showcase](https://img.shields.io/badge/Archify-Showcase_Validated-0D6E52.svg?style=flat-square)](./docs/arquitectura.html)

</div>

---

## 📖 Descripción general

**MCP SECOP II Colombia** (`mcp-secop`) es un servidor **Model Context Protocol (MCP)** de grado de producción que expone las capas técnicas del **Sistema Electrónico para la Contratación Pública (SECOP II)** y **Colombia Compra Eficiente** a cualquier agente LLM (**Claude Desktop, Cursor, Google Antigravity, OpenCode**), operando además en **puente bidireccional en vivo con el proyecto `SCRAPPING`** (`http://127.0.0.1:8010` y workspace local `../SCRAPPING`).

Incluye un **Centro de Control Web en Minimalismo Suizo Institucional de tonalidades claras** (`http://127.0.0.1:8020`) para invocar las 8 herramientas MCP desde el navegador, inspeccionar la taxonomía oficial de 6 dominios de SECOP II, lanzar el motor Spider sobre portales ASP.NET Vortal y exportar fragmentos vectoriales (`.jsonl` y Markdown contextual) listos para **Qdrant, Chroma, pgvector, LangChain y LlamaIndex**.

> 📘 La verdad técnica central —stack, decisiones, convenciones y flujo— vive en
> [`CONSTITUTION.md`](./CONSTITUTION.md).

## 📑 Tabla de contenidos

- [Descripción general](#-descripción-general)
- [Capacidades MCP (8 Tools, 4 Resources, 2 Prompts)](#-capacidades-mcp-8-tools-4-resources-2-prompts)
- [Puente Bidireccional con el proyecto SCRAPPING](#-puente-bidireccional-con-el-proyecto-scrapping)
- [Stack tecnológico](#-stack-tecnológico)
- [Primeros pasos y ejecución](#-primeros-pasos-y-ejecución)
- [Configuración en Clientes MCP](#-configuración-en-clientes-mcp)
- [Arquitectura del proyecto (Archify)](#-arquitectura-del-proyecto)
- [Estructura del repositorio](#-estructura-del-repositorio)
- [Licencia](#-licencia)

## ⚡ Capacidades MCP (8 Tools, 4 Resources, 2 Prompts)

| Código | Herramienta MCP (`Tool`) | Función Principal |
| :--- | :--- | :--- |
| `TOOL-01` | `secop_search_processes` | Búsqueda multidimensional SODA SoQL en `p6dx-8zbt` (Procesos) y `jbjy-vk9h` (Contratos) por palabra clave, entidad, NIT, departamento, modalidad, cuantía COP y código UNSPSC. |
| `TOOL-02` | `secop_spider_crawl` | Motor Spider asíncrono sobre `colombiacompra.gov.co` y `community.secop.gov.co` con detección de sesiones ASP.NET `__VIEWSTATE` y clasificación documental RAG. |
| `TOOL-03` | `secop_inspect_opportunity` | Inspector DOM profundo de expedientes `OpportunityDetail` (`noticeUID=CO1.NTC.*`), tablas contractuales y pliegos anexos. |
| `TOOL-04` | `secop_generate_rag_chunks` | Sintetizador de chunks Markdown con cabecera contextual institucional inyectada, hash SHA-256 y metadatos filtrables para bases vectoriales. |
| `TOOL-05` | `secop_get_taxonomy_map` | Catálogo estructurado de los 6 dominios y 11 enlaces principales del ecosistema SECOP II. |
| `TOOL-06` | `secop_manage_rag_feeds` | Listado y creación de feeds dinámicos (`/api/v1/feeds/{slug}/rag` y `.jsonl`) sincronizados con `SCRAPPING`. |
| `TOOL-07` | `secop_bridge_status` | Diagnóstico en tiempo real del puente HTTP (`:8010`) y detección de módulos en el workspace `../SCRAPPING`. |
| `TOOL-08` | `secop_analyze_procurement_budget` | Analítica financiera en pesos colombianos (COP), distribución por modalidad/departamento y Top 5 de procesos de mayor cuantía. |

**Recursos MCP (`Resources`)**:
- `secop://taxonomy/catalog` — Mapa completo de los 6 dominios de SECOP II.
- `secop://bridge/scrapping-status` — Estado en vivo del puente con `SCRAPPING`.
- `secop://rag/default-feeds` — Feeds RAG preconfigurados y snippets para LangChain/LlamaIndex.
- `secop://schemas/soql-dictionary` — Diccionario técnico SoQL para Datos Abiertos Colombia.

**Prompts MCP (`Prompts`)**:
- `auditoria_licitacion_secop2` — Auditoría integral legal, técnica y presupuestal de pliegos.
- `ingesta_rag_contratacion` — Orquestación de ingesta vectorial hacia Qdrant/Chroma.

## 🔗 Puente Bidireccional con el proyecto SCRAPPING

El módulo [`scrapping_bridge.py`](./src/mcp_secop/scrapping_bridge.py) conecta automáticamente este servidor MCP con el proyecto hermano **`SCRAPPING`**:
1. **Delegación HTTP en Vivo (`ONLINE_HTTP_BRIDGE`)**: Si el backend de `SCRAPPING` está activo en `http://127.0.0.1:8010`, las herramientas MCP delegan y sincronizan feeds directamente con él.
2. **Motor Híbrido Autónomo (`LOCAL_WORKSPACE_HYBRID`)**: Si `SCRAPPING` no está en ejecución por red, `mcp-secop` detecta el workspace local `../SCRAPPING` y ejecuta de forma autónoma las consultas Socrata SODA SoQL, el Spider ASP.NET y el chunker RAG sin interrupción.

## 🛠️ Stack tecnológico

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3.12+ |
| **Gestor de paquetes** | [`uv`](https://docs.astral.sh/uv/) (`uv_build` src-layout) |
| **Servidor MCP** | [`mcp` (MCPServer 2.x)](https://modelcontextprotocol.io/) |
| **Pasarela Web & UI** | FastAPI + Uvicorn + Minimalismo Suizo Institucional Claro (`#F6F6F3` / `#FFFFFF` / `#0D0E11` / `#D9381E`) |
| **Scraping & SODA** | `httpx` asíncrono + `BeautifulSoup4` + Socrata SoQL |
| **Calidad** | Ruff (lint + format) · `ty` (typecheck) · `pytest` (7/7 pruebas AAA) · `pre-commit` |
| **Arquitectura Viva** | [Archify](https://github.com/tt-a1i/archify) (`docs/arquitectura.html`) |

## 🚀 Primeros pasos y ejecución

```bash
git clone https://github.com/LUISBENJUMEARIVERA/MCP-SECOP.git
cd MCP-SECOP

# 1. Sincronizar entorno determinista con uv
uv sync

# 2. Verificar el puente con el proyecto SCRAPPING
uv run mcp-secop --check-bridge

# 3. Iniciar el Centro de Control Web Suizo (Tonalidades Claras) en http://127.0.0.1:8020
uv run mcp-secop --web

# 4. Ejecutar el servidor MCP en modo STDIO (para Claude Desktop / Cursor / Antigravity)
uv run mcp-secop --transport stdio

# 5. Ejecutar verificación completa (Ruff + ty + Pytest)
make check
```

## 🔌 Configuración en Clientes MCP

Agrega este bloque en tu archivo `claude_desktop_config.json` o configuración MCP de **Cursor / Google Antigravity / OpenCode**:

```json
{
  "mcpServers": {
    "mcp-secop-colombia": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/Users/luisa/OneDrive/Escritorio/SKILLS/mcp secop",
        "run",
        "mcp-secop"
      ],
      "env": {
        "SCRAPPING_API_URL": "http://127.0.0.1:8010"
      }
    }
  }
}
```

## 🗺️ Arquitectura del proyecto

Mapa de arquitectura interactivo autocontenido generado y validado con [Archify](https://github.com/tt-a1i/archify) en perfil `showcase`:
- **Visor Interactivo HTML**: [`docs/arquitectura.html`](./docs/arquitectura.html)
- **Fuente Declarativa JSON**: [`docs/arquitectura.json`](./docs/arquitectura.json)

## 📂 Estructura del repositorio

```text
mcp-secop/
├── src/mcp_secop/
│   ├── __init__.py          # Metadatos del paquete
│   ├── models.py            # Modelos Pydantic v2 (SODA, Spider, RAG, Bridge)
│   ├── taxonomy_spider.py   # Catálogo de 6 dominios SECOP II + Spider ASP.NET
│   ├── secop_engine.py      # Constructor SoQL, analítica COP y chunker RAG
│   ├── scrapping_bridge.py  # Puente bidireccional hacia el proyecto SCRAPPING (:8010)
│   ├── mcp_server.py        # Servidor MCP (8 Tools, 4 Resources, 2 Prompts)
│   ├── ui_template.py       # Interfaz Web en Minimalismo Suizo Claro
│   ├── web_app.py           # Pasarela HTTP FastAPI (:8020)
│   └── cli.py               # CLI unificada (mcp-secop)
├── tests/
│   └── test_mcp_secop.py    # Pruebas automatizadas pytest (patrón AAA)
├── docs/
│   ├── arquitectura.json    # Fuente tipada Archify
│   └── arquitectura.html    # Artefacto interactivo Archify
├── CONSTITUTION.md          # Fuente única de verdad del proyecto
├── AGENTS.md                # Contexto operativo para agentes IA
├── Makefile                 # Automatización de tareas
├── pyproject.toml           # Configuración uv, Ruff, pytest y scripts
└── uv.lock                  # Lockfile determinista versionado
```

## 📄 Licencia

Distribuido bajo la [Licencia MIT](./LICENSE).

---

<div align="center">
<sub>Desarrollado por <strong>Ing. Luis Benjumea Rivera</strong> — 2026</sub>
</div>
