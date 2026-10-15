import json
import os
import tempfile
import unittest
from unittest import mock

import storage


class TestPersistence(unittest.TestCase):
    def setUp(self):
        storage.reset_storage()
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = os.path.join(self.folder.name, "requests.json")

    def write_file(self, text):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(text)

    def good_record(self, request_id="A001"):
        return {"id": request_id, "fellow_id": "F001", "card_type": "visitor",
                "status": "requested", "approved_by": None}

    def test_new_id_after_reload_is_A002(self):
        storage.create_request("F001", "visitor")
        storage.save_requests(self.path)
        storage.reset_storage()  # simulates restarting the program
        self.assertEqual(storage.load_requests(self.path), 1)
        self.assertEqual(storage.create_request("F002", "student")["id"], "A002")

    def test_full_data_survives_reload(self):
        storage.create_request("F001", "visitor")
        storage.update_request("A001", "approved", "M01")
        storage.save_requests(self.path)
        storage.reset_storage()
        storage.load_requests(self.path)
        self.assertEqual(storage.get_request("A001")["approved_by"], "M01")
        self.assertEqual(storage.get_request("A001")["status"], "approved")

    def test_missing_file_loads_nothing(self):
        self.assertEqual(storage.load_requests(self.path), 0)
        self.assertEqual(storage.list_requests(), [])

    def test_bad_files_rejected_and_existing_data_kept(self):
        storage.create_request("F001", "visitor")  # valid data already in memory
        bad_files = {
            "corrupt json": "{not json",
            "empty file": "",
            "not a list": json.dumps({"id": "A001"}),
            "missing key": json.dumps([{"id": "A001", "fellow_id": "F001"}]),
            "duplicate ids": json.dumps([self.good_record(), self.good_record()]),
            "invalid status": json.dumps([dict(self.good_record(), status="lost")]),
            "invalid card type": json.dumps([dict(self.good_record(), card_type="vip")]),
            "issued without approver": json.dumps([dict(self.good_record(), status="issued")]),
            "unicode digits in id": json.dumps([self.good_record("A\u0660\u0660\u0661")]),
        }
        for name, text in bad_files.items():
            with self.subTest(problem=name):
                self.write_file(text)
                with self.assertRaises(ValueError):
                    storage.load_requests(self.path)
                self.assertEqual(len(storage.list_requests()), 1)
                self.assertEqual(storage.get_request("A001")["fellow_id"], "F001")

    def test_failed_save_does_not_damage_existing_file(self):
        storage.create_request("F001", "visitor")
        storage.save_requests(self.path)
        with open(self.path, encoding="utf-8") as file:
            original_text = file.read()

        storage.create_request("F002", "staff")
        with mock.patch("storage.json.dump", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                storage.save_requests(self.path)

        with open(self.path, encoding="utf-8") as file:
            self.assertEqual(file.read(), original_text)
        self.assertFalse(os.path.exists(self.path + ".tmp"))


if __name__ == "__main__":
    unittest.main()
