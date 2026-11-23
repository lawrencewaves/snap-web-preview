"""SNAP · paquete para subir al servidor. Uso: SNAP_CONTACT_EMAIL=correo python3 src/release.py https://www.dominio.com
Genera la web con el dominio, comprueba que no queda ningún «TU-DOMINIO» ni nombre de partner (lista en blocklist.txt, fuera del repo: un nombre por línea) y crea snap-web-<dominio>-<fecha>.zip
con el contenido de dist/public (sin config.php, datos ni .well-known, que en el servidor es de root). Ese zip se descomprime tal cual en la carpeta www del hosting."""
import sys, os, subprocess, pathlib, zipfile, datetime, re
if len(sys.argv) < 2 or "TU-DOMINIO" in sys.argv[1]:
    sys.exit("Uso: python3 src/release.py https://www.dominio.com")
if not os.environ.get("SNAP_CONTACT_EMAIL", "").strip():
    sys.exit("Falta SNAP_CONTACT_EMAIL (correo operativo confirmado por Robert): sin él la web no muestra correo y los textos legales usan un canal provisional")
root = pathlib.Path(__file__).resolve().parent.parent
subprocess.run([sys.executable, "-I", str(root / "src/build.py"), sys.argv[1]], check=True)
pub = root / "dist/public"
bl = root / "blocklist.txt"  # nombres de partners: fuera del repo público (R-006); sin él no se publica
if not bl.exists():
    sys.exit("Falta blocklist.txt junto a src/ (un nombre de partner por línea; no se sube al repo)")
names = [re.escape(n.strip()) for n in bl.read_text().splitlines() if n.strip()]
if not names:
    sys.exit("blocklist.txt está vacío")
pat = re.compile("|".join(names), re.I)
dom = re.compile("TU-DOMINIO")  # el config.sample.php lo lleva a propósito: se rellena en el servidor
bad = []
for f in pub.rglob("*"):
    if f.is_file() and f.suffix in (".html", ".xml", ".txt", ".js", ".php", ".htaccess", ".json"):
        txt = f.read_text(errors="ignore")
        if pat.search(txt) or (f.suffix != ".php" and dom.search(txt)):
            bad.append(str(f))
if bad:
    sys.exit("Revisar antes de publicar: " + ", ".join(bad[:5]))
host = sys.argv[1].split("//")[-1].strip("/")
out = root / f"snap-web-{host}-{datetime.date.today()}.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in pub.rglob("*"):
        r = f.relative_to(pub)
        if f.is_file() and r.name != "config.php" and not str(r).startswith(("api/data/", ".well-known/")) or str(r) == "api/data/.htaccess":
            z.write(f, r)
print("Listo:", out.name, "·", sum(1 for _ in zipfile.ZipFile(out).namelist()), "archivos")
