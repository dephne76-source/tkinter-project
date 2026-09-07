"""키오스크 애플리케이션의 메인 컨트롤러."""

import tkinter as tk

from .data import MENU_ITEMS
from .order import Order
from .screens.start import StartScreen
from .screens.order_type import OrderTypeScreen
from .screens.menu import MenuScreen
from .screens.payment import PaymentScreen
from .screens.complete import CompleteScreen

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

BG_COLOR = "#f2f2f2"


class KioskApp(tk.Tk):
    """화면 전환을 담당하는 최상위 애플리케이션."""

    def __init__(self):
        super().__init__()
        self.title("무인 주문 키오스크")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.configure(bg=BG_COLOR)

        # 실제 키오스크 환경에서는 전체화면으로 구동하되,
        # 관리자가 Ctrl+Q 로 종료할 수 있도록 단축키를 둔다.
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.bind("<Control-q>", lambda e: self.destroy())

        self.catalog = {item.id: item for item in MENU_ITEMS}
        self.order = Order()

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container

        self.frames: dict[str, tk.Frame] = {}
        for ScreenClass in (StartScreen, OrderTypeScreen, MenuScreen, PaymentScreen, CompleteScreen):
            frame = ScreenClass(parent=container, app=self)
            self.frames[ScreenClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartScreen")

    def show_frame(self, name: str):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    def start_new_order(self):
        self.order.reset()
        self.show_frame("OrderTypeScreen")

    def cancel_to_start(self):
        self.order.reset()
        self.show_frame("StartScreen")


def run():
    app = KioskApp()
    app.mainloop()
