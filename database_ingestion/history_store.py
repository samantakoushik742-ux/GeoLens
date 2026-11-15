import logging
import os

import mysql.connector

from database_ingestion.create_table import connect_mysql


logger = logging.getLogger("geolens.database")

HISTORY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS geolens_analysis_history (
    id VARCHAR(32) PRIMARY KEY,
    created_at VARCHAR(40) NOT NULL,
    hazard VARCHAR(32) NOT NULL,
    location VARCHAR(255) NULL,
    prediction VARCHAR(32) NOT NULL,
    confidence DOUBLE NOT NULL,
    selected_hazard_probability DOUBLE NULL,
    change_index DOUBLE NOT NULL,
    historical_image VARCHAR(255) NOT NULL,
    recent_image VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    INDEX idx_geolens_history_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

HISTORY_FIELDS = (
    "id",
    "created_at",
    "hazard",
    "location",
    "prediction",
    "confidence",
    "selected_hazard_probability",
    "change_index",
    "historical_image",
    "recent_image",
    "message",
)


def is_database_configured():
    return any(
        os.getenv(name)
        for name in ("MYSQL_HOST", "MYSQL_USER", "MYSQL_DATABASE")
    )


def database_status():
    if not is_database_configured():
        return {"configured": False, "available": False}

    connection = None
    try:
        connection = _connect()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        return {"configured": True, "available": True}
    except (mysql.connector.Error, RuntimeError) as error:
        logger.warning("Aiven database health check failed: %s", error)
        return {"configured": True, "available": False}
    finally:
        if connection is not None:
            connection.close()


def load_records():
    connection = _connect()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(HISTORY_TABLE_SQL)
        cursor.execute(
            "SELECT id, created_at AS timestamp, hazard, location, prediction, confidence, "
            "selected_hazard_probability, change_index, historical_image, "
            "recent_image, message FROM geolens_analysis_history "
            "ORDER BY created_at DESC LIMIT 50"
        )
        return cursor.fetchall()
    except mysql.connector.Error as error:
        raise RuntimeError(f"Could not load analysis history from Aiven: {error}") from error
    finally:
        connection.close()


def save_record(record):
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(HISTORY_TABLE_SQL)
        columns = ", ".join(HISTORY_FIELDS)
        placeholders = ", ".join(["%s"] * len(HISTORY_FIELDS))
        values = tuple(
            record["timestamp"] if field == "created_at" else record[field]
            for field in HISTORY_FIELDS
        )
        cursor.execute(
            f"INSERT INTO geolens_analysis_history ({columns}) "
            f"VALUES ({placeholders})",
            values
        )
        connection.commit()
        cursor.close()
    except mysql.connector.Error as error:
        raise RuntimeError(f"Could not save analysis history to Aiven: {error}") from error
    finally:
        connection.close()


def _connect():
    try:
        return connect_mysql()
    except (mysql.connector.Error, RuntimeError, ValueError, OSError) as error:
        raise RuntimeError("Could not connect to the configured Aiven database.") from error
