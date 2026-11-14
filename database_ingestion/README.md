# Satellite database ingestion

This package adds a MySQL + Google Drive ingestion workflow to the Satellite project.

## Place the folder

Copy `database_ingestion/` into the root of your existing `Satellite/` project.

Expected layout:

```text
Satellite/
├── database_ingestion/
│   ├── create_table.py
│   ├── update_table.py
│   ├── ingest.py
│   ├── requirements.txt
│   └── dataset.zip        # place your ZIP here
├── data/raw/
├── .env                   # project-root environment file
├── credentials.json       # Google OAuth desktop-app credentials
└── ...
```

## Install dependencies

Activate the same virtual environment used by the Satellite project, then run:

```bash
pip install -r database_ingestion/requirements.txt
```

## Configure credentials

1. Add the MySQL/Aiven values to the existing `Satellite/.env`.
2. Set `MYSQL_SSL_CA` to the CA certificate path supplied by Aiven.
3. Enable the Google Drive API in Google Cloud.
4. Create OAuth client credentials for a Desktop application and save the downloaded file as `Satellite/credentials.json`.
5. Do not upload `.env`, `credentials.json`, or `token.json` to public repositories.

## Run in this order

From the `Satellite/` project root:

```bash
python database_ingestion/create_table.py
python database_ingestion/update_table.py
python database_ingestion/ingest.py
```

`update_table.py` is an additive migration for an existing `images` table. Back up the database before running schema changes.

## What ingestion does

- Extracts `database_ingestion/dataset.zip` safely into `database_ingestion/extracted/`.
- Finds JPEG, PNG, WebP, BMP, GIF, TIFF and Sentinel-2 JP2 images.
- Computes SHA-256 hashes to avoid re-uploading duplicate image content.
- Copies images to `data/raw/imported/`, preserving the archive's internal folder structure.
- Uploads new images to Google Drive.
- Stores Drive IDs/URLs, local paths, file hashes, sizes and best-effort metadata in MySQL.
- Infers hazard labels only when `flood`, `vegetation` or `drought` appears in the path/name. It infers a date only when a YYYYMMDD or YYYY-MM-DD style date is present, and a band only when a recognizable Sentinel-2 band token such as B08 or B8A is present. Uncertain values remain NULL.

## Important model-integration note

The imported images are kept under `data/raw/imported/`. This is a safe staging area and does **not** automatically make them valid temporal training pairs. Your current training pipeline may require a specific folder layout and paired historical/recent images. Review and organize the imported data into the exact structure expected by `preprocess_dataset.py` before training.

The `image_path` stored in MySQL is a local machine path. It is useful on this machine, but another computer will have a different path. Use `drive_file_id`/`drive_url` for cloud references.

## Notes

- The ingestion script requires interactive Google OAuth on its first run; it creates `token.json` for later runs.
- Existing database rows are retained. The script uses `file_hash` as the deduplication key.
- Keep your database credentials and Google OAuth files private.
