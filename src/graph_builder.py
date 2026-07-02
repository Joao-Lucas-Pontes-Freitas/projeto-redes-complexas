import igraph as ig
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


def build_contact_graph(
    nodes: pd.DataFrame,
    cutoff_angstrom: float,
) -> tuple[ig.Graph, np.ndarray]:
    if cutoff_angstrom <= 0:
        raise ValueError("O cutoff deve ser positivo.")

    coordinates = nodes[["x", "y", "z"]].to_numpy(dtype=np.float32, copy=True)

    if len(coordinates) < 2:
        pairs = np.empty((0, 2), dtype=np.int64)
    else:
        pairs = cKDTree(coordinates).query_pairs(
            r=cutoff_angstrom,
            output_type="ndarray",
        )
        pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)

    graph = ig.Graph(n=len(nodes), edges=pairs, directed=False)
    return graph, pairs
