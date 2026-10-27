# AGENTS.md — Contexto para Agentes de IA

> Lee primero [`CONSTITUTION.md`](./CONSTITUTION.md) para conocer el propósito, invariantes y decisiones del proyecto.

## 1. Resumen Operativo

- **Proyecto:** `MCP SECOP II Colombia` (`mcp-secop`)
- **Paquete Python:** `src/mcp_secop/`
- **Gestor de Entorno:** `uv` exclusivamente (prohibido `pip` y `requirements.txt`).
- **Puente con `SCRAPPING`:** `src/mcp_secop/scrapping_bridge.py` conecta por HTTP con `http://127.0.0.1:8010` y detecta el workspace hermano en `../SCRAPPING`.

## 2. Comandos Esenciales

```bash
uv sync                              # Sincronizar entorno
uv run mcp-secop --check-bridge      # Diagnosticar puente con SCRAPPING
uv run mcp-secop --web               # Levantar UI Suiza Clara en :8020
uv run mcp-secop --transport stdio   # Ejecutar servidor MCP por STDIO
uv run ruff check .                  # Linter
uv run ty check                      # Typecheck
uv run pytest -v                     # Pruebas (7/7)
```

## 3. Reglas de Mantenimiento

1. Actualiza `CONSTITUTION.md` en el mismo commit ante cualquier cambio arquitectónico.
2. Si modificas la topología de componentes, actualiza `docs/arquitectura.json` y regenera `docs/arquitectura.html` con `Archify`.
3. Mantén la estética de **Minimalismo Suizo Institucional de tonalidades claras** (`#F6F6F3`, `#FFFFFF`, `#0D0E11`, `#D9381E`) en `src/mcp_secop/ui_template.py`.
