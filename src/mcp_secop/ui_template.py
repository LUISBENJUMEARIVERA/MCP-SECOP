"""Plantilla HTML autocontenida del Centro de Control Web MCP SECOP II (Minimalismo Suizo Claro)."""

from __future__ import annotations

SWISS_LIGHT_MCP_UI_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MCP SECOP II COLOMBIA // Centro de Control &amp; Puente SCRAPPING</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg-paper: #F6F6F3;
      --bg-cell: #FFFFFF;
      --bg-subtle: #ECEAE3;
      --bg-hover: #F0EFEA;
      --ink-primary: #0D0E11;
      --ink-secondary: #3E4149;
      --ink-muted: #5C606A;
      --border-strong: #141519;
      --border-subtle: #CFCBC1;
      --accent-vermilion: #D9381E;
      --accent-vermilion-soft: #FDECE9;
      --accent-emerald: #0D6E52;
      --accent-emerald-soft: #E6F4EF;
      --accent-amber: #9A4B06;
      --accent-amber-soft: #FEF3E2;
      --font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html, body {
      background-color: var(--bg-paper);
      color: var(--ink-primary);
      font-family: var(--font-display);
      font-size: 16px;
      line-height: 1.5;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }

    :focus-visible {
      outline: 3px solid var(--accent-vermilion);
      outline-offset: 2px;
    }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }

    /* Top Telemetry Strip */
    .telemetry-bar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      padding: 8px 24px;
      background-color: var(--bg-cell);
      border-bottom: 1px solid var(--border-strong);
      font-family: var(--font-mono);
      font-size: 12px;
      gap: 12px;
    }

    .telemetry-group {
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 3px 8px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      border: 1px solid var(--border-strong);
      background: var(--bg-paper);
      color: var(--ink-primary);
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    .badge-emerald {
      background: var(--accent-emerald-soft);
      color: var(--accent-emerald);
      border-color: var(--accent-emerald);
    }

    .badge-vermilion {
      background: var(--accent-vermilion-soft);
      color: var(--accent-vermilion);
      border-color: var(--accent-vermilion);
    }

    .badge-amber {
      background: var(--accent-amber-soft);
      color: var(--accent-amber);
      border-color: var(--accent-amber);
    }

    .status-dot {
      width: 7px;
      height: 7px;
      background-color: currentColor;
      display: inline-block;
    }

    /* Architectural Shell */
    .shell {
      max-width: 1560px;
      margin: 0 auto;
      border-left: 1px solid var(--border-strong);
      border-right: 1px solid var(--border-strong);
      background-color: var(--bg-paper);
      min-height: calc(100vh - 38px);
    }

    /* Editorial Hero Header */
    .hero-grid {
      display: grid;
      grid-template-columns: 1.6fr 1fr;
      border-bottom: 1px solid var(--border-strong);
      background-color: var(--bg-cell);
    }

    @media (max-width: 1024px) {
      .hero-grid {
        grid-template-columns: 1fr;
      }
    }

    .hero-main {
      padding: 32px 28px;
      border-right: 1px solid var(--border-strong);
    }

    .hero-kicker {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--accent-vermilion);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .hero-title {
      font-size: clamp(1.85rem, 3vw, 2.75rem);
      font-weight: 700;
      letter-spacing: -0.03em;
      line-height: 1.08;
      color: var(--ink-primary);
      margin-bottom: 14px;
    }

    .hero-lead {
      font-size: 1rem;
      color: var(--ink-secondary);
      max-width: 74ch;
      margin-bottom: 20px;
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .hero-metrics {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
    }

    .metric-cell {
      padding: 20px 22px;
      border-bottom: 1px solid var(--border-subtle);
      border-right: 1px solid var(--border-subtle);
      background-color: var(--bg-paper);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .metric-cell:nth-child(2n) {
      border-right: none;
    }

    .metric-cell:nth-child(n+3) {
      border-bottom: none;
    }

    .metric-label {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--ink-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .metric-value {
      font-family: var(--font-mono);
      font-size: 1.65rem;
      font-weight: 700;
      color: var(--ink-primary);
      margin: 6px 0 2px;
    }

    .metric-sub {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--ink-secondary);
    }

    /* Navigation Tabs */
    .nav-tabs {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      border-bottom: 1px solid var(--border-strong);
      background-color: var(--bg-subtle);
    }

    @media (max-width: 900px) {
      .nav-tabs {
        grid-template-columns: 1fr 1fr;
      }
    }

    .tab-btn {
      min-height: 52px;
      padding: 12px 18px;
      background: transparent;
      border: none;
      border-right: 1px solid var(--border-strong);
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--ink-secondary);
      text-align: left;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: background-color 120ms ease, color 120ms ease;
    }

    .tab-btn:last-child {
      border-right: none;
    }

    .tab-btn:hover {
      background-color: var(--bg-hover);
      color: var(--ink-primary);
    }

    .tab-btn.active {
      background-color: var(--bg-cell);
      color: var(--ink-primary);
      box-shadow: inset 0 -3px 0 var(--accent-vermilion);
    }

    /* Buttons & Controls */
    .btn {
      min-height: 44px;
      padding: 10px 18px;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      border: 1px solid var(--border-strong);
      background-color: var(--bg-cell);
      color: var(--ink-primary);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      transition: transform 100ms ease, background-color 120ms ease;
    }

    .btn:hover {
      background-color: var(--bg-subtle);
    }

    .btn:active {
      transform: translateY(1px);
    }

    .btn-primary {
      background-color: var(--accent-vermilion);
      color: #FFFFFF;
      border-color: var(--border-strong);
    }

    .btn-primary:hover {
      background-color: #B82B14;
      color: #FFFFFF;
    }

    .btn-dark {
      background-color: var(--ink-primary);
      color: #FFFFFF;
    }

    .btn-dark:hover {
      background-color: #272A30;
      color: #FFFFFF;
    }

    /* Panels */
    .panel {
      display: none;
    }

    .panel.active {
      display: block;
    }

    /* Workbench Layout (Panel 1) */
    .workbench-grid {
      display: grid;
      grid-template-columns: 360px 1fr;
      min-height: 680px;
    }

    @media (max-width: 1024px) {
      .workbench-grid {
        grid-template-columns: 1fr;
      }
    }

    .tool-rail {
      border-right: 1px solid var(--border-strong);
      background-color: var(--bg-paper);
    }

    .rail-header {
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-strong);
      background-color: var(--bg-subtle);
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--ink-secondary);
    }

    .tool-item {
      width: 100%;
      text-align: left;
      padding: 14px 18px;
      border: none;
      border-bottom: 1px solid var(--border-subtle);
      background: var(--bg-paper);
      cursor: pointer;
      display: block;
      transition: background-color 120ms ease;
    }

    .tool-item:hover {
      background-color: var(--bg-cell);
    }

    .tool-item.active {
      background-color: var(--bg-cell);
      border-left: 4px solid var(--accent-vermilion);
    }

    .tool-code {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--accent-vermilion);
    }

    .tool-name {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--ink-primary);
      margin: 2px 0 4px;
    }

    .tool-desc {
      font-size: 12px;
      color: var(--ink-secondary);
      line-height: 1.35;
    }

    .tool-workspace {
      display: flex;
      flex-direction: column;
      background-color: var(--bg-cell);
    }

    .form-bar {
      padding: 20px 24px;
      border-bottom: 1px solid var(--border-strong);
      background-color: var(--bg-paper);
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 14px;
      margin-top: 12px;
      margin-bottom: 16px;
    }

    .field-group {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }

    .field-group label {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--ink-secondary);
      text-transform: uppercase;
    }

    .input-ctrl {
      min-height: 42px;
      padding: 8px 12px;
      font-family: var(--font-mono);
      font-size: 13px;
      border: 1px solid var(--border-strong);
      background-color: var(--bg-cell);
      color: var(--ink-primary);
      width: 100%;
    }

    .results-split {
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      flex: 1;
    }

    @media (max-width: 1180px) {
      .results-split {
        grid-template-columns: 1fr;
      }
    }

    .visual-pane {
      padding: 20px 24px;
      border-right: 1px solid var(--border-strong);
      background-color: var(--bg-cell);
      overflow-y: auto;
      max-height: 640px;
    }

    .json-pane {
      padding: 20px 24px;
      background-color: var(--bg-paper);
      overflow-y: auto;
      max-height: 640px;
    }

    .pane-title {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--ink-muted);
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    pre.code-block {
      font-family: var(--font-mono);
      font-size: 12px;
      line-height: 1.45;
      background-color: var(--bg-cell);
      border: 1px solid var(--border-strong);
      padding: 14px;
      overflow-x: auto;
      color: var(--ink-primary);
      white-space: pre-wrap;
      word-break: break-word;
    }

    /* Data Cards inside Visual Pane */
    .record-card {
      border: 1px solid var(--border-strong);
      background-color: var(--bg-paper);
      padding: 14px 16px;
      margin-bottom: 12px;
    }

    .record-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 10px;
      margin-bottom: 6px;
      font-family: var(--font-mono);
      font-size: 12px;
    }

    .record-id {
      font-weight: 700;
      color: var(--accent-vermilion);
    }

    .record-price {
      font-weight: 700;
      color: var(--accent-emerald);
      background: var(--accent-emerald-soft);
      padding: 2px 6px;
      border: 1px solid var(--accent-emerald);
    }

    .record-title {
      font-size: 15px;
      font-weight: 700;
      color: var(--ink-primary);
      margin-bottom: 6px;
    }

    .record-meta {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--ink-secondary);
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 8px;
    }

    /* Section Grid for Panels 2, 3, 4 */
    .section-pad {
      padding: 28px;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }

    .grid-3 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 20px;
    }

    @media (max-width: 960px) {
      .grid-2 {
        grid-template-columns: 1fr;
      }
    }

    .swiss-box {
      border: 1px solid var(--border-strong);
      background-color: var(--bg-cell);
      padding: 20px;
    }

    .swiss-box-title {
      font-size: 1.15rem;
      font-weight: 700;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .table-clean {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-mono);
      font-size: 12px;
      margin-top: 10px;
    }

    .table-clean th, .table-clean td {
      border: 1px solid var(--border-subtle);
      padding: 8px 10px;
      text-align: left;
    }

    .table-clean th {
      background-color: var(--bg-subtle);
      color: var(--ink-primary);
      font-weight: 700;
      text-transform: uppercase;
    }

    .footer-bar {
      padding: 16px 24px;
      border-top: 1px solid var(--border-strong);
      background-color: var(--bg-cell);
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--ink-secondary);
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }
  </style>
</head>
<body>
  <header class="telemetry-bar" role="banner">
    <div class="telemetry-group">
      <span class="badge badge-vermilion">
        <span class="status-dot"></span>
        MCP PROTOCOL v2025.1 // FASTMCP
      </span>
      <span><strong>SERVER:</strong> mcp-secop-colombia</span>
      <span><strong>TRANSPORTS:</strong> STDIO · SSE · HTTP REST</span>
    </div>
    <div class="telemetry-group">
      <span id="bridge-pill" class="badge badge-emerald">
        <span class="status-dot"></span>
        PUENTE SCRAPPING: VERIFICANDO...
      </span>
      <a href="/arquitectura.html" target="_blank" rel="noopener" class="badge" style="text-decoration:none;">
        DIAGRAMA ARCHIFY ↗
      </a>
      <a href="/docs" target="_blank" rel="noopener" class="badge" style="text-decoration:none;">
        OPENAPI 3.1 ↗
      </a>
    </div>
  </header>

  <main class="shell">
    <!-- Hero Section -->
    <section class="hero-grid" aria-label="Tesis del Servidor MCP SECOP II">
      <div class="hero-main">
        <div class="hero-kicker">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          REPÚBLICA DE COLOMBIA · COLOMBIA COMPRA EFICIENTE · MODEL CONTEXT PROTOCOL
        </div>
        <h1 class="hero-title">MCP SECOP II &amp; Puente Híbrido SCRAPPING</h1>
        <p class="hero-lead">
          Servidor MCP estandarizado que conecta agentes de IA (Claude Desktop, Cursor, Antigravity, OpenCode)
          con la contratación pública colombiana en tiempo real: consultas Socrata SODA SoQL
          (<code>p6dx-8zbt</code> / <code>jbjy-vk9h</code>), motor Spider asíncrono sobre portales
          ASP.NET Vortal y generación de chunks contextuales enlazados al proyecto <strong>SCRAPPING</strong>.
        </p>
        <div class="hero-actions">
          <button type="button" class="btn btn-primary" onclick="runSelectedTool()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            Ejecutar Herramienta MCP Activa
          </button>
          <button type="button" class="btn" onclick="switchTab('tab-bridge')">
            Inspeccionar Puente SCRAPPING
          </button>
          <a href="/arquitectura.html" target="_blank" rel="noopener" class="btn btn-dark">
            Abrir Mapa de Arquitectura (Archify)
          </a>
        </div>
      </div>

      <div class="hero-metrics">
        <div class="metric-cell">
          <span class="metric-label">HERRAMIENTAS MCP EXPUESTAS</span>
          <div class="metric-value" id="metric-tools">8 TOOLS</div>
          <span class="metric-sub">4 Resources · 2 Prompts Auditables</span>
        </div>
        <div class="metric-cell">
          <span class="metric-label">ESTADO PUENTE SCRAPPING</span>
          <div class="metric-value" id="metric-bridge">ACTIVO</div>
          <span class="metric-sub" id="metric-bridge-sub">Sincronizado con ../SCRAPPING</span>
        </div>
        <div class="metric-cell">
          <span class="metric-label">TAXONOMÍA SECOP II INDEXADA</span>
          <div class="metric-value">6 DOMINIOS</div>
          <span class="metric-sub">11 Enlaces Oficiales + SODA + OCDS</span>
        </div>
        <div class="metric-cell">
          <span class="metric-label">FEEDS DINÁMICOS PARA RAG</span>
          <div class="metric-value" id="metric-feeds">3 FEEDS</div>
          <span class="metric-sub">Markdown Anclado + Stream JSONL</span>
        </div>
      </div>
    </section>

    <!-- Navigation Tabs -->
    <nav class="nav-tabs" role="tablist" aria-label="Secciones del Centro de Control MCP">
      <button type="button" class="tab-btn active" id="btn-tab-tools" role="tab" aria-selected="true" onclick="switchTab('tab-tools')">
        <span>01 // CONSOLA DE HERRAMIENTAS MCP (8)</span>
        <span>[EJECUTAR]</span>
      </button>
      <button type="button" class="tab-btn" id="btn-tab-bridge" role="tab" aria-selected="false" onclick="switchTab('tab-bridge')">
        <span>02 // PUENTE PROYECTO SCRAPPING</span>
        <span>[:8010]</span>
      </button>
      <button type="button" class="tab-btn" id="btn-tab-taxonomy" role="tab" aria-selected="false" onclick="switchTab('tab-taxonomy')">
        <span>03 // TAXONOMÍA SECOP II &amp; SPIDER</span>
        <span>[6 DOMINIOS]</span>
      </button>
      <button type="button" class="tab-btn" id="btn-tab-clients" role="tab" aria-selected="false" onclick="switchTab('tab-clients')">
        <span>04 // CLIENTES MCP &amp; ARQUITECTURA</span>
        <span>[JSON CONFIG]</span>
      </button>
    </nav>

    <!-- TAB 01: MCP TOOLS WORKBENCH -->
    <section id="tab-tools" class="panel active" role="tabpanel">
      <div class="workbench-grid">
        <aside class="tool-rail" aria-label="Catálogo de herramientas MCP">
          <div class="rail-header">CATÁLOGO DE HERRAMIENTAS MCP (SELECCIONA UNA)</div>
          <div id="tools-list-container"></div>
        </aside>

        <div class="tool-workspace">
          <div class="form-bar">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
              <div>
                <span class="badge badge-vermilion" id="active-tool-code">TOOL-01</span>
                <strong style="font-family:var(--font-mono); font-size:15px; margin-left:8px;" id="active-tool-name">secop_search_processes</strong>
              </div>
              <span style="font-family:var(--font-mono); font-size:12px; color:var(--ink-secondary);" id="active-tool-latency">Listo para invocación JSON-RPC</span>
            </div>
            <p style="font-size:13px; color:var(--ink-secondary); margin-top:6px;" id="active-tool-desc"></p>

            <form id="mcp-tool-form" onsubmit="event.preventDefault(); runSelectedTool();">
              <div class="form-grid" id="dynamic-form-fields"></div>
              <div style="display:flex; gap:10px; flex-wrap:wrap;">
                <button type="submit" class="btn btn-primary" id="btn-execute-tool">
                  Invocar Herramienta MCP Ahora
                </button>
                <button type="button" class="btn" onclick="resetToolDefaults()">
                  Restaurar Parámetros Base
                </button>
              </div>
            </form>
          </div>

          <div class="results-split">
            <div class="visual-pane">
              <div class="pane-title">
                <span>VISTA ESTRUCTURADA DE RESULTADOS</span>
                <span class="badge" id="visual-summary-badge">SIN EJECUTAR</span>
              </div>
              <div id="visual-results-container"></div>
            </div>
            <div class="json-pane">
              <div class="pane-title">
                <span>RESPUESTA MCP JSON-RPC ESTRUCTURADA</span>
                <button type="button" class="badge" style="cursor:pointer;" onclick="copyJsonOutput()">COPIAR JSON</button>
              </div>
              <pre class="code-block" id="json-results-output">// Selecciona y ejecuta una herramienta MCP para inspeccionar su carga útil JSON.</pre>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 02: SCRAPPING PROJECT BRIDGE -->
    <section id="tab-bridge" class="panel" role="tabpanel">
      <div class="section-pad">
        <div class="grid-2">
          <div class="swiss-box">
            <div class="swiss-box-title">
              <span>Estado del Puente Bidireccional SCRAPPING</span>
              <button type="button" class="btn" onclick="refreshBridgeStatus()">Verificar Conexión</button>
            </div>
            <p style="font-size:13px; color:var(--ink-secondary); margin-bottom:14px;">
              El servidor <strong>MCP-SECOP</strong> detecta automáticamente el proyecto hermano
              <code>SCRAPPING</code> tanto por red (<code>http://127.0.0.1:8010</code>) como en el sistema de archivos local,
              compartiendo feeds RAG, taxonomía y motor híbrido SODA SoQL + Spider.
            </p>
            <table class="table-clean" id="bridge-status-table">
              <tbody></tbody>
            </table>
          </div>

          <div class="swiss-box">
            <div class="swiss-box-title">
              <span>Crear Nuevo Feed RAG Sincronizado</span>
              <span class="badge badge-emerald">MCP + SCRAPPING</span>
            </div>
            <p style="font-size:13px; color:var(--ink-secondary); margin-bottom:14px;">
              Publica un nuevo endpoint de ingesta vectorial (<code>/api/v1/feeds/{slug}/rag</code> y <code>.jsonl</code>)
              accesible desde agentes MCP, LangChain y LlamaIndex.
            </p>
            <form onsubmit="event.preventDefault(); createNewFeedFromUI();">
              <div class="form-grid" style="grid-template-columns: 1fr 1fr;">
                <div class="field-group">
                  <label for="feed-name-input">Nombre del Feed RAG</label>
                  <input id="feed-name-input" class="input-ctrl" type="text" value="Ciberseguridad y SOC en Entidades Estatales" required />
                </div>
                <div class="field-group">
                  <label for="feed-kw-input">Palabra Clave (SoQL Keyword)</label>
                  <input id="feed-kw-input" class="input-ctrl" type="text" value="ciberseguridad" required />
                </div>
                <div class="field-group">
                  <label for="feed-dep-input">Departamento (Opcional)</label>
                  <input id="feed-dep-input" class="input-ctrl" type="text" placeholder="Ej. Valle del Cauca" />
                </div>
                <div class="field-group">
                  <label for="feed-chunk-input">Tamaño Máximo de Chunk (Chars)</label>
                  <input id="feed-chunk-input" class="input-ctrl" type="number" value="1400" min="400" max="4000" />
                </div>
              </div>
              <button type="submit" class="btn btn-primary">Publicar y Sincronizar Feed RAG</button>
            </form>
          </div>
        </div>

        <div class="swiss-box" style="margin-top:20px;">
          <div class="swiss-box-title">
            <span>Feeds RAG Activos &amp; Endpoints Compartidos</span>
            <span class="badge" id="feeds-count-badge">CARGANDO...</span>
          </div>
          <div id="feeds-list-container" class="grid-3" style="margin-top:14px;"></div>
        </div>
      </div>
    </section>

    <!-- TAB 03: SECOP II TAXONOMY & SPIDER -->
    <section id="tab-taxonomy" class="panel" role="tabpanel">
      <div class="section-pad">
        <div style="margin-bottom:20px; display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:12px;">
          <div>
            <h2 style="font-size:1.35rem; font-weight:700;">Mapa Taxonómico Oficial de SECOP II (6 Dominios / 11 Enlaces)</h2>
            <p style="font-size:13px; color:var(--ink-secondary);">
              Haz clic en <strong>Rastrear con Spider MCP</strong> sobre cualquier enlace para inspeccionar su DOM, cabeceras HTTP y sesión ASP.NET <code>__VIEWSTATE</code>.
            </p>
          </div>
        </div>
        <div id="taxonomy-container" class="grid-2"></div>
      </div>
    </section>

    <!-- TAB 04: MCP CLIENT CONFIGS & ARCHIFY -->
    <section id="tab-clients" class="panel" role="tabpanel">
      <div class="section-pad">
        <div class="grid-2">
          <div class="swiss-box">
            <div class="swiss-box-title">
              <span>Configuración para Claude Desktop / Cursor / Antigravity</span>
              <span class="badge badge-vermilion">STDIO TRANSPORT</span>
            </div>
            <p style="font-size:13px; color:var(--ink-secondary); margin-bottom:12px;">
              Agrega este bloque en tu archivo <code>mcp_config.json</code> o <code>claude_desktop_config.json</code> para usar el servidor con <code>uv</code>:
            </p>
            <pre class="code-block" id="client-config-stdio">{
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
}</pre>
          </div>

          <div class="swiss-box">
            <div class="swiss-box-title">
              <span>Arquitectura Interactiva Validada (Archify Showcase)</span>
              <a href="/arquitectura.html" target="_blank" rel="noopener" class="btn btn-primary">Abrir Visor Archify ↗</a>
            </div>
            <p style="font-size:13px; color:var(--ink-secondary); margin-bottom:12px;">
              El repositorio incluye su mapa de arquitectura interactivo compilado y verificado con
              <strong>Archify</strong> en <code>docs/arquitectura.json</code> y <code>docs/arquitectura.html</code>.
            </p>
            <table class="table-clean">
              <thead>
                <tr>
                  <th>Recurso / Prompt MCP</th>
                  <th>URI / Identificador</th>
                  <th>Propósito</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Resource</strong></td>
                  <td><code>secop://taxonomy/catalog</code></td>
                  <td>Catálogo completo de los 6 dominios y 11 enlaces de SECOP II</td>
                </tr>
                <tr>
                  <td><strong>Resource</strong></td>
                  <td><code>secop://bridge/scrapping-status</code></td>
                  <td>Telemetría de vinculación con el proyecto SCRAPPING</td>
                </tr>
                <tr>
                  <td><strong>Resource</strong></td>
                  <td><code>secop://rag/default-feeds</code></td>
                  <td>Feeds dinámicos y código para LangChain / LlamaIndex</td>
                </tr>
                <tr>
                  <td><strong>Resource</strong></td>
                  <td><code>secop://schemas/soql-dictionary</code></td>
                  <td>Diccionario SoQL de <code>p6dx-8zbt</code> y <code>jbjy-vk9h</code></td>
                </tr>
                <tr>
                  <td><strong>Prompt</strong></td>
                  <td><code>auditoria_licitacion_secop2</code></td>
                  <td>Auditoría legal, presupuestal y técnica de licitaciones</td>
                </tr>
                <tr>
                  <td><strong>Prompt</strong></td>
                  <td><code>ingesta_rag_contratacion</code></td>
                  <td>Pipeline de ingesta vectorial hacia Qdrant / Chroma / pgvector</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer-bar">
    <span>MCP SECOP II COLOMBIA v1.0.0 · Estándar Jan Polanco · Archify · Vanguard Swiss Light UI</span>
    <span>Autor: <strong>Ing. Luis Benjumea Rivera</strong> · Repositorio: <code>LUISBENJUMEARIVERA/MCP-SECOP</code></span>
  </footer>

  <script>
    let TOOLS_CATALOG = [];
    let ACTIVE_TOOL = null;

    function formatCOP(val) {
      const num = Number(val || 0);
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        maximumFractionDigits: 0
      }).format(num);
    }

    function switchTab(tabId) {
      document.querySelectorAll('.panel').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => {
        el.classList.remove('active');
        el.setAttribute('aria-selected', 'false');
      });
      const panel = document.getElementById(tabId);
      const btn = document.getElementById('btn-' + tabId);
      if (panel) panel.classList.add('active');
      if (btn) {
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
      }
    }

    async function initDashboard() {
      const [toolsResp, bridgeResp, taxResp, feedsResp] = await Promise.all([
        fetch('/api/v1/mcp/tools').then(r => r.json()),
        fetch('/api/v1/bridge/status').then(r => r.json()),
        fetch('/api/v1/taxonomy').then(r => r.json()),
        fetch('/api/v1/feeds').then(r => r.json())
      ]);

      TOOLS_CATALOG = toolsResp.tools || [];
      renderToolsRail();
      if (TOOLS_CATALOG.length > 0) {
        selectTool(TOOLS_CATALOG[0].name);
        await runSelectedTool();
      }

      renderBridgeStatus(bridgeResp);
      renderTaxonomy(taxResp);
      renderFeeds(feedsResp);
    }

    function renderToolsRail() {
      const container = document.getElementById('tools-list-container');
      container.innerHTML = TOOLS_CATALOG.map(t => `
        <button type="button" class="tool-item" id="rail-${t.name}" onclick="selectTool('${t.name}')">
          <div class="tool-code">${t.code}</div>
          <div class="tool-name">${t.name}</div>
          <div class="tool-desc">${t.title}</div>
        </button>
      `).join('');
    }

    function selectTool(toolName) {
      const found = TOOLS_CATALOG.find(t => t.name === toolName);
      if (!found) return;
      ACTIVE_TOOL = found;

      document.querySelectorAll('.tool-item').forEach(el => el.classList.remove('active'));
      const activeBtn = document.getElementById('rail-' + toolName);
      if (activeBtn) activeBtn.classList.add('active');

      document.getElementById('active-tool-code').textContent = found.code;
      document.getElementById('active-tool-name').textContent = found.name;
      document.getElementById('active-tool-desc').textContent = found.description;

      renderToolFormFields(found.default_args || {});
    }

    function renderToolFormFields(argsObj) {
      const container = document.getElementById('dynamic-form-fields');
      const keys = Object.keys(argsObj);
      if (keys.length === 0) {
        container.innerHTML = `
          <div style="font-family:var(--font-mono); font-size:12px; color:var(--ink-secondary);">
            Esta herramienta MCP no requiere argumentos obligatorios. Haz clic en Invocar para ejecutarla.
          </div>
        `;
        return;
      }

      container.innerHTML = keys.map(k => {
        const val = argsObj[k] !== null && argsObj[k] !== undefined ? argsObj[k] : '';
        return `
          <div class="field-group">
            <label for="arg-${k}">${k}</label>
            <input id="arg-${k}" name="${k}" class="input-ctrl" type="text" value="${String(val).replace(/"/g, '&quot;')}" />
          </div>
        `;
      }).join('');
    }

    function resetToolDefaults() {
      if (!ACTIVE_TOOL) return;
      renderToolFormFields(ACTIVE_TOOL.default_args || {});
    }

    async function runSelectedTool() {
      if (!ACTIVE_TOOL) return;
      const btn = document.getElementById('btn-execute-tool');
      btn.textContent = 'EJECUTANDO EN SECOP II...';
      const args = {};
      const defaultArgs = ACTIVE_TOOL.default_args || {};
      for (const k of Object.keys(defaultArgs)) {
        const inputEl = document.getElementById('arg-' + k);
        if (inputEl) {
          const rawVal = inputEl.value.trim();
          if (rawVal !== '') {
            if (typeof defaultArgs[k] === 'number') {
              args[k] = Number(rawVal);
            } else {
              args[k] = rawVal;
            }
          }
        }
      }

      const t0 = performance.now();
      const resp = await fetch('/api/v1/mcp/call', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool_name: ACTIVE_TOOL.name, arguments: args })
      });
      const payload = await resp.json();
      const elapsed = (performance.now() - t0).toFixed(1);

      btn.textContent = 'Invocar Herramienta MCP Ahora';
      document.getElementById('active-tool-latency').textContent = `Completado en ${elapsed} ms`;
      document.getElementById('json-results-output').textContent = JSON.stringify(payload, null, 2);

      renderVisualResult(ACTIVE_TOOL.name, payload.result || payload);
    }

    function renderVisualResult(toolName, data) {
      const container = document.getElementById('visual-results-container');
      const badge = document.getElementById('visual-summary-badge');

      if (data.records && Array.isArray(data.records)) {
        badge.textContent = `${data.records.length} PROCESOS · ${data.data_source || 'SODA'}`;
        container.innerHTML = data.records.map(r => `
          <article class="record-card">
            <div class="record-header">
              <span class="record-id">${r.process_id} // ${r.reference}</span>
              <span class="record-price">${formatCOP(r.base_price_cop)}</span>
            </div>
            <div class="record-title">${r.title}</div>
            <p style="font-size:12.5px; color:var(--ink-secondary);">${r.description}</p>
            <div class="record-meta">
              <span><strong>ENTIDAD:</strong> ${r.entity_name} (NIT: ${r.entity_nit})</span>
              <span><strong>UBICACIÓN:</strong> ${r.department} - ${r.city}</span>
              <span><strong>MODALIDAD:</strong> ${r.modality}</span>
              <span><strong>ESTADO:</strong> ${r.status}</span>
              <span><strong>UNSPSC:</strong> ${r.unspsc_code}</span>
            </div>
          </article>
        `).join('');
        return;
      }

      if (data.chunks && Array.isArray(data.chunks)) {
        badge.textContent = `${data.total_chunks} CHUNKS RAG · ${data.total_estimated_tokens} TOKENS`;
        container.innerHTML = data.chunks.map(c => `
          <article class="record-card">
            <div class="record-header">
              <span class="record-id">${c.chunk_id}</span>
              <span class="badge badge-emerald">${c.token_estimate} TOKENS · HASH ${c.content_hash.slice(0, 8)}</span>
            </div>
            <pre class="code-block" style="margin-top:8px; font-size:11.5px;">${c.text}</pre>
          </article>
        `).join('');
        return;
      }

      if (data.discovered_links && Array.isArray(data.discovered_links)) {
        badge.textContent = `${data.total_links_discovered} ENLACES · HTTP ${data.http_status}`;
        container.innerHTML = `
          <div class="record-card">
            <div class="record-header">
              <span class="record-id">${data.page_title}</span>
              <span class="badge badge-vermilion">VIEWSTATE: ${data.aspnet_viewstate_detected ? 'DETECTADO' : 'NO'}</span>
            </div>
            <p style="font-size:12px; color:var(--ink-secondary);">${data.meta_description}</p>
          </div>
          ${data.discovered_links.slice(0, 15).map(l => `
            <div class="record-card" style="padding:10px 14px;">
              <div class="record-header">
                <span class="badge">${l.category}</span>
                <span class="badge badge-emerald">RAG: ${l.rag_relevance}</span>
              </div>
              <div style="font-size:13px; font-weight:600; margin-top:4px;">${l.anchor_text}</div>
              <div style="font-family:var(--font-mono); font-size:11px; color:var(--ink-muted); word-break:break-all;">${l.url}</div>
            </div>
          `).join('')}
        `;
        return;
      }

      if (data.top_5_highest_value_processes) {
        const fin = data.financial_summary_cop || {};
        badge.textContent = `TOTAL ANALIZADO: ${formatCOP(fin.total_budget_cop)}`;
        container.innerHTML = `
          <div class="record-card">
            <div class="record-title">Resumen Presupuestal Consolidado</div>
            <div class="record-meta">
              <span><strong>PRESUPUESTO TOTAL:</strong> ${formatCOP(fin.total_budget_cop)}</span>
              <span><strong>PROMEDIO:</strong> ${formatCOP(fin.average_budget_cop)}</span>
              <span><strong>ENTIDADES ÚNICAS:</strong> ${fin.unique_entities}</span>
            </div>
          </div>
          ${data.top_5_highest_value_processes.map(p => `
            <div class="record-card">
              <div class="record-header">
                <span class="record-id">${p.process_id}</span>
                <span class="record-price">${formatCOP(p.base_price_cop)}</span>
              </div>
              <div class="record-title">${p.title}</div>
              <div class="record-meta">
                <span>${p.entity_name}</span>
                <span>${p.modality}</span>
              </div>
            </div>
          `).join('')}
        `;
        return;
      }

      badge.textContent = 'EJECUCIÓN EXITOSA';
      container.innerHTML = `<pre class="code-block">${JSON.stringify(data, null, 2)}</pre>`;
    }

    function renderBridgeStatus(st) {
      const pill = document.getElementById('bridge-pill');
      const metricVal = document.getElementById('metric-bridge');
      const metricSub = document.getElementById('metric-bridge-sub');

      if (st.scrapping_http_reachable) {
        pill.className = 'badge badge-emerald';
        pill.innerHTML = `<span class="status-dot"></span> PUENTE SCRAPPING: ONLINE (${st.scrapping_http_latency_ms} ms)`;
        metricVal.textContent = 'ONLINE :8010';
      } else if (st.scrapping_workspace_detected) {
        pill.className = 'badge badge-emerald';
        pill.innerHTML = `<span class="status-dot"></span> WORKSPACE SCRAPPING VINCULADO`;
        metricVal.textContent = 'VINCULADO';
      }
      metricSub.textContent = `${st.detected_modules.length} módulos compartidos detectados`;

      const tbody = document.querySelector('#bridge-status-table tbody');
      tbody.innerHTML = `
        <tr><th>Modo de Operación</th><td><span class="badge badge-emerald">${st.bridge_mode}</span></td></tr>
        <tr><th>URL API SCRAPPING</th><td><code>${st.scrapping_api_url}</code> (${st.scrapping_http_reachable ? 'Activa en red' : 'Motor local embebido activo'})</td></tr>
        <tr><th>Ruta Workspace Hermano</th><td><code>${st.scrapping_workspace_path}</code></td></tr>
        <tr><th>Módulos Detectados</th><td><code>${st.detected_modules.join(', ')}</code></td></tr>
        <tr><th>Diagnóstico</th><td>${st.status_message}</td></tr>
      `;
    }

    async function refreshBridgeStatus() {
      const st = await fetch('/api/v1/bridge/status').then(r => r.json());
      renderBridgeStatus(st);
    }

    function renderTaxonomy(categories) {
      const container = document.getElementById('taxonomy-container');
      container.innerHTML = categories.map(cat => `
        <article class="swiss-box">
          <div class="swiss-box-title">
            <span><span class="badge badge-vermilion">${cat.code}</span> ${cat.name}</span>
          </div>
          <p style="font-size:12.5px; color:var(--ink-secondary); margin-bottom:10px;">${cat.description}</p>
          <div style="font-family:var(--font-mono); font-size:11px; color:var(--ink-muted); margin-bottom:12px;">
            <strong>VOLUMEN:</strong> ${cat.record_volume_estimate} · <strong>FORMATO:</strong> ${cat.primary_format}
          </div>
          ${cat.links.map(lnk => `
            <div class="record-card" style="margin-bottom:8px;">
              <div class="record-header">
                <span class="record-id">${lnk.id} · ${lnk.title}</span>
                <span class="badge badge-emerald">RAG SCORE: ${lnk.rag_utility_score}/100</span>
              </div>
              <p style="font-size:12px; color:var(--ink-secondary); margin-bottom:8px;">${lnk.description}</p>
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <code style="font-size:11px; color:var(--ink-muted);">${lnk.url}</code>
                <button type="button" class="btn" style="min-height:34px; padding:4px 10px; font-size:11px;" onclick="launchSpiderOnUrl('${lnk.url}')">
                  Rastrear con Spider MCP
                </button>
              </div>
            </div>
          `).join('')}
        </article>
      `).join('');
    }

    async function launchSpiderOnUrl(targetUrl) {
      switchTab('tab-tools');
      selectTool('secop_spider_crawl');
      const input = document.getElementById('arg-seed_url');
      if (input) input.value = targetUrl;
      await runSelectedTool();
    }

    function renderFeeds(feeds) {
      document.getElementById('metric-feeds').textContent = `${feeds.length} FEEDS`;
      document.getElementById('feeds-count-badge').textContent = `${feeds.length} ENDPOINTS ACTIVOS`;
      const container = document.getElementById('feeds-list-container');
      container.innerHTML = feeds.map(f => `
        <div class="record-card" style="margin-bottom:0;">
          <div class="record-header">
            <span class="record-id">${f.slug}</span>
            <span class="badge badge-emerald">${f.chunk_size_chars} CHARS</span>
          </div>
          <div class="record-title">${f.name}</div>
          <p style="font-size:12px; color:var(--ink-secondary); margin-bottom:10px;">${f.description}</p>
          <div style="font-family:var(--font-mono); font-size:11px; margin-bottom:10px;">
            <div><strong>MCP RAG JSON:</strong> <a href="/api/v1/feeds/${f.slug}/rag" target="_blank">/api/v1/feeds/${f.slug}/rag</a></div>
            <div><strong>STREAM JSONL:</strong> <a href="/api/v1/feeds/${f.slug}/jsonl" target="_blank">/api/v1/feeds/${f.slug}/jsonl</a></div>
          </div>
        </div>
      `).join('');
    }

    async function createNewFeedFromUI() {
      const name = document.getElementById('feed-name-input').value.trim();
      const keyword = document.getElementById('feed-kw-input').value.trim();
      const departamento = document.getElementById('feed-dep-input').value.trim() || null;
      const chunk_size_chars = Number(document.getElementById('feed-chunk-input').value || 1400);

      await fetch('/api/v1/mcp/call', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tool_name: 'secop_manage_rag_feeds',
          arguments: { action: 'create', name, keyword, departamento, chunk_size_chars }
        })
      });
      const feedsResp = await fetch('/api/v1/feeds').then(r => r.json());
      renderFeeds(feedsResp);
    }

    function copyJsonOutput() {
      const text = document.getElementById('json-results-output').textContent;
      navigator.clipboard.writeText(text);
    }

    window.addEventListener('DOMContentLoaded', initDashboard);
  </script>
</body>
</html>
"""
