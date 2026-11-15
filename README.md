# GeoLens - Satellite Multi-Hazard Monitoring

Local environmental monitoring interface connected to a temporal CNN that classifies a historical/recent satellite pair as **vegetation**, **drought**, or **flood**.

The website design is the existing GeoLens frontend. Flask serves that frontend and the analysis API from one address:

**http://127.0.0.1:5000**

## What is actually implemented

There is **one** model architecture: `TemporalDisasterCNN` in `models/disaster_cnn.py`.

It does **not** include three separately trained flood, vegetation, and drought networks. The same checkpoint outputs class probabilities for all three categories. Hazard buttons on the website select which monitoring context you are studying; they do not load a different model.

A trained checkpoint is expected at:

```text
models/best_multi_hazard_cnn.pth
```

If that file is missing, the backend still starts. Image analysis returns a clear error instead of a fabricated prediction.

The current checkpoint expects one input band. Use aligned, single-band GeoTIFF pairs; RGB PNG/JPEG uploads are accepted by the file picker but are incompatible with this checkpoint and return a channel-mismatch error. The model weights and preprocessing have not been changed.

## Windows setup

```bat
cd C:\Satellite
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

The server binds to `0.0.0.0` and uses `PORT` (default `5000`). Open the local interface at `http://127.0.0.1:5000`:

```powershell
$env:HOST = "0.0.0.0"
$env:PORT = "8000"
python app.py
```

## Run the application

1. Start the complete application (Flask serves both the website and API):

```powershell
python app.py
```

2. Open the printed local URL (for example, http://127.0.0.1:5000)
3. Go to **Image analysis**
4. Choose Flood, Drought, or Vegetation
5. Upload a previous satellite image and a current satellite image
6. Click **Analyse image pair**

If the configured port is already in use, the process exits with an error. It does not switch ports automatically.

## Deploying on Vercel and Render

The frontend is plain HTML/CSS/JavaScript. Configure Vercel with `frontend/` as the root directory, the **Other** framework preset, no build command, and `.` as the output directory. Set the Render service URL in `frontend/api-config.js` before deploying:

```javascript
window.GEOLENS_API = {
    BASE_URL: "https://YOUR-RENDER-SERVICE.onrender.com"
};
```

Static Vercel deployments do not expose environment variables to browser JavaScript automatically, so `VITE_API_BASE_URL` is not used by this project. The Render URL belongs in this runtime config file. Keep it HTTPS.

For Render, use the repository root as the service root directory and configure:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --workers 1 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT`
- Health check path: `/api/health`

Render supplies `PORT`. Set these service environment variables:

| Variable | Value |
| --- | --- |
| `HOST` | `0.0.0.0` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated production Vercel origin and any fixed local development origins |
| `CORS_ALLOWED_ORIGIN_REGEX` | Optional regex restricted to this project's Vercel preview URLs |
| `MYSQL_HOST` | Aiven service hostname |
| `MYSQL_PORT` | Aiven service port |
| `MYSQL_USER` | Aiven database user |
| `MYSQL_PASSWORD` | Aiven database password (secret) |
| `MYSQL_DATABASE` | Aiven database name |
| `MYSQL_SSL_CA` | Path to the Aiven CA certificate uploaded as a Render secret file |
| `GEOLENS_MODEL_PATH` | Optional deployed checkpoint path if it is not at `models/best_multi_hazard_cnn.pth` |

Set `CORS_ALLOWED_ORIGINS` to the exact Vercel production origin. If using preview deployments, set a project-scoped `CORS_ALLOWED_ORIGIN_REGEX`; do not use `*`. Add `/api/health` as Render's health check. Analysis history uses an additive `geolens_analysis_history` MySQL table when all required MySQL variables are set; with no database configuration, local development keeps using `data/analysis_history.json`. Existing local JSON history is not migrated or deleted automatically.

The checkpoint is gitignored and must be made available to the Render service separately (or committed through an approved large-file workflow). The health endpoint reports whether it is present; analysis returns `503` if it is missing. Do not deploy credentials in frontend files or commit `.env`.

## Training a model

Raw GeoTIFF pairs belong in:

```text
data/raw/<vegetation|drought|flood>/historical/
data/raw/<vegetation|drought|flood>/recent/
```

Matching filenames are paired automatically.

```bat
python preprocessing/preprocess_dataset.py
python train.py
```

The trainer writes `models/best_multi_hazard_cnn.pth`. After that file exists, reload the website and run analysis again.

## API

The frontend reads the backend base URL from `frontend/api-config.js`:

```javascript
window.GEOLENS_API = { BASE_URL: "" }
```

An empty base URL makes requests relative to the page for same-origin local development. The frontend calls `/api/health`, `/api/history`, and submits multipart image pairs to `/api/analyze`.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Backend, model, and optional database status |
| GET | `/api/capabilities` | Supported hazards and upload rules |
| POST | `/api/analyze` | Multipart `historical`, `recent`, `hazard` |
| GET | `/api/history` | Recent analyses from Aiven or local JSON storage |

Successful analysis responses include the predicted class, softmax confidence, class probabilities, and a temporal change index. Confidence is **not** disaster probability.

## Project layout

```text
app.py                         Flask server
config.py                      Host, port, upload limits
database_ingestion/history_store.py  Aiven-backed analysis history
predict.py                     Preprocess + inference
train.py                       CNN training
models/disaster_cnn.py         Temporal CNN
preprocessing/                 GeoTIFF preprocessing
utils/dataset.py               Training dataset
frontend/                      Existing GeoLens UI
```
