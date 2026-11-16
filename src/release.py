"""SNAP · paquete para subir al servidor. Uso: python3 src/release.py https://www.dominio.com
Genera la web con el dominio, comprueba que no queda ningún «TU-DOMINIO» ni nombre de partner y crea snap-web-<dominio>-<fecha>.zip
con el contenido de dist/public (sin config.php ni datos). Ese zip se descomprime tal cual en la carpeta www del hosting."""
import sys, subprocess, pathlib, zipfile, datetime, re
if len(sys.argv) < 2 or "TU-DOMINIO" in sys.argv[1]:
    sys.exit("Uso: python3 src/release.py https://www.dominio.com")
root = pathlib.Path(__file__).resolve().parent.parent
subprocess.run([sys.executable, "-I", str(root / "src/build.py"), sys.argv[1]], check=True)
pub = root / "dist/public"
bad = [str(f) for f in pub.rglob("*") if f.suffix in (".html", ".xml", ".txt", ".js") and re.search(r"TU-DOMINIO|partner|sun ?stay|partner|partner", f.read_text(errors="ignore"), re.I)]
if bad:
    sys.exit("Revisar antes de publicar: " + ", ".join(bad[:5]))
host = sys.argv[1].split("//")[-1].strip("/")
out = root / f"snap-web-{host}-{datetime.date.today()}.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in pub.rglob("*"):
        r = f.relative_to(pub)
        if f.is_file() and r.name != "config.php" and not str(r).startswith("api/data/") or str(r) == "api/data/.htaccess":
            z.write(f, r)
print("Listo:", out.name, "·", sum(1 for _ in zipfile.ZipFile(out).namelist()), "archivos")
