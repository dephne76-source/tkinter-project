"""메뉴 선택 화면: 카테고리 탭 + 상품 목록 + 장바구니."""

import tkinter as tk
from tkinter import messagebox

from ..data import CATEGORIES, items_by_category


class MenuScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f2f2f2")
        self.app = app
        self.current_category = CATEGORIES[0]
        self.cart_labels: dict[str, tk.Label] = {}

        self._build_header()
        self._build_category_tabs()

        body = tk.Frame(self, bg="#f2f2f2")
        body.pack(fill="both", expand=True, padx=20, pady=10)

        self.menu_area = tk.Frame(body, bg="#f2f2f2")
        self.menu_area.pack(side="left", fill="both", expand=True)

        self._build_cart_panel(body)

    # ---------- 화면 구성 ----------

    def _build_header(self):
        header = tk.Frame(self, bg="#2b2f77", height=60)
        header.pack(fill="x")
        tk.Label(
            header, text="메뉴 선택", font=("맑은 고딕", 20, "bold"), fg="white", bg="#2b2f77"
        ).pack(side="left", padx=20, pady=10)
        tk.Button(
            header,
            text="처음으로",
            font=("맑은 고딕", 12),
            relief="flat",
            command=self._confirm_cancel,
        ).pack(side="right", padx=20, pady=10)

    def _build_category_tabs(self):
        tab_bar = tk.Frame(self, bg="#e0e0e0")
        tab_bar.pack(fill="x")
        self.tab_buttons: dict[str, tk.Button] = {}
        for category in CATEGORIES:
            btn = tk.Button(
                tab_bar,
                text=category,
                font=("맑은 고딕", 16, "bold"),
                relief="flat",
                width=10,
                height=2,
                command=lambda c=category: self._select_category(c),
            )
            btn.pack(side="left", padx=2, pady=2)
            self.tab_buttons[category] = btn

    def _build_cart_panel(self, parent):
        panel = tk.Frame(parent, bg="white", width=300, relief="groove", bd=2)
        panel.pack(side="right", fill="y", padx=(15, 0))
        panel.pack_propagate(False)

        tk.Label(
            panel, text="장바구니", font=("맑은 고딕", 18, "bold"), bg="white"
        ).pack(pady=(15, 5))

        self.cart_items_frame = tk.Frame(panel, bg="white")
        self.cart_items_frame.pack(fill="both", expand=True, padx=10)

        self.total_label = tk.Label(
            panel, text="총 금액: 0원", font=("맑은 고딕", 18, "bold"), bg="white"
        )
        self.total_label.pack(pady=10)

        self.checkout_button = tk.Button(
            panel,
            text="결제하기",
            font=("맑은 고딕", 16, "bold"),
            bg="#ffcc00",
            relief="flat",
            height=2,
            command=self._go_to_payment,
        )
        self.checkout_button.pack(fill="x", padx=15, pady=(0, 15))

    # ---------- 화면 갱신 ----------

    def on_show(self):
        self._select_category(CATEGORIES[0])
        self._refresh_cart()

    def _select_category(self, category):
        self.current_category = category
        for name, btn in self.tab_buttons.items():
            btn.configure(bg="#3b6fd8" if name == category else "#e0e0e0",
                          fg="white" if name == category else "black")

        for widget in self.menu_area.winfo_children():
            widget.destroy()

        items = items_by_category(category)
        columns = 3
        for index, item in enumerate(items):
            row, col = divmod(index, columns)
            self._make_item_card(self.menu_area, item).grid(
                row=row, column=col, padx=10, pady=10, sticky="nsew"
            )
        for col in range(columns):
            self.menu_area.grid_columnconfigure(col, weight=1)

    def _make_item_card(self, parent, item):
        card = tk.Frame(parent, bg="white", relief="raised", bd=1, width=220, height=160)
        card.grid_propagate(False)

        tk.Label(
            card, text=item.name, font=("맑은 고딕", 15, "bold"), bg="white", wraplength=200
        ).pack(pady=(12, 4))
        tk.Label(
            card, text=item.description, font=("맑은 고딕", 10), bg="white", fg="#666666",
            wraplength=200,
        ).pack()
        tk.Label(
            card, text=f"{item.price:,}원", font=("맑은 고딕", 13, "bold"), bg="white", fg="#c0392b"
        ).pack(pady=(4, 8))
        tk.Button(
            card,
            text="담기",
            font=("맑은 고딕", 12, "bold"),
            bg="#3b8f3b",
            fg="white",
            relief="flat",
            command=lambda: self._add_to_cart(item),
        ).pack(fill="x", padx=15)
        return card

    def _add_to_cart(self, item):
        self.app.order.add_item(item)
        self._refresh_cart()

    def _refresh_cart(self):
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        order = self.app.order
        catalog = self.app.catalog

        if order.is_empty():
            tk.Label(
                self.cart_items_frame, text="담긴 메뉴가 없습니다", bg="white", fg="#999999"
            ).pack(pady=20)
        else:
            for item_id, qty in order.lines.items():
                item = catalog[item_id]
                row = tk.Frame(self.cart_items_frame, bg="white")
                row.pack(fill="x", pady=4)

                tk.Label(
                    row, text=f"{item.name}", font=("맑은 고딕", 11), bg="white", anchor="w"
                ).pack(side="top", fill="x")

                sub = tk.Frame(row, bg="white")
                sub.pack(fill="x")
                tk.Button(
                    sub, text="-", width=2, relief="flat",
                    command=lambda i=item_id: self._remove_one(i),
                ).pack(side="left")
                tk.Label(sub, text=str(qty), bg="white", width=3).pack(side="left")
                tk.Button(
                    sub, text="+", width=2, relief="flat",
                    command=lambda i=item: self._add_to_cart(i),
                ).pack(side="left")
                tk.Label(
                    sub, text=f"{item.price * qty:,}원", bg="white", anchor="e"
                ).pack(side="right")
                tk.Button(
                    sub, text="삭제", fg="#c0392b", relief="flat",
                    command=lambda i=item_id: self._delete_item(i),
                ).pack(side="right", padx=4)

        total = order.total_price(catalog)
        self.total_label.configure(text=f"총 금액: {total:,}원")
        self.checkout_button.configure(state="normal" if not order.is_empty() else "disabled")

    def _remove_one(self, item_id):
        self.app.order.remove_item(item_id)
        self._refresh_cart()

    def _delete_item(self, item_id):
        self.app.order.delete_item(item_id)
        self._refresh_cart()

    def _confirm_cancel(self):
        if self.app.order.is_empty() or messagebox.askyesno(
            "주문 취소", "주문을 취소하고 처음 화면으로 돌아가시겠습니까?"
        ):
            self.app.cancel_to_start()

    def _go_to_payment(self):
        if self.app.order.is_empty():
            return
        self.app.show_frame("PaymentScreen")
