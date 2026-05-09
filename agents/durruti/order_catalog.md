# Catálogo de órdenes operativas

Lista viva de las órdenes que Durruti sabe procesar. Cada una tiene
input esperado, pasos, agentes implicados, criterios de éxito y
requisitos de aprobación.

> Cuando el humano dé una orden que no encaje con ninguna de éstas, Durruti
> primero intenta mapearla a la más cercana. Si no encaja, pide aclaración
> y propone añadir una nueva entrada al catálogo.

---

## FASE 1 (las que Durruti debe dominar)

### 1. `investigar_nicho`
- **Input:** nicho (texto), profundidad opcional (`baja`/`media`/`alta`).
- **Pasos:**
  1. Crear/recuperar proyecto en memoria.
  2. Delegar en Researcher con el brief.
  3. Recibir informe.
  4. Reportar al humano + dejar el `.md` en `outputs/research/`.
- **Output:** informe en Markdown con tamaño de mercado, competencia,
  palabras clave, ángulos diferenciadores, monetización viable.
- **Aprobación:** no requiere.
- **Coste estimado (real):** ~0.15 €.

### 2. `crear_landing`
- **Input:** objetivo, estilo, info del producto.
- **Pasos:**
  1. Si no hay research previo, sugerir hacerlo primero.
  2. Delegar en Builder.
  3. Recibir borrador (HTML + copy).
  4. Reportar al humano.
- **Output:** carpeta en `outputs/landings/[nombre]/` con `index.html`,
  `style.css`, `README.md`.
- **Aprobación:** crear local NO requiere; **publicar SÍ requiere OK**.
- **Coste estimado (real):** ~0.18 €.

### 3. `generar_contenido`
- **Input:** tema, formato (post / hilo / email / script), cantidad.
- **Pasos:**
  1. Delegar en Builder.
  2. Recibir borradores.
  3. Reportar al humano.
- **Output:** `.md` en `outputs/content/`.
- **Aprobación:** generar NO requiere; **publicar/enviar SÍ requiere OK**.
- **Coste estimado (real):** ~0.05–0.10 € por pieza.

### 4. `auditar_competencia`
- **Input:** competidor (URL, nombre).
- **Pasos:**
  1. Delegar en Researcher.
  2. Recibir informe.
  3. Reportar al humano.
- **Output:** informe en `outputs/research/competencia/`.
- **Aprobación:** no requiere.

### 5. `crear_proyecto`
- **Input:** nombre, descripción, objetivo.
- **Pasos:**
  1. `memory.crear_proyecto(...)`.
  2. Anotar en bitácora.
  3. Reportar.
- **Output:** archivo en `memory/projects/[slug].md` + fila en SQLite.
- **Aprobación:** no requiere.

### 6. `status`
- **Input:** ninguno (o `--proyecto [slug]` para detalle).
- **Pasos:**
  1. Listar proyectos activos.
  2. Listar tareas pendientes.
  3. Calcular costes (día/semana/mes).
  4. Reportar.
- **Output:** texto formateado al humano.
- **Aprobación:** no requiere.

---

## FASE 2 (con Operator, no antes)

### 7. `responder_whatsapp`
- Pendiente de definir cuando llegue Operator.

### 8. `publicar_red`
- Pendiente.

### 9. `enviar_email`
- Pendiente.

### 10. `automatizar_proceso`
- Pendiente.

---

## Cómo se añade una nueva orden

1. Durruti propone la entrada (no la añade directamente).
2. Humano aprueba.
3. Se actualiza este archivo + el playbook si toca.
4. Anotación en `CHANGELOG.md`.
