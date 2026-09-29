import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_schedule(self):
        state = core.new_game()
        self.assertTrue(core.schedule(state, "S1"))
        self.assertFalse(core.schedule(state, "S1"))

    def test_02_no_sell_when_full(self):
        state = core.new_game()
        core.sell_ticket(state, "S1")
        core.sell_ticket(state, "S1")
        result = core.sell_ticket(state, "S1")
        self.assertFalse(result)

    def test_03_price_exact(self):
        state = core.new_game()
        self.assertEqual(core.price(state, 4), 3)

    def test_04_cancel_session_refunds(self):
        state = core.new_game()
        core.sell_ticket(state, "S1")
        core.cancel_session(state, "S1")
        self.assertEqual(state["tickets"].get("S1", 0), 0)

    def test_05_no_show_on_fault(self):
        state = core.new_game()
        state["projector_fault"] = True
        result = core.show(state, "S1")
        self.assertFalse(result)

    def test_06_refund_failure_keeps_order(self):
        state = core.new_game()
        state["tickets"] = {"S1": 1}
        result = core.refund(state, "S1")
        self.assertFalse(result)
        self.assertEqual(state["tickets"]["S1"], 1)

    def test_07_extra_show_once(self):
        state = core.new_game()
        state["bonus"] = 0
        core.extra_show(state)
        self.assertEqual(state["bonus"], 1)

    def test_08_load_preserves_ticket(self):
        state = core.new_game()
        state["ticket_id"] = 4
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["ticket_id"], 4)


if __name__ == "__main__":
    unittest.main()
