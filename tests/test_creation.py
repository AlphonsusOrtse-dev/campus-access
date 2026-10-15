import unittest

import storage


class TestCreation(unittest.TestCase):
    def setUp(self):
        storage.reset_storage()

    def test_valid_creation(self):
        request = storage.create_request("F001", "visitor")
        self.assertEqual(
            request,
            {
                "id": "A001",
                "fellow_id": "F001",
                "card_type": "visitor",
                "status": "requested",
                "approved_by": None,
            },
        )

    def test_ids_increase(self):
        self.assertEqual(storage.create_request("F001", "visitor")["id"], "A001")
        self.assertEqual(storage.create_request("F002", "staff")["id"], "A002")

    def test_blank_fellow_id_rejected_and_nothing_created(self):
        for bad in ("", "   "):
            with self.assertRaises(ValueError):
                storage.create_request(bad, "visitor")
        self.assertEqual(storage.list_requests(), [])

    def test_invalid_card_type_rejected(self):
        with self.assertRaises(ValueError):
            storage.create_request("F001", "guest")
        self.assertEqual(storage.list_requests(), [])

    def test_wrong_input_type_rejected(self):
        with self.assertRaises(ValueError):
            storage.create_request(123, "visitor")
        with self.assertRaises(ValueError):
            storage.create_request("F001", None)

    def test_malformed_and_unknown_ids_rejected(self):
        storage.create_request("F001", "visitor")
        bad_ids = ["", "a001", "A1", "A00x", "A000", "B001", "A\u0660\u0660\u0661", 5, None]
        for bad in bad_ids:
            with self.assertRaises(ValueError):
                storage.get_request(bad)
        with self.assertRaises(ValueError):
            storage.get_request("A999")  # well-formed but unknown

    def test_get_request_returns_copy(self):
        storage.create_request("F001", "visitor")
        copy = storage.get_request("A001")
        copy["status"] = "returned"
        self.assertEqual(storage.get_request("A001")["status"], "requested")

    def test_update_without_approver_is_rejected_and_record_unchanged(self):
        storage.create_request("F001", "visitor")
        before = storage.get_request("A001")
        with self.assertRaises(ValueError):
            storage.update_request("A001", "approved", "   ")
        with self.assertRaises(ValueError):
            storage.update_request("A001", "issued", None)
        self.assertEqual(storage.get_request("A001"), before)

    def test_update_valid_change(self):
        storage.create_request("F001", "visitor")
        updated = storage.update_request("A001", "approved", "M01")
        self.assertEqual(updated["status"], "approved")
        self.assertEqual(storage.get_request("A001")["approved_by"], "M01")


if __name__ == "__main__":
    unittest.main()
