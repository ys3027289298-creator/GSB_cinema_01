"""电影院核心逻辑：排片、座位、票务和放映。"""

import json

COMMANDS = ("schedule", "sell", "price", "cancel", "show", "refund", "extra", "quit")


def new_game():
    return {
        "sessions": {},
        "seats": 2,
        "tickets": {},
        "day": 1,
        "ticket_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    if not isinstance(state, dict):
        raise ValueError("存档必须是 JSON 对象")
    for key, value in new_game().items():
        state.setdefault(key, value)
    if not isinstance(state["sessions"], dict) or not isinstance(state["tickets"], dict):
        raise ValueError("存档字段类型非法")
    return state


def _valid_session_id(session_id):
    return isinstance(session_id, str) and bool(session_id.strip())


def schedule(self, session_id):
    if not _valid_session_id(session_id):
        return False
    if session_id in self["sessions"]:
        return False
    self["sessions"][session_id] = True
    return True


def sell_ticket(self, session_id):
    if not _valid_session_id(session_id):
        return False
    sold = self["tickets"].get(session_id, 0)
    if sold >= self["seats"]:
        return False
    self["tickets"][session_id] = sold + 1
    self["ticket_id"] += 1
    return True


def price(self, end_day):
    if not isinstance(end_day, int) or isinstance(end_day, bool):
        return 0
    return max(end_day - self["day"], 0)


def cancel_session(self, session_id):
    if not _valid_session_id(session_id):
        return False
    had_session = self["sessions"].pop(session_id, None) is not None
    had_tickets = self["tickets"].pop(session_id, None) is not None
    return had_session or had_tickets


def show(self, session_id):
    if not _valid_session_id(session_id):
        return False
    if self.get("projector_fault"):
        return False
    self["shows"] = self.get("shows", 0) + 1
    return True


def refund(self, session_id):
    if not _valid_session_id(session_id):
        return False
    if session_id not in self["sessions"]:
        return False
    sold = self["tickets"].get(session_id, 0)
    if sold <= 0:
        return False
    if sold == 1:
        del self["tickets"][session_id]
    else:
        self["tickets"][session_id] = sold - 1
    return True


def extra_show(self):
    if self.get("extra_used"):
        return False
    self["extra_used"] = True
    self["bonus"] = self.get("bonus", 0) + 1
    return True


def _report(ok):
    print("ok" if ok else "fail")


def main():
    state = new_game()
    print("电影院 - 命令: schedule/sell/price/cancel/show/refund/extra/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            continue
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "quit":
            break
        if cmd not in COMMANDS:
            print("error: 未知命令")
            continue
        try:
            if cmd == "schedule" and len(args) == 1:
                _report(schedule(state, args[0]))
            elif cmd == "sell" and len(args) == 1:
                _report(sell_ticket(state, args[0]))
            elif cmd == "price" and len(args) == 1:
                print(price(state, int(args[0])))
            elif cmd == "cancel" and len(args) == 1:
                _report(cancel_session(state, args[0]))
            elif cmd == "show" and len(args) == 1:
                _report(show(state, args[0]))
            elif cmd == "refund" and len(args) == 1:
                _report(refund(state, args[0]))
            elif cmd == "extra" and not args:
                _report(extra_show(state))
            else:
                print("error: 命令格式错误")
        except ValueError:
            print("error: 参数无效")


if __name__ == "__main__":
    main()
