import pandas as pd, re, html, zipfile, math
from pathlib import Path

# =========================
# CONFIG
# =========================
EXCEL = "Contrato Praia Georeferenciado2.xlsx"
OUT = Path("KMZ_LOCALIDADES")
OUT.mkdir(exist_ok=True)

# =========================
# FUNÇÕES
# =========================
def parse_coord(x):
    if pd.isna(x): return None
    s = str(x).replace("°","").replace(",",".")
    m = re.search(r"[-+]?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None

def morada_sem_numero(s):
    if pd.isna(s): return ""
    s = re.sub(r"\s+\d+.*$", "", str(s).strip())
    return s.strip(" ,;-")

def esc(s):
    return html.escape(str(s))

# =========================
# LER EXCEL
# =========================
df = pd.read_excel(EXCEL)
df["lat"] = df["latitude"].apply(parse_coord)
df["lon"] = df["longitude"].apply(parse_coord)
df = df.dropna(subset=["lat","lon","LOCALIDADE","MORADA","CIL"])
df["MORADA_LIMPA"] = df["MORADA"].apply(morada_sem_numero)

# =========================
# GERAR KMZ POR LOCALIDADE
# =========================
for localidade, df_loc in df.groupby("LOCALIDADE"):

    print(f"Gerando {localidade}...")

    parts = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        "<kml xmlns='http://www.opengis.net/kml/2.2'>",
        "<Document>",
        f"<name>{esc(localidade)}</name>"
    ]

    for morada, g in df_loc.groupby("MORADA_LIMPA"):
        parts.append(f"<Folder><name>{esc(morada)}</name>")
        for _, r in g.iterrows():
            parts.append("<Placemark>")
            parts.append(f"<name>{esc(r['CIL'])}</name>")
            parts.append("<Point>")
            parts.append(f"<coordinates>{r['lon']},{r['lat']},0</coordinates>")
            parts.append("</Point>")
            parts.append("</Placemark>")
        parts.append("</Folder>")

    parts.append("</Document></kml>")
    kml = "\n".join(parts)

    kmz_path = OUT / f"{localidade}.kmz"
    with zipfile.ZipFile(kmz_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("doc.kml", kml)

print("✔ KMZs criados com sucesso")