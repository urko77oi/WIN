# scoring.md — Agente Scout

> Sistema de scoring triple obligatorio. Cada oportunidad seria se evalúa en 3 perfiles de riesgo, no en uno solo.

---

## 🎯 Filosofía del scoring

El founder pidió **lectura dual/triple**: misma oportunidad evaluada bajo distintos apetitos de riesgo. Esto evita:

- Falsos negativos (descartar oportunidad agresiva por filtro conservador).
- Falsos positivos (lanzarse a oportunidad agresiva creyendo que es segura).
- Decisiones binarias mal calibradas.

**El Scout NUNCA entrega un único score.** Siempre los 3.

---

## 📐 Los 3 perfiles

| Perfil | Símbolo | Apetito de riesgo | Horizonte | Inversión típica | Tasa de éxito esperada |
|---|---|---|---|---|---|
| **Conservador** | 🛡️ | Bajo | 6-18 meses | < 1.000€ inicial | 30-50% (más seguro) |
| **Equilibrado** | ⚖️ | Medio | 3-12 meses | 500-5.000€ | 15-30% |
| **Agresivo** | 🔥 | Alto | 1-6 meses | 1.000-20.000€ | 5-15% (alto upside) |

---

## 🧮 Dimensiones evaluadas

Cada perfil pondera de forma distinta las **8 dimensiones** que el Scout puntúa de 0 a 10.

### D1 — Tamaño de mercado (TAM)
*¿Cuánto hay sobre la mesa?*
- 0 = nicho marginal sin escala.
- 5 = mercado mediano local/nicho global.
- 10 = mercado masivo, multi-millón potenciales.

### D2 — Crecimiento del mercado
*¿Va para arriba o para abajo?*
- 0 = en clara contracción.
- 5 = estable.
- 10 = crecimiento explosivo verificable (Trends, datos, demografía).

### D3 — Saturación competitiva
*¿Qué tan lleno está?* (puntuación inversa: más saturado = menos puntos).
- 0 = monopolizado por gigantes.
- 5 = competencia razonable, hay hueco.
- 10 = casi vacío, demanda visible sin oferta seria.

### D4 — Barrera de entrada
*¿Qué difícil es montarlo?* (puntuación inversa: más barrera = menos puntos para conservador, más para agresivo).
- 0 = barrera enorme (regulación, capital, expertise).
- 5 = barrera moderada.
- 10 = arrancar en una semana es viable.

### D5 — Monetización clara
*¿Cómo se hace dinero y es evidente?*
- 0 = no se ve cómo monetizar.
- 5 = monetización plausible pero no probada en el nicho.
- 10 = competidores facturando ya, modelo evidente.

### D6 — Ratio CAC/LTV preliminar
*¿Es económicamente viable?*
- 0 = CAC > LTV (suicida).
- 5 = ratio 1:1 a 1:2 (límite).
- 10 = ratio 1:3 o mejor proyectado.

### D7 — Ajuste con capacidades del founder
*¿El founder + sus agentes pueden ejecutar esto?*
- 0 = requiere expertise/red que no tienen.
- 5 = ejecutable con esfuerzo significativo.
- 10 = encaja perfectamente con stack actual.

### D8 — Riesgos legales/regulatorios/éticos
*¿Hay minas?* (puntuación inversa: más riesgo = menos puntos).
- 0 = riesgo grave (regulación dura, problemas éticos).
- 5 = riesgo moderado manejable.
- 10 = sin riesgos identificados.

---

## ⚖️ Pesos por perfil

Cada perfil pondera distinto las 8 dimensiones. Los pesos suman 100% en cada perfil.

### 🛡️ Perfil Conservador

| Dimensión | Peso |
|---|---|
| D1 Tamaño mercado | 10% |
| D2 Crecimiento | 10% |
| D3 Saturación (menos = mejor) | 15% |
| D4 Barrera entrada (baja = mejor) | 15% |
| D5 Monetización clara | 20% |
| D6 CAC/LTV | 15% |
| D7 Ajuste founder | 10% |
| D8 Riesgo legal | 5% |
| **Total** | **100%** |

**Filosofía:** prioriza **monetización probada**, **bajo CAC** y **baja barrera**. Acepta menos upside a cambio de más certeza.

---

### ⚖️ Perfil Equilibrado

| Dimensión | Peso |
|---|---|
| D1 Tamaño mercado | 15% |
| D2 Crecimiento | 15% |
| D3 Saturación | 15% |
| D4 Barrera entrada | 10% |
| D5 Monetización clara | 15% |
| D6 CAC/LTV | 10% |
| D7 Ajuste founder | 10% |
| D8 Riesgo legal | 10% |
| **Total** | **100%** |

**Filosofía:** mezcla balanceada. Es el escenario "base" que más se parece a una decisión racional estándar.

---

### 🔥 Perfil Agresivo

| Dimensión | Peso |
|---|---|
| D1 Tamaño mercado | 20% |
| D2 Crecimiento | 25% |
| D3 Saturación | 15% |
| D4 Barrera entrada | 5% |
| D5 Monetización clara | 5% |
| D6 CAC/LTV | 5% |
| D7 Ajuste founder | 10% |
| D8 Riesgo legal | 15% |
| **Total** | **100%** |

**Filosofía:** prioriza **upside** y **timing**. Asume que se puede aprender a monetizar, que CAC bajará, que se contratará expertise. **Pero** mantiene riesgo legal alto porque un nicho ilegal no se arregla con dinero.

---

## 🧮 Cálculo del score

Para cada perfil:

```
Score = Σ (puntuación_dimensión × peso_perfil)
```

Ejemplo concreto:

```
Oportunidad: "Cursos de cocina vegana B2C mercado hispano"

Puntuaciones (0-10):
D1 Tamaño = 7
D2 Crecimiento = 8
D3 Saturación = 6 (algunos players pero no domina)
D4 Barrera = 8 (montar curso y vender online es asequible)
D5 Monetización = 9 (modelo probado en otros nichos)
D6 CAC/LTV = 6 (estimado pero no validado)
D7 Ajuste founder = 7
D8 Riesgo legal = 10

Score Conservador  = 7×0.10 + 8×0.10 + 6×0.15 + 8×0.15 + 9×0.20 + 6×0.15 + 7×0.10 + 10×0.05 = 7.40
Score Equilibrado = 7×0.15 + 8×0.15 + 6×0.15 + 8×0.10 + 9×0.15 + 6×0.10 + 7×0.10 + 10×0.10 = 7.40
Score Agresivo    = 7×0.20 + 8×0.25 + 6×0.15 + 8×0.05 + 9×0.05 + 6×0.05 + 7×0.10 + 10×0.15 = 7.55
```

---

## 🚦 Umbrales de decisión

Por perfil, traducir el score a recomendación:

### 🛡️ Conservador
- **≥ 8.0** → Go inmediato.
- **6.5-7.9** → Validar con landing test.
- **5.0-6.4** → Investigar más antes de decidir.
- **< 5.0** → Descartar para este perfil.

### ⚖️ Equilibrado
- **≥ 7.5** → Go inmediato.
- **6.0-7.4** → Validar con landing test.
- **4.5-5.9** → Investigar más.
- **< 4.5** → Descartar para este perfil.

### 🔥 Agresivo
- **≥ 7.0** → Go con plan claro de cap de pérdida.
- **5.5-6.9** → Sprint de validación corto (≤14 días).
- **4.0-5.4** → Mantener en watchlist, no actuar.
- **< 4.0** → Descartar.

**Push alert se dispara automáticamente con cualquier score ≥ 8.5 en cualquier perfil.**

---

## 🟢🟡🔴 Banderas de confianza obligatorias

Cada score lleva una bandera de confianza separada:

- 🟢 **Confianza alta** — 5+ fuentes sólidas, datos cuantitativos verificables, mercado conocido.
- 🟡 **Confianza media** — 3-4 fuentes, mezcla cuanti/cuali, mercado parcialmente conocido.
- 🔴 **Confianza baja** — < 3 fuentes, predominantemente cualitativo, o mercado opaco.

**Un score 9 con confianza 🔴 NO es lo mismo que un score 7 con confianza 🟢.** Se reportan ambos datos. La bandera roja exige investigación adicional antes de cualquier "go".

---

## 🎯 Reporte canónico de scoring

Cada memo incluye este bloque obligatorio:

```
╔════════════════════════════════════════════════╗
║  TRIPLE SCORING                                ║
╠════════════════════════════════════════════════╣
║  🛡️ Conservador:  7.4/10  | Validar  | 🟢      ║
║  ⚖️ Equilibrado:  7.4/10  | Validar  | 🟢      ║
║  🔥 Agresivo:     7.5/10  | Validar  | 🟢      ║
╠════════════════════════════════════════════════╣
║  Recomendación primaria: ⚖️ Equilibrado       ║
║  Acción sugerida: landing test 14 días, 80€   ║
╚════════════════════════════════════════════════╝
```

Y abajo, **tabla de dimensiones** con las 8 puntuaciones y justificación breve por cada una.

---

## 🚫 Reglas duras de scoring

1. **Nunca scorear sin las 8 dimensiones.** Si falta data en alguna, declarar y no estimar.
2. **Confianza baja en 3+ dimensiones → bandera 🔴 automática del conjunto.**
3. **Riesgo legal D8 ≤ 3 → descarte automático en perfiles Conservador y Equilibrado** (en Agresivo se reporta pero con avisos rojos).
4. **Saturación D3 = 0 → descarte automático en Conservador.**
5. **CAC/LTV D6 ≤ 2 → descarte en los 3 perfiles** (un negocio que pierde dinero por cliente no es un negocio).

---

## 🔁 Calibración del modelo

Este scoring es **versión 1.0**. Cada postmortem mensual (ver `playbook.md` WF-5) puede proponer ajustes:

- Re-balancear pesos si datos históricos lo justifican.
- Añadir/quitar dimensiones si una no aporta señal.
- Ajustar umbrales si los hit rates están descalibrados.

**Cualquier cambio requiere aprobación del founder y se versiona** (ej: `scoring.md` v1.1 con changelog al final).

---

## 📝 Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | inicial | Versión base con 3 perfiles, 8 dimensiones |
