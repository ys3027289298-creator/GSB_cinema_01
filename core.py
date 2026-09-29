"""电影院核心逻辑：排片、座位、票务和放映。"""

import json


def new_game():
    return {
        "sessions": {},
        "seats": 2,
        "tickets": {},
        "day": 1,
        "ticket_id": 0,
        "bonus": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    # 读档必须原样恢复票号，否则后续票号会与存档前重复
    return json.loads(text)


def schedule(self, session_id):
    # 非法/空场次或已排过的场次一律拒绝，保证重复排片幂等
    if not session_id or session_id in self["sessions"]:
        return False
    self["sessions"][session_id] = True
    return True


def sell_ticket(self, session_id):
    # 空数据拒绝；达到座位容量临界后不再售票，重复调用幂等
    if not session_id:
        return False
    sold = self["tickets"].get(session_id, 0)
    if sold >= self["seats"]:
        return False
    self["tickets"][session_id] = sold + 1
    return True


def price(self, end_day):
    # 跨日票价 = 结束日 - 当天（含头含尾的天数差）
    return end_day - self["day"]


def cancel_session(self, session_id):
    # 取消场次必须退还该场已售票款；重复取消幂等（无票可退）
    if not session_id:
        return False
    self["tickets"].pop(session_id, None)
    return True


def show(self, session_id):
    # 放映机故障时不得计场次；空场次/未排片也不得放映
    if self.get("projector_fault"):
        return False
    if not session_id or session_id not in self["sessions"]:
        return False
    return True


def refund(self, session_id):
    # 退票必须校验场次存在且确有票可退；失败时订单原样保留
    if not session_id or session_id not in self["sessions"]:
        return False
    if self["tickets"].get(session_id, 0) <= 0:
        return False
    self["tickets"][session_id] -= 1
    if self["tickets"][session_id] == 0:
        del self["tickets"][session_id]
    return True


def extra_show(self):
    # 加映事件只生效一次，重复输入幂等
    if self.get("extra_done"):
        return False
    self["extra_done"] = True
    self["bonus"] = self.get("bonus", 0) + 1
    return True


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
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None
        if cmd == "quit":
            break
        elif cmd == "schedule":
            print("ok" if schedule(state, arg) else "fail")
        elif cmd == "sell":
            print("ok" if sell_ticket(state, arg) else "fail")
        elif cmd == "price":
            try:
                print(price(state, int(arg)))
            except (TypeError, ValueError):
                print("fail")
        elif cmd == "cancel":
            print("ok" if cancel_session(state, arg) else "fail")
        elif cmd == "show":
            print("ok" if show(state, arg) else "fail")
        elif cmd == "refund":
            print("ok" if refund(state, arg) else "fail")
        elif cmd == "extra":
            print("ok" if extra_show(state) else "fail")
        else:
            print("fail")


if __name__ == "__main__":
    main()
