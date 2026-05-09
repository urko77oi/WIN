# SETUP — Cómo arrancar este proyecto tras clonar

Este repo (FORRARSE / Durruti) **no incluye archivos sensibles ni el entorno
virtual**. Tras clonar tienes que crear unas cuantas cosas a mano. Esta es la
lista completa.

> Si algo no encaja con lo que ves al clonar, **pregunta antes de improvisar**.

---

## 1. Lo que NO está en el repo (y por qué)

| Ruta | Qué es | Por qué no está |
|---|---|---|
| `.env` | Variables de entorno reales (API keys, tokens) | Contiene secretos. Se crea desde `.env.example` |
| `.venv/` | Entorno virtual de Python | Se regenera con `uv sync` |
| `secrets/.env` | Secretos adicionales si aplica | Igual que `.env` |
| `secrets/*.key`, `*.pem`, `backup_*.enc` | Claves y backups cifrados | Nunca van a git |
| `memory/db.sqlite` | Base de datos local de Durruti | Se crea sola al arrancar |
| `memory/research_cache/` | Cache de investigaciones | Se regenera |
| `logs/*.log`, `logs/doctor-*.md` | Logs operativos | Se generan al usar el sistema |
| `outputs/` | Salidas generadas por los agentes | Se crean al ejecutar |
| `__pycache__/`, `.pytest_cache/`, etc. | Caches de Python | Se regeneran |

Lo que SÍ está: todo el código, los `.md` de diseño de los 3 agentes, los
scripts, configs (`config/*.yaml`), y la plantilla `.env.example`.

---

## 2. Requisitos previos

- **Python 3.11 o superior**
- **`uv`** — gestor de dependencias. Instalación en Windows (PowerShell):
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  (En Linux/macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Git** (ya lo tienes si has clonado esto)
- **Una API key de Anthropic** *solo si* quieres ejecutar en modo `real`. Para
  empezar no hace falta — el modo `mock` funciona sin coste y sin internet.

---

## 3. Pasos tras clonar

```powershell
# 1. Entrar al proyecto
cd WIN   # o como hayas nombrado la carpeta tras 'git clone'

# 2. Crear el entorno virtual e instalar dependencias
uv sync

# 3. Copiar la plantilla de entorno
copy .env.example .env

# 4. (Opcional) Editar .env si vas a usar modo real:
#    - LLM_MODE=real
#    - ANTHROPIC_API_KEY=tu_clave_aqui
#    Para arrancar de cero, déjalo en LLM_MODE=mock

# 5. Arrancar Durruti
uv run python scripts/start.py
```

Si todo va bien, te aparece el prompt CLI de Durruti en español. Pruébalo
con algo como:

```
> investiga el nicho cursos yoga online
> status
```

---

## 4. Inventario de claves (cuando las necesites)

`secrets/secrets.md` lleva la tabla viva de qué claves usa el proyecto, para
qué, dónde conseguirlas y cuándo rotarlas. Estado actual:

- `ANTHROPIC_API_KEY` — necesaria solo si `LLM_MODE=real`. Se obtiene en
  https://console.anthropic.com → API Keys.
- `TELEGRAM_BOT_TOKEN` — Fase 1, todavía no se usa. Se crea con `@BotFather`.
- `TELEGRAM_CHAT_ID` — Fase 1, se descubre con `scripts/setup_telegram.py`.

**Reglas de oro con los secretos** (también en `secrets/README.md`):

1. Ningún secreto va a un commit. Si dudas, no commitees.
2. Los valores reales viven en `.env` (raíz) o `secrets/.env`. Los nombres
   de variables están en `.env.example`.
3. Si una clave se filtra: rótala inmediatamente en el panel del proveedor,
   actualiza tu `.env` local, y anótalo en `secrets/secrets.md`.

---

## 5. Si algo falla al arrancar

1. `uv run python scripts/doctor.py` — autodiagnóstico.
2. Mira el log más reciente en `logs/`.
3. Lee `DOCTOR.md` para el protocolo.
4. Si nada de lo anterior aclara: pregunta.

---

## 6. Cosas que pueden faltar y deberías preguntar antes de tocar

Estos archivos **deberían existir tras seguir los pasos de arriba**. Si no
existen o ves algo distinto, pregunta antes de crearlos manualmente:

- `.env` — lo creas tú copiando de `.env.example`. Si no aparece tras el
  paso 3, revisa que estás en la carpeta correcta.
- `.venv/` — la crea `uv sync`. Si falla, mira el error de uv: suele ser
  versión de Python o permisos.
- `memory/db.sqlite` — se crea al primer arranque. Si no se crea, pregunta
  (puede ser problema de permisos en la carpeta `memory/`).

Cualquier otro archivo extraño que veas y no esté listado aquí: **pregunta**.
No improvises sobre la estructura del proyecto.
