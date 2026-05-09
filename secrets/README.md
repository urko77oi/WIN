# Secretos

Esta carpeta es **privada**. `.gitignore` bloquea su contenido excepto este
README y el inventario `secrets.md`.

## Reglas

1. **Ningún secreto va en un commit.** Si lo dudas, no commitees.
2. Los valores reales de las claves van en `.env` (raíz del proyecto) o en
   `secrets/.env`. Los nombres de las variables están en `.env.example`.
3. **Inventario vivo en `secrets.md`**: qué claves necesitamos, para qué,
   cómo conseguirlas, cuándo rotarlas. Lo mantiene Durruti y se revisa
   periódicamente.
4. **Cuando una clave se necesita, Durruti te la pide** (Telegram en Fase 1+,
   CLI en Fase 0) con instrucciones exactas: dónde obtenerla y cómo pegarla.
5. **Backup cifrado** (Fase 1+): `scripts/backup.py` generará una copia
   cifrada de esta carpeta con contraseña que solo tú conoces.

## Si una clave se filtra por error

1. Rotar la clave en el panel del proveedor inmediatamente.
2. Actualizar el valor en `.env` local.
3. Anotar la rotación en `secrets.md`.
4. Si subió a un commit público: el repo cambia de privado a comprometido,
   hay que purgar la historia (avisa a Claude Code, te guío).
