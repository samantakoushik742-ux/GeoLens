from __future__ import annotations

from create_table import connect_mysql


# Safe, additive migration for installations that already have an `images` table.
COLUMN_DEFINITIONS = {
    "cloudinary_url": "TEXT NULL",
    "cloudinary_public_id": "VARCHAR(255) NULL",
    "drive_file_id": "VARCHAR(255) NULL",
    "drive_url": "TEXT NULL",
    "image_path": "TEXT NULL",
    "source_path": "TEXT NULL",
    "hazard_type": "VARCHAR(50) NULL",
    "acquisition_date": "DATE NULL",
    "band_name": "VARCHAR(30) NULL",
    "file_hash": "CHAR(64) NULL",
    "file_size": "BIGINT NULL",
    "uploaded_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
}


def main():
    conn = connect_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'images'")
        if cursor.fetchone() is None:
            print("Images table does not exist. Creating it...")
            cursor.execute("""
                CREATE TABLE images (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    filename VARCHAR(255) NOT NULL,
                    cloudinary_url TEXT NULL,
                    cloudinary_public_id VARCHAR(255) NULL,
                    drive_file_id VARCHAR(255) NULL,
                    drive_url TEXT NULL,
                    image_path TEXT NULL,
                    source_path TEXT NULL,
                    hazard_type VARCHAR(50) NULL,
                    acquisition_date DATE NULL,
                    band_name VARCHAR(30) NULL,
                    file_hash CHAR(64) NULL UNIQUE,
                    file_size BIGINT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
        else:
            cursor.execute("SHOW COLUMNS FROM images")
            existing = {row[0] for row in cursor.fetchall()}
            for column, definition in COLUMN_DEFINITIONS.items():
                if column not in existing:
                    cursor.execute(f"ALTER TABLE images ADD COLUMN `{column}` {definition}")
                    print(f"Added column: {column}")

            # Existing Cloudinary columns may be NOT NULL. New Drive-only records
            # must be allowed to leave them empty.
            cursor.execute("SHOW COLUMNS FROM images")
            refreshed = {row[0]: row for row in cursor.fetchall()}
            for column, definition in (
                ("cloudinary_url", "TEXT NULL"),
                ("cloudinary_public_id", "VARCHAR(255) NULL"),
            ):
                if column in refreshed:
                    cursor.execute(f"ALTER TABLE images MODIFY COLUMN `{column}` {definition}")

            # Add a unique index only if one is not already present.
            cursor.execute("SHOW INDEX FROM images")
            indexes = cursor.fetchall()
            has_hash_unique = any(row[2] == 1 and row[4] == "file_hash" for row in indexes)
            if "file_hash" in refreshed and not has_hash_unique:
                cursor.execute(
                    "ALTER TABLE images ADD UNIQUE INDEX uq_images_file_hash (file_hash)"
                )

        conn.commit()
        cursor.close()
        print("Images table migration completed.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
