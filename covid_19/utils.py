from typing import *

import hug
import pandas as pd


def expose(func=None, output=hug.output_format.pretty_json):
    """Expose function over http and as a cli command."""

    def decorator(f):
        return hug.get(output=output)(hug.cli(output=output)(func))

    if func is not None:
        return decorator(func)
    else:
        return decorator


def to_records(df: pd.DataFrame) -> List[dict]:
    """Convert a datafram to a list of dictionaries minus the index."""
    return [
        {k: v for k, v in row.items() if k != "index"}
        for row in df.to_dict(orient="records")
    ]
