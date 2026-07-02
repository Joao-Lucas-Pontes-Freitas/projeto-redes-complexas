from pathlib import Path

import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _set_equal_aspect(axis, nodes: pd.DataFrame) -> None:
    coordinates = nodes[["x", "y", "z"]].to_numpy(dtype=np.float64)
    axis.set_box_aspect(np.maximum(np.ptp(coordinates, axis=0), 1.0))


def plot_degree_distribution(
    pdb_id: str,
    graph: ig.Graph,
    cutoff_angstrom: float,
    output_path: Path,
) -> None:
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.hist(graph.degree(), bins="auto")
    axis.set_xlabel("Grau")
    axis.set_ylabel("Quantidade de resíduos")
    axis.set_title(
        f"{pdb_id.upper()} — distribuição de graus " f"(cutoff={cutoff_angstrom:.1f} Å)"
    )
    axis.grid(alpha=0.25)
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(figure)


def plot_centrality_3d(
    pdb_id: str,
    nodes: pd.DataFrame,
    values: pd.Series,
    metric_label: str,
    cutoff_angstrom: float,
    output_path: Path,
) -> None:
    figure = plt.figure(figsize=(9, 7))
    axis = figure.add_subplot(111, projection="3d")
    scatter = axis.scatter(
        nodes["x"],
        nodes["y"],
        nodes["z"],
        c=values,
        s=8 if len(nodes) > 5_000 else 18,
    )
    _set_equal_aspect(axis, nodes)
    axis.set_xlabel("x (Å)")
    axis.set_ylabel("y (Å)")
    axis.set_zlabel("z (Å)")
    axis.set_title(
        f"{pdb_id.upper()} — {metric_label}\n" f"cutoff={cutoff_angstrom:.1f} Å"
    )
    colorbar = figure.colorbar(scatter, ax=axis, pad=0.10, shrink=0.70)
    colorbar.set_label(metric_label)
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(figure)


def plot_communities_3d(
    pdb_id: str,
    nodes: pd.DataFrame,
    membership: tuple[int, ...],
    modularity: float,
    resolution: float,
    cutoff_angstrom: float,
    output_path: Path,
) -> None:
    figure = plt.figure(figsize=(9, 7))
    axis = figure.add_subplot(111, projection="3d")
    scatter = axis.scatter(
        nodes["x"],
        nodes["y"],
        nodes["z"],
        c=np.asarray(membership, dtype=np.int64),
        s=8 if len(nodes) > 5_000 else 18,
    )
    _set_equal_aspect(axis, nodes)
    axis.set_xlabel("x (Å)")
    axis.set_ylabel("y (Å)")
    axis.set_zlabel("z (Å)")
    axis.set_title(
        f"{pdb_id.upper()} — comunidades Louvain\n"
        f"{len(set(membership))} comunidades, modularidade={modularity:.4f}, "
        f"resolução={resolution:g}, cutoff={cutoff_angstrom:.1f} Å"
    )
    colorbar = figure.colorbar(scatter, ax=axis, pad=0.10, shrink=0.70)
    colorbar.set_label("Comunidade Louvain")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(figure)
