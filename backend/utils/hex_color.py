from random import choice

HEX_LITERAL = "0123456789abcdef"


def generate_hex_color():
    return "#" + "".join(choice(HEX_LITERAL) for _ in range(6))


HEX_COLORS = [
    "#b81c1c",
    "#43bf43",
    "#3333d6",
    "#abab09",
    "#e820e8",
    "#21cccc",
    "#f08b26",
    "#bf4582",
    "#a1e85a",
    "#327ec9",
    "#581799",
    "#43916a",
    "#ed7291",
    "#ab4624",
]


def get_hex_colors(n: int) -> list[str]:
    return HEX_COLORS[:n] + [generate_hex_color() for _ in range(n - len(HEX_COLORS))]
