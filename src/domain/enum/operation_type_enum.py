from enum import StrEnum


class OperationType(StrEnum):
    RENT = "rent"
    SALE = "sale"

    @property
    def zonaprop_value(self) -> str:
        return "alquiler" if self is OperationType.RENT else "venta"
