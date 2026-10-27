# CONSTITUTION — MCP SECOP II Colombia

> **Verdad central del proyecto.** Este documento define el propósito, el stack, la
> estructura, las convenciones y el flujo de trabajo de `MCP SECOP II Colombia`. Si algo aquí
> contradice al código, el código manda **y este archivo se actualiza**.

> ⚠️ **Directiva de mantenimiento:** cada vez que se realicen cambios significativos
> (nuevas funcionalidades, cambios arquitectónicos, adición de clases/módulos o ajustes
> de tecnologías), **se debe actualizar este archivo en el mismo commit** para mantener
> la verdad central del proyecto bien documentada.

---

## 0. Identidad del proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | MCP SECOP II Colombia |
| **Descripción** | Servidor MCP (Model Context Protocol) e Inspector Web Suizo para SECOP II y Colombia Compra Eficiente, conectado en puente bidireccional con el proyecto SCRAPPING y generador de pipelines RAG. |
| **Repositorio** | https://github.com/LUISBENJUMEARIVERA/MCP-SECOP |
| **Autoría** | Ing. Luis Benjumea Rivera — luisantoniobenjumeaia@gmail.com |
| **Licencia** | MIT |
| **Rama principal** | `main` |
| **Estado** | Producción Operativa v1.0.0 ✅ |

## 1. Propósito y no-propósito

### Propósito

Exponer el ecosistema de contratación pública colombiana (**SECOP II** y **Colombia Compra Eficiente**) como un servidor oficial **Model Context Protocol (MCP)** (`mcp-secop-colombia`) con 8 herramientas, 4 recursos y 2 prompts auditables, conectado en **puente bidireccional con el proyecto hermano `SCRAPPING`** (`http://127.0.0.1:8010` y workspace `../SCRAPPING`), acompañado de un **Centro de Control Web en Minimalismo Suizo Institucional de tonalidades claras** (`:8020`) y un generador de chunks semánticos listos para RAG (Qdrant, Chroma, pgvector, LangChain, LlamaIndex).

### No-propósito

No reemplaza el portal transaccional autenticado de presentación de ofertas de Vortal/SECOP II ni almacena credenciales privadas de proveedores estatales. Opera sobre fuentes públicas oficiales (Socrata SODA `p6dx-8zbt` / `jbjy-vk9h`, portales públicos de Colombia Compra Eficiente y expedientes públicos `OpportunityDetail`).

## 2. Alcance

### Dentro del alcance

- **Servidor MCP (`FastMCP`)** compatible con transporte `stdio` y `sse` para Claude Desktop, Cursor, Google Antigravity y OpenCode.
- **8 Herramientas MCP (`Tools`)**:
  1. `secop_search_processes`: Filtrado multidimensional SODA SoQL (`procesos` y `contratos`) con enriquecimiento Spider opcional.
  2. `secop_spider_crawl`: Motor Spider asíncrono con detección de tokens ASP.NET `__VIEWSTATE` y clasificación documental RAG.
  3. `secop_inspect_opportunity`: Inspector profundo de expedientes `OpportunityDetail` (`noticeUID=CO1.NTC.*`).
  4. `secop_generate_rag_chunks`: Generador de fragmentos Markdown con cabecera contextual institucional inyectada y hash SHA-256.
  5. `secop_get_taxonomy_map`: Catálogo estructurado de los 6 dominios y 11 enlaces principales de SECOP II.
  6. `secop_manage_rag_feeds`: Creación y listado de feeds dinámicos (`/api/v1/feeds/{slug}/rag` y `.jsonl`) sincronizados con `SCRAPPING`.
  7. `secop_bridge_status`: Diagnóstico en tiempo real del puente HTTP (`:8010`) y vinculación en disco con el proyecto `SCRAPPING`.
  8. `secop_analyze_procurement_budget`: Analítica presupuestal consolidada en COP y Top 5 de procesos de mayor cuantía.
- **4 Recursos MCP (`Resources`)**: `secop://taxonomy/catalog`, `secop://bridge/scrapping-status`, `secop://rag/default-feeds` y `secop://schemas/soql-dictionary`.
- **2 Prompts MCP (`Prompts`)**: `auditoria_licitacion_secop2` e `ingesta_rag_contratacion`.
- **Centro de Control Web Suizo (Tonalidades Claras)**: Pasarela FastAPI en `:8020` diseñada bajo las directrices de `vanguard-frontend-engine` (paleta papel arquitectónico `#F6F6F3`, celdas `#FFFFFF`, tinta `#0D0E11`, acento bermellón `#D9381E` y esmeralda `#0D6E52`).
- **Diagrama de Arquitectura Interactivo (`Archify`)**: Especificación declarativa en `docs/arquitectura.json` y artefacto autocontenido en `docs/arquitectura.html`.

### Fuera del alcance (por ahora)

- Radicación automatizada de ofertas electrónicas con firma digital certificada dentro de sesiones privadas STS de SECOP II.

## 3. Stack técnico

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3.12+ |
| **Gestor de paquetes y entorno** | [`uv`](https://docs.astral.sh/uv/) |
| **Build backend** | `uv_build` (src-layout) |
| **Paquete Python** | `mcp_secop` |
| **Protocolo de Agentes** | [`mcp` (FastMCP SDK)](https://modelcontextprotocol.io/) |
| **Pasarela Web & API** | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| **Motor HTTP & Spider DOM** | `httpx` (Async) + `BeautifulSoup4` |
| **Tipado estático** | [`ty`](https://github.com/astral-sh/ty) |
| **Testing** | [`pytest`](https://docs.pytest.org/) + `pytest-asyncio` |
| **Linting / Formato** | [Ruff](https://docs.astral.sh/ruff/) |
| **Pre-commit** | [pre-commit](https://pre-commit.com) |
| **CI/CD** | [GitHub Actions](.github/workflows/ci.yml) |
| **Diagramas de arquitectura** | [Archify](https://github.com/tt-a1i/archify) (`docs/arquitectura.html`) |
| **Dependencias automáticas** | [Dependabot](.github/dependabot.yml) |

> ⚠️ **Regla dura:** toda gestión de dependencias y entornos pasa por `uv`. Está
> **prohibido** `pip` y `requirements.txt`.

## 4. Estructura del repositorio

```text
mcp-secop/
├── src/mcp_secop/
│   ├── __init__.py          # Versión y metadatos del paquete
│   ├── models.py            # Esquemas Pydantic v2 (SODA, Spider, RAG, Puente SCRAPPING)
│   ├── taxonomy_spider.py   # Catálogo de 6 dominios SECOP II y Spider asíncrono ASP.NET
│   ├── secop_engine.py      # Constructor SoQL, agregador COP y chunker RAG contextual
│   ├── scrapping_bridge.py  # Conector bidireccional HTTP (:8010) y local (../SCRAPPING)
│   ├── mcp_server.py        # Servidor FastMCP (8 Tools, 4 Resources, 2 Prompts)
│   ├── ui_template.py       # Interfaz Web en Minimalismo Suizo Institucional Claro
│   ├── web_app.py           # Pasarela FastAPI (:8020) y endpoints REST/JSONL
│   └── cli.py               # CLI unificada (mcp-secop y mcp-secop-web)
├── tests/
│   └── test_mcp_secop.py    # Suite de pruebas unitarias e integración (patrón AAA)
├── docs/
│   ├── arquitectura.json    # Fuente declarativa del diagrama Archify
│   └── arquitectura.html    # Visor interactivo autocontenido Archify
├── .github/                 # Gobernanza (PR/issue templates, CI, Dependabot, labels)
├── .opencode/rules/         # Reglas para agentes (tgrep)
├── AGENTS.md                # Contexto operativo para agentes LLM
├── CONSTITUTION.md          # Este archivo — verdad central del proyecto
├── README.md                # Puerta de entrada pública
├── CONTRIBUTING.md          # Guía de contribución
├── CODE_OF_CONDUCT.md       # Código de conducta
├── Makefile                 # Interfaz de comandos automatizados
├── pyproject.toml           # Metadatos y dependencias gestionadas con uv
├── uv.lock                  # Lockfile determinista (versionado)
├── .python-version          # Versión de Python fijada (3.12)
└── .pre-commit-config.yaml  # Hooks de calidad automatizada
```

## 5. Convenciones de código

- **Estilo:** [PEP 8](https://peps.python.org/pep-0008/) y [PEP 257](https://peps.python.org/pep-0257/), impuesto por **Ruff** (`line-length = 100`, comillas dobles).
- **Tipado:** anotaciones estrictas en funciones y modelos Pydantic v2.
- **Nomenclatura:** `snake_case` (funciones/variables), `PascalCase` (clases), `UPPER_CASE` (constantes).
- **Pruebas:** `pytest` con el patrón **AAA** (*Arrange · Act · Assert*).
- **Invariantes del dominio SECOP II:**
  - Todo chunk RAG debe llevar inyectada la cabecera contextual institucional (`process_id`, `entity_name`, `entity_nit`, `modality`, `base_price_cop`, `unspsc_code`) para evitar fragmentos huérfanos en búsquedas vectoriales.
  - Toda consulta SoQL sanitiza comillas simples y soporta degradación elegante (`HYBRID_CACHE_FALLBACK`) si la pasarela de Datos Abiertos presenta latencia o mantenimiento.
  - La interfaz web respeta estrictamente el **Minimalismo Suizo Institucional de tonalidades claras** (`#F6F6F3` / `#FFFFFF` / `#0D0E11` / `#D9381E`), sin degradados púrpura-azul ni emojis.

## 6. Calidad y automatización

| Herramienta | Rol | Comando |
|-------------|-----|---------|
| `uv` | Entornos y dependencias | `uv sync` |
| Ruff | Lint + formato | `make lint` / `make format` |
| `ty` | Verificación de tipos | `make typecheck` |
| `pytest` | Pruebas automatizadas | `make test` |
| `pre-commit` | Hooks antes de cada commit | `make pre-commit` |
| Servidor MCP | Ejecución STDIO | `uv run mcp-secop` |
| Centro Web Suizo | Ejecución HTTP `:8020` | `uv run mcp-secop --web` |

## 7. Repositorio y Git

- **Remoto (HTTPS/SSH):** `https://github.com/LUISBENJUMEARIVERA/MCP-SECOP.git`
- **Rama principal:** `main`
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).

## 8. Flujo diario (commit + push)

```bash
git status
make check
git add -A
git commit -m "feat: mensaje descriptivo"
git push -u origin main
```

## 9. Historial de decisiones técnicas

| Fecha | Decisión | Motivo |
|-------|----------|--------|
| 2026-10-27 | Adoptar `uv` + `src-layout` (`src/mcp_secop`) bajo `jan-project-standard` | Reproducibilidad determinista, empaquetado limpio y gobernanza auditable |
| 2026-10-27 | Implementar servidor MCP con `FastMCP` + Pasarela FastAPI en `:8020` | Soportar tanto clientes MCP nativos (`stdio`/`sse`) como inspección interactiva en navegador y REST/JSONL |
| 2026-10-27 | Construir `ScrappingBridgeClient` hacia `SCRAPPING` (`:8010` y `../SCRAPPING`) | Permitir delegación en vivo al proyecto `SCRAPPING` y sincronización de feeds RAG con fallback autónomo |
| 2026-10-27 | Diseñar Centro de Control Web en Minimalismo Suizo Claro (`vanguard-frontend-engine`) | Tonalidades claras de alto contraste (`#F6F6F3`, `#FFFFFF`, `#0D0E11`, `#D9381E`), tipografía `Space Grotesk` + `JetBrains Mono` |
| 2026-10-27 | Documentar arquitectura de runtime con `Archify` en `docs/arquitectura.{json,html}` | Documentación viva verificada automáticamente en perfil `showcase` |

## 10. Notas y tareas pendientes

- [x] Estandarizar estructura con `jan-project-standard` y poblar `CONSTITUTION.md`.
- [x] Implementar las 8 herramientas MCP, 4 recursos y 2 prompts sobre SECOP II.
- [x] Conectar el puente bidireccional con el proyecto `SCRAPPING`.
- [x] Construir la interfaz web profesional de tonalidades claras (Minimalismo Suizo Institucional).
- [x] Generar y validar el diagrama de arquitectura interactivo con `Archify` (`docs/arquitectura.html`).
- [x] Ejecutar suite de pruebas (`pytest`), linter (`ruff`) y verificador de tipos (`ty`).
- [x] Publicar en `https://github.com/LUISBENJUMEARIVERA/MCP-SECOP`.
