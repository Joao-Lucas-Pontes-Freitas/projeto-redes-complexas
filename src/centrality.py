import warnings

import igraph as ig
import numpy as np
import pandas as pd


def compute_centralities(
    graph: ig.Graph,
    nodes: pd.DataFrame,
    pdb_id: str,
    cutoff_angstrom: float,
) -> tuple[pd.DataFrame, dict]:
    if graph.vcount() == 0:
        raise ValueError("O grafo não possui vértices.")
    if graph.is_directed():
        raise ValueError("As centralidades exigem um grafo não direcionado.")
    if graph.vcount() != len(nodes):
        raise ValueError("O número de vértices não corresponde à tabela de resíduos.")
    if not graph.is_connected():
        raise ValueError("A centralidade de autovetor exige um grafo conectado.")

    degree = np.asarray(graph.degree(), dtype=np.int64)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Some eigenvector centralities are nearly zero.*",
            category=RuntimeWarning,
        )
        eigenvector = np.asarray(
            graph.eigenvector_centrality(scale=True, weights=None),
            dtype=np.float64,
        )

    columns = [
        "node_index",
        "chain_id",
        "entity_id",
        "residue_number",
        "insertion_code",
        "residue_name",
        "x",
        "y",
        "z",
    ]
    table = nodes[columns].copy()
    table["degree"] = degree
    table["eigenvector_centrality"] = eigenvector

    top_degree = table.loc[table["degree"].idxmax()]
    top_eigenvector = table.loc[table["eigenvector_centrality"].idxmax()]

    summary = {
        "pdb_id": pdb_id.upper(),
        "cutoff_angstrom": float(cutoff_angstrom),
        "top_degree_chain_id": str(top_degree["chain_id"]),
        "top_degree_residue_number": int(top_degree["residue_number"]),
        "top_degree_residue_name": str(top_degree["residue_name"]),
        "top_degree_value": int(top_degree["degree"]),
        "top_eigenvector_chain_id": str(top_eigenvector["chain_id"]),
        "top_eigenvector_residue_number": int(top_eigenvector["residue_number"]),
        "top_eigenvector_residue_name": str(top_eigenvector["residue_name"]),
        "top_eigenvector_value": float(top_eigenvector["eigenvector_centrality"]),
    }

    return table, summary
