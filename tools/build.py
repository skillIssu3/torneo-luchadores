#!/usr/bin/env python3
"""Lee luchadores/*.py y genera docs/luchadores.json para la web.

IMPORTANTE: los archivos NO se ejecutan nunca. Se leen como texto y solo se
aceptan líneas del tipo  NOMBRE = "algo"  (valores literales). Así, aunque
alguien mande un archivo con código malicioso, aquí no hace nada.

Uso:
    python3 tools/build.py            # genera docs/luchadores.json (salta los rotos)
    python3 tools/build.py --check    # solo valida; sale con error si hay algún archivo mal
"""
import ast
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CARPETA = RAIZ / "luchadores"
SALIDA = RAIZ / "docs" / "luchadores.json"

MAX_VIDA = 30       # mismos límites que ejercicios-equipo/config.py
MAX_ATAQUE = 8
NOMBRE_ARCHIVO = re.compile(r"^[a-z0-9][a-z0-9-]{0,38}\.py$")
CAMPOS = {"NOMBRE", "VIDA", "ATAQUE", "GRITO", "EMOJI"}


def leer(ruta: Path) -> dict:
    """Devuelve el luchador de un archivo o lanza ValueError con un mensaje claro."""
    if not NOMBRE_ARCHIVO.match(ruta.name):
        raise ValueError("el nombre del archivo debe ir en minúsculas, sin espacios ni tildes "
                         "(por ejemplo beltza07.py)")
    try:
        arbol = ast.parse(ruta.read_text(encoding="utf-8"))
    except SyntaxError as e:
        raise ValueError(f"error de sintaxis en la línea {e.lineno}: ¿comillas sin cerrar?")
    except UnicodeDecodeError:
        raise ValueError("el archivo debe estar guardado en UTF-8")

    datos = {}
    for nodo in arbol.body:
        if isinstance(nodo, ast.Expr) and isinstance(nodo.value, ast.Constant):
            continue  # comentario de documentación entre comillas triples
        if not (isinstance(nodo, ast.Assign) and len(nodo.targets) == 1
                and isinstance(nodo.targets[0], ast.Name)):
            raise ValueError(f"línea {nodo.lineno}: solo se admiten líneas como NOMBRE = \"...\" (sin código)")
        clave = nodo.targets[0].id
        try:
            valor = ast.literal_eval(nodo.value)
        except (ValueError, SyntaxError):
            raise ValueError(f"línea {nodo.lineno}: {clave} debe ser un texto o un número, sin operaciones")
        if clave in CAMPOS:
            datos[clave] = valor

    for obligatorio in ("NOMBRE", "VIDA", "ATAQUE"):
        if obligatorio not in datos:
            raise ValueError(f"falta la línea {obligatorio} = ...")
    nombre = datos["NOMBRE"]
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("NOMBRE debe ser un texto entre comillas")
    for campo in ("VIDA", "ATAQUE"):
        if isinstance(datos[campo], bool) or not isinstance(datos[campo], int):
            raise ValueError(f"{campo} debe ser un número entero")
        if datos[campo] < 1:
            raise ValueError(f"{campo} debe ser al menos 1")
    grito = datos.get("GRITO")
    emoji = datos.get("EMOJI")
    if grito is not None and not isinstance(grito, str):
        raise ValueError("GRITO debe ser un texto entre comillas")
    if emoji is not None and not isinstance(emoji, str):
        raise ValueError("EMOJI debe ser un texto entre comillas")

    return {
        "autor": ruta.stem,
        "nombre": nombre.strip()[:24],
        "vida": min(datos["VIDA"], MAX_VIDA),
        "ataque": min(datos["ATAQUE"], MAX_ATAQUE),
        "grito": (grito or "").strip()[:80],
        "emoji": (emoji or "").strip()[:8],
    }


def main() -> int:
    solo_comprobar = "--check" in sys.argv
    luchadores, errores = [], 0
    for ruta in sorted(CARPETA.glob("*.py")):
        if ruta.name.startswith("_"):
            continue
        try:
            luchadores.append(leer(ruta))
        except ValueError as e:
            errores += 1
            print(f"ERROR luchadores/{ruta.name}: {e}", file=sys.stderr)
    print(f"{len(luchadores)} luchadores válidos, {errores} con errores.")
    if solo_comprobar:
        return 1 if errores else 0
    SALIDA.parent.mkdir(exist_ok=True)
    SALIDA.write_text(json.dumps(luchadores, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Escrito {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
