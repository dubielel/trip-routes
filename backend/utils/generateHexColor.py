from random import choice

HEX_LITERAL = "0123456789abcdef"


def generate_hex_color():
    return "#" + "".join(choice(HEX_LITERAL) for _ in range(6))
