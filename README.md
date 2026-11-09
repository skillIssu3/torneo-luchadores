# Torneo de luchadores · 0xDecode

Aquí se juntan los luchadores de **todos los equipos** y combaten en una web, por rondas y por turnos.
La web se publica sola en GitHub Pages: `https://skillissu3.github.io/torneo-luchadores/`

## Para participar (Ronda 3)

No necesitas permisos en la organización: trabajas desde **tu propia copia (fork)** y propones el cambio con un **Pull Request**. Un organizador lo revisa y lo acepta.

1. En esta página pulsa **Fork** (arriba a la derecha) para crear tu copia en tu cuenta.
2. Clónala con SSH (cambia `TU_USUARIO`):
   ```
   git clone git@github.com:TU_USUARIO/torneo-luchadores.git
   cd torneo-luchadores
   ```
3. Crea una rama:
   ```
   git checkout -b mi-luchador
   ```
4. Copia tu luchador de `ejercicios-equipo/miembros/` a `luchadores/`, **con tu usuario de GitHub en minúsculas** como nombre de archivo (por ejemplo `luchadores/beltza07.py`). Opcionalmente añade una línea `EMOJI = "🐉"` para elegir tu figura (mira `luchadores/_plantilla.py`).
5. Sube tu rama a tu fork y abre el Pull Request:
   ```
   git add luchadores/tuusuario.py
   git commit -m "Añado a tuusuario al torneo"
   git push -u origin mi-luchador
   ```
   En GitHub pulsa **Compare & pull request**. Debe aparecer una ✅ verde (la validación automática). Si sale una ❌, entra en *Details* y lee qué falla.

Reglas: solo se admite **un archivo** `luchadores/tuusuario.py`, con valores directos (sin código). VIDA máx. 30, ATAQUE máx. 8.

## Para organizar

- **Ajustes únicos** del repo: *Settings > Pages > Source: GitHub Actions*, y proteger `main` (*Settings > Branches*: exigir Pull Request y que pase la comprobación **validar**).
- Cada PR con ✅: **Merge pull request**. Al hacer merge, la web se regenera sola en 1-2 minutos.
- En directo: abre la web, **Espacio** o clic avanza el texto, **A** activa el modo automático, **F** pantalla completa.
- Si algo va mal, en local: `python3 tools/build.py && python3 -m http.server -d docs` y abre `http://localhost:8000`.
- Con menos de 2 luchadores válidos, la web muestra luchadores de ejemplo (modo demo).

## Cómo funciona

- `tools/build.py` lee `luchadores/*.py` **sin ejecutarlos** (solo valores literales) y genera `docs/luchadores.json`.
- `.github/workflows/validar.yml` comprueba cada PR: que solo toque `luchadores/` y que el luchador sea válido. No usa secretos.
- `.github/workflows/pages.yml` regenera el JSON y publica `docs/` en cada cambio de `main`.
- `docs/index.html` es toda la web (HTML + JS, sin dependencias). Los nombres y gritos se muestran como texto, nunca como HTML.
