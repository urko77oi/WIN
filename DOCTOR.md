# DOCTOR — Protocolo de diagnóstico

Cuando algo no funciona y no sabes por qué, sigue este orden.
Este documento está pensado para que **Claude Code lo lea junto contigo**
y diagnostique en español llano.

---

## 1. Ejecuta el autodiagnóstico

```powershell
uv run python scripts/doctor.py
```

Genera un reporte en `logs/doctor-AAAA-MM-DD.md` con:
- ¿Está bien instalado el entorno?
- ¿`.env` presente y con las claves esperadas?
- ¿Memoria accesible?
- ¿Última actividad? ¿Tareas colgadas?
- ¿Espacio en disco / red?
- (Si `LLM_MODE=real`) ¿API Anthropic responde?

---

## 2. Mira los logs recientes

```powershell
# Última hora de actividad
type logs\$(Get-Date -Format 'yyyy-MM-dd').log
```

Busca líneas con `ERROR` o `WARNING`. Cópialas a Claude Code si no las entiendes.

---

## 3. Síntomas comunes y soluciones rápidas

| Síntoma | Causa probable | Acción |
|---|---|---|
| `ModuleNotFoundError` al arrancar | Entorno no sincronizado | `uv sync` |
| "No se encuentra .env" | Falta el archivo | `copy .env.example .env` |
| "ANTHROPIC_API_KEY no definida" en `LLM_MODE=real` | Falta la key | Mete la key en `.env` o cambia a `LLM_MODE=mock` |
| Durruti devuelve siempre lo mismo | Estás en `LLM_MODE=mock` | Es lo esperado en Fase 0 |
| `database is locked` | Procesos paralelos sobre SQLite | Cierra el otro proceso o reinicia |
| Tareas colgadas en `tasks/pending/` | Algo crasheó a medias | Mueve manualmente a `tasks/completed/` o re-arranca |
| El sistema no responde y no hay logs | Proceso no arrancó | `uv run python scripts/start.py` y observa stdout |

---

## 4. Modo pánico: parar todo

Si Durruti se está comportando raro y quieres frenarlo:

- En el terminal donde corre: `Ctrl+C`.
- Si dejó tareas a medias: revísalas en `tasks/in_progress/` y muévelas
  manualmente a `tasks/pending/` cuando quieras reanudar.
- Para reanudar: `uv run python scripts/start.py`.

---

## 5. Si nada funciona

1. Copia el contenido de `logs/doctor-*.md` más reciente.
2. Copia el último log de `logs/AAAA-MM-DD.log`.
3. Pégaselos a Claude Code con el mensaje:
   *"Lee `DOCTOR.md` y estos logs. Diagnostícame qué pasa y proponme
   pasos concretos."*

Claude Code tiene contexto del sistema y puede leer todo el repo.
