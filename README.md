# Route Analysis Toolkit

Python + Leaflet Web GIS toolkit for analyzing oversized transport corridors.

**Workflow:** upload a real route (My Maps **KMZ**/KML · GeoJSON · GPX) → snap obstacles to **chainage (km)** → apply vehicle templates → export PDF / CSV / GeoJSON / project JSON.

Includes a built-in sample: **Montpellier → Lyon** (KMZ).

**Live demo:** https://route-analysis-toolkit.vercel.app

> Not for certified operational transport planning.

![Toolkit hero](images/hero-placeholder.svg)

## Features

- **Upload route** — GeoJSON, KML, **KMZ**, GPX
- **Km snap / chainage** — obstacles snap onto the corridor (`km 42.30`)
- **Rich obstacles** — severity, bypass flag, note, optional photo
- **Vehicle templates** — extra-long · wide & heavy · very heavy · custom
- **Distance profile** — markers every ~50 km in map + PDF
- **Checklist report** — conflicts in km order + field checklist
- **Save / load project** — download JSON · autosave in browser · server copy (local runs only)
- **Sample corridor** — Montpellier → Lyon KMZ with example obstacles

## Technologies

| Layer | Stack |
|-------|--------|
| Backend | Python, FastAPI, Shapely, NumPy, ReportLab |
| Frontend | Leaflet, vanilla JS |
| Sample | `backend/data/sample_montpellier_lyon.kmz` |

## Quick start

```bash
git clone https://github.com/GeoByteBrew/Route_Analysis_Toolkit.git
cd Route_Analysis_Toolkit

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Try it

1. App loads **Montpellier → Lyon** sample KMZ with example obstacles
2. Or upload your own **KMZ / KML / GeoJSON / GPX**
3. Click **Click map to place obstacle**, set type/value, click the route
4. Adjust vehicle limits → **Run Analysis**
5. Download **GeoJSON / CSV / PDF** (generated on demand, nothing stored on the server)

## Example API

### Sample route

```bash
curl -s http://127.0.0.1:8000/api/sample/route | python3 -m json.tool
```

### Upload a KMZ

```bash
curl -s -X POST http://127.0.0.1:8000/api/upload/route \
  -F "file=@backend/data/sample_montpellier_lyon.kmz" | python3 -m json.tool
```

### Analyze route + obstacles

```bash
curl -s -X POST http://127.0.0.1:8000/api/analyze \
  -H 'Content-Type: application/json' \
  -d @- <<'EOF' | python3 -m json.tool
{
  "route": {
    "type": "Feature",
    "properties": {"name": "demo"},
    "geometry": {
      "type": "LineString",
      "coordinates": [[3.87613,43.61087],[4.80729,44.54327],[4.8355,45.76412]]
    }
  },
  "obstacles": [
    {"name": "Low bridge", "type": "low_bridge", "value": 3.7, "lon": 4.62745, "lat": 43.95685}
  ],
  "vehicle": {
    "length_m": 45, "width_m": 4.5, "height_m": 4.2,
    "weight_t": 80, "max_slope_pct": 8
  }
}
EOF
```

### Key endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/meta` | App metadata |
| `GET` | `/api/sample/route` | Montpellier → Lyon sample + obstacles |
| `POST` | `/api/upload/route` | Parse GeoJSON / KML / KMZ / GPX |
| `POST` | `/api/analyze` | Route + obstacles analysis |
| `POST` | `/api/export/{pdf\|csv\|geojson}` | Build a report from an `/api/analyze` result |

### Export a report

```bash
curl -s -X POST http://127.0.0.1:8000/api/analyze -H 'Content-Type: application/json' \
  -d '{"route": {...}, "obstacles": [...]}' > result.json
curl -s -X POST http://127.0.0.1:8000/api/export/pdf -H 'Content-Type: application/json' \
  -d @result.json -o report.pdf
```

## Deploy (Vercel)

The app is stateless, so it runs as a single Vercel Function:

1. Import the repo in Vercel — preset **FastAPI**, root `./`, no environment variables needed
2. `pyproject.toml` points Vercel at the app (`[tool.vercel] entrypoint = "backend.app:app"`)
3. Static files in `frontend/` are served from the CDN

On Vercel, server-side project copies are disabled (read-only filesystem); saving a project downloads the JSON and autosaves in the browser instead. Request bodies are limited to ~4.5 MB, so keep obstacle photos small.

## How analysis works

```mermaid
flowchart LR
  A[Upload KMZ / KML / GeoJSON / GPX] --> B[Show corridor on Leaflet]
  B --> C[User places obstacles]
  C --> D[Vehicle limits]
  D --> E[Compare values vs constraints]
  E --> F[Feasibility + PDF / CSV / GeoJSON]
```

| Obstacle type | Conflict when |
|---------------|---------------|
| Low bridge | clearance &lt; vehicle height |
| Narrow road | width &lt; vehicle width |
| Weight limit | limit &lt; vehicle weight |
| Steep slope | slope &gt; vehicle max slope |
| Note | always caution if on corridor |

## Project layout

```
Route_Analysis_Toolkit/
├── backend/
│   ├── app.py
│   ├── data/
│   │   ├── sample_montpellier_lyon.kmz
│   │   └── sample_obstacles.json
│   └── services/
│       ├── parse_route.py
│       ├── custom_analyze.py
│       ├── vehicle.py
│       └── report.py
├── frontend/
├── scripts/run.sh
├── pyproject.toml
└── outputs/
```

## License

MIT — see [LICENSE](LICENSE).
