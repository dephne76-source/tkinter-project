"""결제 화면: 결제 수단 선택 및 결제 진행 시뮬레이션."""

import tkinter as tk

from ..order import next_order_number


class PaymentScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f2f2f2")
        self.app = app
        self.selected_method = tk.StringVar(value="")

        tk.Label(
            self, text="결제 수단을 선택해주세요", font=("맑은 고딕", 28, "bold"), bg="#f2f2f2"
        ).pack(pady=(60, 20))

        self.summary_label = tk.Label(self, text="", font=("맑은 고딕", 20), bg="#f2f2f2")
        self.summary_label.pack(pady=(0, 40))

        method_area = tk.Frame(self, bg="#f2f2f2")
        method_area.pack()
        for method in ("신용카드", "현금", "간편결제"):
            tk.Button(
                method_area,
                text=method,
                font=("맑은 고딕", 18, "bold"),
                width=12,
                height=4,
                relief="flat",
                bg="#3b6fd8",
                fg="white",
                command=lambda m=method: self._pay(m),
            ).pack(side="left", padx=15)

        self.status_label = tk.Label(self, text="", font=("맑은 고딕", 16), bg="#f2f2f2")
        self.status_label.pack(pady=30)

        tk.Button(
            self,
            text="이전으로",
            font=("맑은 고딕", 14),
            relief="flat",
            command=lambda: self.app.show_frame("MenuScreen"),
        ).pack(side="bottom", pady=20)

    def on_show(self):
        order = self.app.order
        total = order.total_price(self.app.catalog)
        self.summary_label.configure(
            text=f"주문 유형: {order.dine_type}   |   총 수량: {order.total_count}개   |   총 금액: {total:,}원"
        )
        self.status_label.configure(text="")

    def _pay(self, method):
        self.status_label.configure(text=f"{method} 결제를 진행 중입니다...")
        self.update_idletasks()
        self.after(1200, lambda: self._finish_payment(method))

    def _finish_payment(self, method):
        order_number = next_order_number()
        self.app.last_order_number = order_number
        self.app.last_payment_method = method
        self.app.show_frame("CompleteScreen")
