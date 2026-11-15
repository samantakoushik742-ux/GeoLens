import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import app as backend


class BackendApiTests(unittest.TestCase):
    def setUp(self):
        self.client = backend.app.test_client()

    def test_health_check_reports_service_and_model(self):
        with (
            patch.object(backend, "model_status", return_value={"available": True}),
            patch.object(
                backend,
                "database_status",
                return_value={"configured": False, "available": False},
            ),
        ):
            response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["service"], "GeoLens Backend")
        self.assertEqual(payload["status"], "ok")
        self.assertTrue(payload["model"]["available"])

    def test_cors_preflight_allows_local_frontend(self):
        response = self.client.options(
            "/api/analyze",
            headers={
                "Origin": "http://localhost:5500",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Access-Control-Allow-Origin"],
            "http://localhost:5500",
        )
        self.assertIn("POST", response.headers["Access-Control-Allow-Methods"])
        self.assertIn(
            "content-type",
            response.headers["Access-Control-Allow-Headers"].lower(),
        )

    def test_cors_rejects_unconfigured_origin(self):
        response = self.client.options(
            "/api/analyze",
            headers={
                "Origin": "https://unconfigured.example",
                "Access-Control-Request-Method": "POST",
            },
        )

        self.assertNotIn("Access-Control-Allow-Origin", response.headers)

    def test_capabilities_matches_upload_contract(self):
        response = self.client.get("/api/capabilities")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["uploads"]["historical_field"], "historical")
        self.assertEqual(payload["uploads"]["recent_field"], "recent")
        self.assertEqual(payload["uploads"]["hazard_field"], "hazard")
        self.assertIn(".tif", payload["uploads"]["extensions"])

    def test_history_returns_saved_records_in_local_development(self):
        expected = [{"id": "test-record", "prediction": "flood"}]
        with tempfile.TemporaryDirectory() as temporary_directory:
            history_file = Path(temporary_directory) / "history.json"
            history_file.write_text(json.dumps(expected), encoding="utf-8")
            with (
                patch.object(backend, "is_database_configured", return_value=False),
                patch.object(backend, "HISTORY_FILE", history_file),
            ):
                response = self.client.get("/api/history")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["records"], expected)

    def test_analyze_accepts_multipart_image_pair_and_preserves_response(self):
        def image_file(name):
            output = io.BytesIO()
            Image.new("RGB", (8, 8), color="green").save(output, format="PNG")
            output.seek(0)
            return (output, name)

        result = {
            "predicted_class": "flood",
            "confidence": 0.9,
            "class_probabilities": {
                "flood": 0.9,
                "drought": 0.05,
                "vegetation": 0.05,
            },
            "change_index": 0.2,
            "interpretation": "Test result",
            "input_channels": 3,
            "image_size": 256,
            "class_names": ["vegetation", "drought", "flood"],
        }

        with tempfile.TemporaryDirectory() as upload_dir:
            with (
                patch.object(backend, "UPLOAD_DIR", Path(upload_dir)),
                patch.object(
                    backend,
                    "model_status",
                    return_value={"available": True},
                ),
                patch.object(backend, "run_pair_inference", return_value=result),
                patch.object(backend, "save_history_record"),
                patch.object(backend, "encode_preview", return_value=None),
            ):
                response = self.client.post(
                    "/api/analyze",
                    data={
                        "historical": image_file("old.png"),
                        "recent": image_file("new.png"),
                        "hazard": "flood",
                    },
                    content_type="multipart/form-data",
                )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["success"])
        self.assertEqual(payload["prediction"], "flood")
        self.assertEqual(payload["class_probabilities"]["flood"], 0.9)

    def test_analyze_returns_service_unavailable_when_model_is_missing(self):
        def image_file(name):
            output = io.BytesIO()
            Image.new("RGB", (8, 8), color="green").save(output, format="PNG")
            output.seek(0)
            return (output, name)

        with tempfile.TemporaryDirectory() as upload_dir:
            with (
                patch.object(backend, "UPLOAD_DIR", Path(upload_dir)),
                patch.object(
                    backend,
                    "model_status",
                    return_value={"available": False},
                ),
            ):
                response = self.client.post(
                    "/api/analyze",
                    data={
                        "historical": image_file("old.png"),
                        "recent": image_file("new.png"),
                        "hazard": "flood",
                    },
                    content_type="multipart/form-data",
                )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json()["error"], "Trained model not found")
        self.assertNotIn(str(backend.DEFAULT_MODEL), response.get_json()["message"])


if __name__ == "__main__":
    unittest.main()
