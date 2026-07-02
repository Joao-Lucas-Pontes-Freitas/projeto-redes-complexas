import random

import igraph as ig


def run_louvain(
    graph: ig.Graph,
    resolution: float,
    seed: int,
) -> tuple[tuple[int, ...], dict]:
    if graph.vcount() == 0:
        raise ValueError("O grafo não possui vértices.")
    if graph.is_directed():
        raise ValueError("Louvain exige um grafo não direcionado.")
    if resolution <= 0:
        raise ValueError("A resolução deve ser positiva.")

    ig.set_random_number_generator(random.Random(seed))
    clustering = graph.community_multilevel(
        weights=None,
        return_levels=False,
        resolution=float(resolution),
    )

    membership = tuple(int(value) for value in clustering.membership)
    summary = {
        "algorithm": "louvain",
        "resolution": float(resolution),
        "seed": int(seed),
        "number_of_communities": len(set(membership)),
        "modularity": float(clustering.modularity),
    }

    return membership, summary
