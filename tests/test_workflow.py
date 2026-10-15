import unittest
import storage
import workflow


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        storage.reset_storage()

    def test_b1_illegal_shortcut_requested_to_issued(self):
        req = storage.create_request("F001", "visitor")
        with self.assertRaises(ValueError):
            workflow.issue_card(req["id"])
        # Verify status remains requested
        self.assertEqual(storage.get_request(req["id"])["status"], "requested")

    def test_b2_reject_blank_approver(self):
        req = storage.create_request("F002", "student")
        with self.assertRaises(ValueError):
            workflow.approve_request(req["id"], "   ")
        self.assertEqual(storage.get_request(req["id"])["status"], "requested")

    def test_b3_full_workflow_success(self):
        req = storage.create_request("F003", "staff")
        workflow.approve_request(req["id"], "M01")
        self.assertEqual(storage.get_request(req["id"])["status"], "approved")
        
        workflow.issue_card(req["id"])
        self.assertEqual(storage.get_request(req["id"])["status"], "issued")
        
        workflow.return_card(req["id"])
        self.assertEqual(storage.get_request(req["id"])["status"], "returned")

    def test_b4_double_return_rejection(self):
        req = storage.create_request("F004", "visitor")
        workflow.approve_request(req["id"], "M02")
        workflow.issue_card(req["id"])
        workflow.return_card(req["id"])
        
        with self.assertRaises(ValueError):
            workflow.return_card(req["id"])


if __name__ == "__main__":
    unittest.main()