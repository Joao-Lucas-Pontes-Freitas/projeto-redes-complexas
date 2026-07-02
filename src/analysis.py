import igraph as ig


def summarize_graph(
    pdb_id: str,
    graph: ig.Graph,
    cutoff_angstrom: float,
) -> dict:
    degrees = graph.degree()

    return {
        "pdb_id": pdb_id.upper(),
        "cutoff_angstrom": float(cutoff_angstrom),
        "vertices": graph.vcount(),
        "arestas": graph.ecount(),
        "grau_minimo": min(degrees) if degrees else 0,
        "grau_medio": sum(degrees) / len(degrees) if degrees else 0.0,
        "grau_maximo": max(degrees) if degrees else 0,
    }
