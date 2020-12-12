from typing import NamedTuple
from pathlib import Path

import pandas as pd


class AttendeeReport(NamedTuple):
    no: int
    csv: pd.DataFrame

    @classmethod
    def build(cls, csv_file: Path):
        return cls(
            no=int(csv_file.name.split("_")[0]),
            csv=pd.read_csv(csv_file, encoding="utf_8_sig"),
        )
