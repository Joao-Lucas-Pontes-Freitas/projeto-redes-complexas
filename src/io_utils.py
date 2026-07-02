import json
from pathlib import Path

import numpy as np
import pandas as pd


def ensure_output_directories(*directories: Path) -> None:
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def save_dataframe(path: Path, dataframe: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path, index=False)


def save_edges(path: Path, pairs: np.ndarray) -> None:
    dataframe = pd.DataFrame(pairs, columns=["source", "target"])
    save_dataframe(path, dataframe)
