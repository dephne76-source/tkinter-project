"""시작 화면: 화면 전체를 터치하면 주문이 시작된다."""

import tkinter as tk


class StartScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2b2f77")
        self.app = app

        title = tk.Label(
            self,
            text="어서오세요!",
            font=("맑은 고딕", 48, "bold"),
            fg="white",
            bg="#2b2f77",
        )
        title.pack(expand=True)

        subtitle = tk.Label(
            self,
            text="화면을 터치하여 주문을 시작하세요",
            font=("맑은 고딕", 22),
            fg="#dcdcff",
            bg="#2b2f77",
        )
        subtitle.pack(pady=(0, 40))

        start_button = tk.Button(
            self,
            text="주문 시작하기",
            font=("맑은 고딕", 26, "bold"),
            bg="#ffcc00",
            fg="#2b2f77",
            activebackground="#ffe680",
            relief="flat",
            width=20,
            height=2,
            command=self.app.start_new_order,
        )
        start_button.pack(pady=(0, 80))

        # 화면 어디를 터치해도 시작되도록 전체 프레임에 클릭 이벤트를 건다.
        self.bind("<Button-1>", lambda e: self.app.start_new_order())
        title.bind("<Button-1>", lambda e: self.app.start_new_order())
        subtitle.bind("<Button-1>", lambda e: self.app.start_new_order())
