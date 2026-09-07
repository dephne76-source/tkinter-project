"""주문(장바구니) 상태 관리."""

import itertools

from .data import MenuItem

_order_number_counter = itertools.count(1)


class Order:
    """현재 진행 중인 주문 상태를 담는 객체."""

    def __init__(self):
        self.dine_type: str | None = None  # "매장" 또는 "포장"
        self.lines: dict[str, int] = {}  # item.id -> quantity

    def reset(self):
        self.dine_type = None
        self.lines.clear()

    def add_item(self, item: MenuItem, qty: int = 1):
        self.lines[item.id] = self.lines.get(item.id, 0) + qty

    def remove_item(self, item_id: str):
        if item_id in self.lines:
            self.lines[item_id] -= 1
            if self.lines[item_id] <= 0:
                del self.lines[item_id]

    def delete_item(self, item_id: str):
        self.lines.pop(item_id, None)

    @property
    def total_count(self) -> int:
        return sum(self.lines.values())

    def total_price(self, catalog: dict[str, MenuItem]) -> int:
        return sum(catalog[item_id].price * qty for item_id, qty in self.lines.items())

    def is_empty(self) -> bool:
        return not self.lines


def next_order_number() -> int:
    return next(_order_number_counter)
