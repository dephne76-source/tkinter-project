"""메뉴 데이터 정의."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItem:
    id: str
    name: str
    price: int
    category: str
    description: str = ""


CATEGORIES = ["버거", "사이드", "음료", "디저트"]

MENU_ITEMS = [
    MenuItem("burger_classic", "클래식 버거", 5900, "버거", "순 쇠고기 패티와 신선한 채소"),
    MenuItem("burger_cheese", "치즈 버거", 6500, "버거", "고소한 치즈가 두 배"),
    MenuItem("burger_bulgogi", "불고기 버거", 6200, "버거", "달콤한 불고기 소스"),
    MenuItem("burger_spicy", "스파이시 치킨 버거", 6800, "버거", "매콤한 치킨 패티"),
    MenuItem("side_fries", "감자튀김", 2500, "사이드", "바삭한 감자튀김"),
    MenuItem("side_nuggets", "치킨너겟(6조각)", 3500, "사이드", "겉바속촉 너겟"),
    MenuItem("side_salad", "가든 샐러드", 3000, "사이드", "신선한 채소 샐러드"),
    MenuItem("drink_cola", "콜라", 2000, "음료", "시원한 탄산음료"),
    MenuItem("drink_cider", "사이다", 2000, "음료", "청량한 탄산음료"),
    MenuItem("drink_coffee", "아메리카노", 2500, "음료", "깊은 풍미의 커피"),
    MenuItem("drink_juice", "오렌지 주스", 2800, "음료", "상큼한 과일 주스"),
    MenuItem("dessert_icecream", "소프트아이스크림", 1800, "디저트", "부드러운 아이스크림"),
    MenuItem("dessert_pie", "애플파이", 2200, "디저트", "따뜻한 애플파이"),
    MenuItem("dessert_cookie", "초코쿠키", 1500, "디저트", "달콤한 초코쿠키"),
]


def items_by_category(category: str):
    return [item for item in MENU_ITEMS if item.category == category]
