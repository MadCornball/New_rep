from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class TransferType(AutoName):
    MAIN_UMFUTURE = auto()
    MAIN_CMFUTURE = auto()
    MAIN_MARGIN = auto()
    UMFUTURE_MAIN = auto()
    UMFUTURE_MARGIN = auto()
    CMFUTURE_MAIN = auto()
    CMFUTURE_MARGIN = auto()
    MARGIN_MAIN = auto()
    MARGIN_UMFUTURE = auto()
    MARGIN_CMFUTURE = auto()
    ISOLATEDMARGIN_MARGIN = auto()
    MARGIN_ISOLATEDMARGIN = auto()
    ISOLATEDMARGIN_ISOLATEDMARGIN = auto()
    MAIN_FUNDING = auto()
    FUNDING_MAIN = auto()
    FUNDING_UMFUTURE = auto()
    UMFUTURE_FUNDING = auto()
    MARGIN_FUNDING = auto()
    FUNDING_MARGIN = auto()
    FUNDING_CMFUTURE = auto()
    CMFUTURE_FUNDING = auto()