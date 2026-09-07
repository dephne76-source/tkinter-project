"""매장식사 / 포장 선택 화면."""

import tkinter as tk


class OrderTypeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f2f2f2")
        self.app = app

        tk.Label(
            self,
            text="주문 방법을 선택해주세요",
            font=("맑은 고딕", 32, "bold"),
            bg="#f2f2f2",
        ).pack(pady=(100, 60))

        button_area = tk.Frame(self, bg="#f2f2f2")
        button_area.pack(expand=True)

        self._make_choice_button(button_area, "매장 식사", "#3b8f3b").grid(row=0, column=0, padx=30)
        self._make_choice_button(button_area, "포장", "#3b6fd8").grid(row=0, column=1, padx=30)

        tk.Button(
            self,
            text="취소",
            font=("맑은 고딕", 14),
            relief="flat",
            command=self.app.cancel_to_start,
        ).pack(side="bottom", pady=30)

    def _make_choice_button(self, parent, label, color):
        return tk.Button(
            parent,
            text=label,
            font=("맑은 고딕", 24, "bold"),
            fg="white",
            bg=color,
            activebackground=color,
            relief="flat",
            width=14,
            height=5,
            command=lambda: self._choose(label),
        )

    def _choose(self, dine_type):
        self.app.order.dine_type = dine_type
        self.app.show_frame("MenuScreen")
