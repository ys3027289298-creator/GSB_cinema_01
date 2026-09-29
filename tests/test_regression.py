import unittest

import core


class TestRegression(unittest.TestCase):
    def test_invalid_session_id_rejected(self):
        state = core.new_game()
        self.assertFalse(core.schedule(state, ""))
        self.assertFalse(core.schedule(state, "   "))
        self.assertFalse(core.schedule(state, None))
        self.assertFalse(core.sell_ticket(state, ""))
        self.assertFalse(core.cancel_session(state, None))
        self.assertFalse(core.show(state, ""))
        self.assertFalse(core.refund(state, ""))
        self.assertEqual(state["sessions"], {})
        self.assertEqual(state["tickets"], {})

    def test_capacity_boundary(self):
        state = core.new_game()
        self.assertTrue(core.sell_ticket(state, "S1"))
        self.assertTrue(core.sell_ticket(state, "S1"))
        self.assertFalse(core.sell_ticket(state, "S1"))
        self.assertEqual(state["tickets"]["S1"], 2)
        self.assertTrue(core.sell_ticket(state, "S2"))

    def test_duplicate_input_idempotent(self):
        state = core.new_game()
        self.assertTrue(core.schedule(state, "S1"))
        self.assertFalse(core.schedule(state, "S1"))
        self.assertEqual(list(state["sessions"]), ["S1"])
        self.assertTrue(core.extra_show(state))
        self.assertFalse(core.extra_show(state))
        self.assertEqual(state["bonus"], 1)

    def test_cancel_idempotent(self):
        state = core.new_game()
        core.schedule(state, "S1")
        core.sell_ticket(state, "S1")
        self.assertTrue(core.cancel_session(state, "S1"))
        self.assertFalse(core.cancel_session(state, "S1"))
        self.assertEqual(state["tickets"].get("S1", 0), 0)

    def test_refund_requires_scheduled_session(self):
        state = core.new_game()
        core.schedule(state, "S1")
        core.sell_ticket(state, "S1")
        self.assertTrue(core.refund(state, "S1"))
        self.assertFalse(core.refund(state, "S1"))
        self.assertEqual(state["tickets"].get("S1", 0), 0)

    def test_empty_and_invalid_save_data(self):
        loaded = core.load_state("{}")
        self.assertEqual(loaded["ticket_id"], 0)
        self.assertEqual(loaded["seats"], 2)
        with self.assertRaises(ValueError):
            core.load_state("")
        with self.assertRaises(ValueError):
            core.load_state("[1, 2]")

    def test_save_load_round_trip_stable(self):
        state = core.new_game()
        core.schedule(state, "S1")
        core.sell_ticket(state, "S1")
        once = core.load_state(core.save_state(state))
        twice = core.load_state(core.save_state(once))
        self.assertEqual(once, twice)
        self.assertEqual(once["ticket_id"], state["ticket_id"])

    def test_price_boundaries(self):
        state = core.new_game()
        self.assertEqual(core.price(state, 1), 0)
        self.assertEqual(core.price(state, 0), 0)
        self.assertEqual(core.price(state, 5), 4)
        self.assertEqual(core.price(state, "x"), 0)

    def test_show_counts_only_when_projector_ok(self):
        state = core.new_game()
        self.assertTrue(core.show(state, "S1"))
        self.assertEqual(state["shows"], 1)
        state["projector_fault"] = True
        self.assertFalse(core.show(state, "S1"))
        self.assertEqual(state["shows"], 1)


if __name__ == "__main__":
    unittest.main()
