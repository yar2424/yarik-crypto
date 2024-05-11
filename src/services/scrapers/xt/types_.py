from typing_extensions import TypedDict


class TickerData(TypedDict):
    s: str  # Symbol
    t: int  # Time as Unix timestamp
    cv: float  # Change in volume as float
    cr: float  # Change rate as float
    o: float  # Open price as float
    c: float  # Close price as float
    h: float  # High price as float
    l: float  # Low price as float
    q: float  # Quote volume in USDT as float
    v: float  # Base volume in traded cryptocurrency as float
