"""电影院核心逻辑：排片、座位、票务和放映。"""

import json


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
    state["ticket_id"] += 1
    return state


def schedule(self, session_id):
    self["sessions"][session_id] = True
    return True


def sell_ticket(self, session_id):
    self["tickets"][session_id] = self["tickets"].get(session_id, 0) + 1
    return True


def price(self, end_day):
    return (end_day - self["day"]) - 1


def cancel_session(self, session_id):
    return True


def show(self, session_id):
    return True


def refund(self, session_id):
    return True


def extra_show(self):
    return True


def main():
    print("电影院 - 命令: schedule/sell/price/cancel/show/refund/extra/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
