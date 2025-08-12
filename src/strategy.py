import pandas as pd
from dataclasses import dataclass

@dataclass
class Signals:
    weight: pd.Series  # values in [0,1], index aligned to data

class SmaCross:
    def __init__(self, fast_col: str = "sma_fast", slow_col: str = "sma_slow"):
        self.fast_col = fast_col
        self.slow_col = slow_col

    def generate(self, feats: pd.DataFrame) -> Signals:
        raw = (feats[self.fast_col] > feats[self.slow_col]).astype(float)
        weight = raw.shift(1).fillna(0.0)  # shift to avoid lookahead bias
        return Signals(weight=weight)
