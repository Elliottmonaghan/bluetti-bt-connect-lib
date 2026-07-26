import struct

from . import DeviceField, FieldName


class SInt32Field(DeviceField):
    """A signed 32-bit integer spanning two consecutive 16-bit registers.

    Some registers (e.g. 32-bit combined power/energy totals) are reported
    as two consecutive big-endian registers forming a signed 32-bit value.
    """

    def __init__(
        self,
        name: FieldName,
        address: int,
        multiplier: float = 1,
        min: int | None = None,
        max: int | None = None,
    ):
        super().__init__(name, address, 2)
        self.multiplier = multiplier
        self.min = min
        self.max = max

    def parse(self, data: bytes) -> float:
        val = struct.unpack("!i", data)[0]
        if self.multiplier != 1:
            val = round(val * self.multiplier, 2)
        return val

    def in_range(self, value: float) -> bool:
        if self.min is not None and self.min > value:
            return False
        if self.max is not None and self.max < value:
            return False
        return True
