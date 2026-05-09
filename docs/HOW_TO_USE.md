# Cómo usar Durruti

Guía operativa para el humano. Si solo vas a leer un documento, lee éste.

---

## Primer arranque

Una vez por máquina:

```powershell
cd durruti
uv sync                # instala dependencias
copy .env.example .env # crea tu archivo de entorno (no se sube a git)
```

Edita `.env` si quieres cambiar algo. Por defecto:
- `LLM_MODE=mock` → respuestas simuladas, sin coste.
- `LOG_LEVEL=INFO` → trazas legibles.

---

## Día a día

### Hablar con Durruti
```powershell
uv run python scripts/start.py
```
Aparece un prompt `>`. Escribe tu orden en español. Ejemplos:

- `investiga el nicho cursos yoga online`
- `crea una landing para vender un curso de fotografía móvil`
- `genera 3 posts cortos sobre productividad en remoto`
- `crea proyecto: agencia de redes para fisioterapeutas`
- `status`

Para salir: `salir`, `exit`, o `Ctrl+C`.

### Ver el estado
```powershell
uv run python scripts/status.py
```
Muestra: modo LLM, proyectos activos, costes.

### Diagnosticar fallos
```powershell
uv run python scripts/doctor.py
```
Genera un reporte en `logs/doctor-AAAA-MM-DD.md`.
Si no entiendes el reporte, pásaselo a Claude Code y di:
*"Lee `DOCTOR.md` y este reporte. Diagnostica."*

### Aprobar / rechazar tareas pendientes (Fase 1+)
```powershell
uv run python scripts/approve.py
```
En Fase 0 normalmente no hay pendientes (Durruti pregunta en el momento).

---

## Cómo Durruti decide

1. Lees su orden → la clasifica → delega en el especialista adecuado
   (Scout o Builder).
2. El especialista hace su parte.
3. Durruti consolida y te lo cuenta.
4. Si hay que aprobar algo (publicar, gastar dinero), te lo pregunta antes.

Más detalle en [`HOW_TO_GIVE_ORDERS.md`](HOW_TO_GIVE_ORDERS.md).

---

## Memoria

Tres lugares:

| Carpeta | Qué hay | Quién escribe |
|---|---|---|
| `memory/projects/` | Un `.md` por proyecto activo | Durruti (al crear) y luego anota bitácora |
| `memory/learnings/` | Lecciones | Cualquier agente cuando aprenda algo no obvio |
| `memory/playbooks/` | Procesos repetibles | Durruti, cuando un proceso se ha repetido 2+ veces |

`memory/db.sqlite` guarda lo estructurado (proyectos, costes, decisiones).
**No la edites a mano** salvo emergencia.

---

## Cuando algo falle

1. Mira el banner que sale al ejecutar el script.
2. Mira el último log en `logs/`.
3. `uv run python scripts/doctor.py`.
4. Lee [`DOCTOR.md`](../DOCTOR.md).
5. Si nada de lo anterior aclara: copia logs y reporte a Claude Code.

---

## Cambiar a modo real (Fase 1+)

Cuando tengas créditos en `console.anthropic.com`:

1. Edita `.env`:
   ```
   LLM_MODE=real
   ANTHROPIC_API_KEY=sk-ant-...
   ```
2. `uv run python scripts/status.py` para confirmar el modo.
3. Sigue igual: las llamadas pasan a ser reales y se trackea coste real.
