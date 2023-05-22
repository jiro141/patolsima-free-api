from decimal import Decimal


def round_2_decimals(val: Decimal) -> Decimal:
    return val.quantize(Decimal(".01"))
