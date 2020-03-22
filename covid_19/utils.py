from typing import *

import hug
import pandas as pd


def expose(func):
    """Expose function over http and as a cli command."""
    return hug.get()(hug.cli()(func))


def to_records(df: pd.DataFrame) -> List[dict]:
    """Convert a datafram to a list of dictionaries minus the index."""
    return [
        {k: v for k, v in row.items() if k != "index"}
        for row in df.to_dict(orient="records")
    ]
