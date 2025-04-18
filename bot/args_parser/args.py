from bot.consts import DURATION_PATTERN


class Duration:
    _pattern = DURATION_PATTERN

    def __init__(self, value: str):
        if not self._pattern.fullmatch(value):
            raise ValueError('duration must comply with format "[int|float][d|h|m|s]"')

        self.value = float(value[:-1])
        self.unit = value[-1]

    def to_seconds(self) -> int:
        if self.unit == "d":
            seconds = self.value * 3600 * 24
        elif self.unit == "h":
            seconds = self.value * 3600
        elif self.unit == "m":
            seconds = self.value * 60
        else:
            seconds = self.value

        return int(seconds)
