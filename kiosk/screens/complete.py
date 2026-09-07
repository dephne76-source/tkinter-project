"""주문 완료 화면: 주문번호를 안내하고 일정 시간 후 시작 화면으로 복귀."""

import tkinter as tk

AUTO_RETURN_MS = 8000


class CompleteScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2b2f77")
        self.app = app
        self._after_id = None

        tk.Label(
            self, text="주문이 완료되었습니다!", font=("맑은 고딕", 34, "bold"),
            fg="white", bg="#2b2f77",
        ).pack(pady=(120, 20))

        self.order_number_label = tk.Label(
            self, text="", font=("맑은 고딕", 60, "bold"), fg="#ffcc00", bg="#2b2f77"
        )
        self.order_number_label.pack(pady=20)

        self.detail_label = tk.Label(
            self, text="", font=("맑은 고딕", 18), fg="#dcdcff", bg="#2b2f77"
        )
        self.detail_label.pack(pady=10)

        tk.Label(
            self, text="화면에 표시된 번호가 호출되면 픽업대에서 수령해주세요",
            font=("맑은 고딕", 16), fg="#dcdcff", bg="#2b2f77",
        ).pack(pady=(30, 10))

        tk.Button(
            self,
            text="처음으로 돌아가기",
            font=("맑은 고딕", 16, "bold"),
            bg="#ffcc00",
            relief="flat",
            command=self._return_now,
        ).pack(pady=40)

    def on_show(self):
        order_number = getattr(self.app, "last_order_number", 0)
        method = getattr(self.app, "last_payment_method", "")
        self.order_number_label.configure(text=f"No. {order_number}")
        self.detail_label.configure(text=f"결제 수단: {method}")

        if self._after_id is not None:
            self.after_cancel(self._after_id)
        self._after_id = self.after(AUTO_RETURN_MS, self._return_now)

    def _return_now(self):
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        self.app.cancel_to_start()
