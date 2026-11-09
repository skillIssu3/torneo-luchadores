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
4. Trae lo último de `ejercicios-equipo`, para que tu luchador lleve su grito de guerra (el de la Ronda 2):
   ```
   git -C ../ejercicios-equipo checkout main
   git -C ../ejercicios-equipo fetch
   git -C ../ejercicios-equipo merge origin/main
   ```
   Estos comandos actúan sobre `ejercicios-equipo` sin que salgas de esta carpeta, así que tu rama `mi-luchador` no cambia.
   Los dos repos tienen que estar uno al lado del otro, por ejemplo en `~/git`. Si te sale `cannot change to '../ejercicios-equipo'`, esa carpeta no está ahí: no sigas hasta encontrarla.
5. Copia tu luchador de `ejercicios-equipo/miembros/` a esta carpeta, **con tu usuario de GitHub en minúsculas** como nombre de archivo. Por ejemplo, si tu archivo era `ana.py` y tu usuario es `beltza07`:
   ```
   cp ../ejercicios-equipo/miembros/ana.py luchadores/beltza07.py
   ```
   Opcionalmente, añade al final una línea `EMOJI = "🐉"` para elegir tu figura (mira `luchadores/_plantilla.py`).
6. Sube tu rama a tu fork y abre el Pull Request. Antes, comprueba que estás en tu rama: `git branch --show-current` debe decir `mi-luchador`.
   ```
   git add luchadores/tuusuario.py
   git commit -m "Añado a tuusuario al torneo"
   git push -u origin mi-luchador
   ```
   En GitHub pulsa **Compare & pull request**. La validación automática pone una ✅ verde (a veces tarda hasta que un organizador la aprueba). Si sale una ❌, entra en *Details* y lee qué falla.

   Si no te sale el botón, abre esta dirección (cambia `TU_USUARIO` por tu usuario de GitHub):
   ```
   https://github.com/skillIssu3/torneo-luchadores/compare/main...TU_USUARIO:torneo-luchadores:mi-luchador?expand=1
   ```
   Si pone «There isn't anything to compare», tu commit no está en la rama `mi-luchador`: pide ayuda a un organizador. No uses el enlace que imprime `git push`, porque apunta a tu propio fork.

Reglas: el PR solo puede cambiar **un archivo**, `luchadores/tuusuario.py` (tu usuario de GitHub en minúsculas), con valores directos (sin código). VIDA máx. 30, ATAQUE máx. 8. La validación rechaza otro nombre de archivo o tocar el luchador de otra persona.

## Para organizar

- **Ajuste recomendado (una vez):** *Settings > Actions > General > Fork pull request workflows from outside collaborators* > «Require approval for first-time contributors who are new to GitHub». Las cuentas nuevas necesitarán que pulséis **Approve and run workflows** en su PR. Es normal.
- Activar Pages una vez: *Settings > Pages > Source: GitHub Actions*.
- Haced merge solo de los PR con ✅ (*Merge pull request*). Al hacer merge, la web se regenera sola en 1-2 minutos.
- En directo: abre la web, **Espacio** o clic avanza el texto, **A** activa el modo automático, **F** pantalla completa.
- Si algo va mal, en local: `python3 tools/build.py && python3 -m http.server -d docs` y abre `http://localhost:8000`.
- Con menos de 2 luchadores válidos, la web muestra luchadores de ejemplo (modo demo).

## Cómo funciona

- `tools/build.py` lee `luchadores/*.py` **sin ejecutarlos** (solo valores literales) y genera `docs/luchadores.json`.
- `.github/workflows/validar.yml` comprueba cada PR: que cambie un único archivo, `luchadores/<usuario del autor>.py` (añadirlo o editar el propio, nunca borrar ni tocar el de otra persona), y que el luchador sea válido. No usa secretos.
- `.github/workflows/pages.yml` regenera el JSON y publica `docs/` en cada cambio de `main`.
- `docs/index.html` es toda la web (HTML + JS, sin dependencias). Los nombres y gritos se muestran como texto, nunca como HTML.
