import unittest
from unittest.mock import patch

from database_ingestion import history_store


class FakeCursor:
    def __init__(self):
        self.statements = []

    def execute(self, query, values=None):
        self.statements.append((query, values))

    def fetchall(self):
        return []

    def close(self):
        pass


class FakeConnection:
    def __init__(self):
        self.fake_cursor = FakeCursor()
        self.committed = False

    def cursor(self, dictionary=False):
        return self.fake_cursor

    def commit(self):
        self.committed = True

    def close(self):
        pass


class AnalysisHistoryStoreTests(unittest.TestCase):
    def test_saves_analysis_as_an_additive_insert(self):
        connection = FakeConnection()
        record = {
            "id": "abc123",
            "timestamp": "2026-11-15T10:00:00+00:00",
            "hazard": "flood",
            "location": "Kolkata",
            "prediction": "flood",
            "confidence": 0.9,
            "selected_hazard_probability": 0.8,
            "change_index": 0.2,
            "historical_image": "old.png",
            "recent_image": "new.png",
            "message": "Test analysis",
        }

        with patch.object(
            history_store,
            "connect_mysql",
            return_value=connection,
        ):
            history_store.save_record(record)

        statements = connection.fake_cursor.statements
        self.assertIn("CREATE TABLE IF NOT EXISTS", statements[0][0])
        self.assertIn("INSERT INTO geolens_analysis_history", statements[1][0])
        self.assertNotIn("ON DUPLICATE KEY UPDATE", statements[1][0])
        self.assertEqual(statements[1][1][1], record["timestamp"])
        self.assertTrue(connection.committed)


if __name__ == "__main__":
    unittest.main()
