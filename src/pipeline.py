from .analysis import summarize_graph
from .biological_validation import validate_communities_by_entity
from .centrality import compute_centralities
from .community import run_louvain
from .config import PipelineConfig
from .downloader import download_mmcif
from .graph_builder import build_contact_graph
from .io_utils import ensure_output_directories, save_dataframe, save_edges, save_json
from .parser import extract_residue_ca_nodes
from .visualization import (
    plot_centrality_3d,
    plot_communities_3d,
    plot_degree_distribution,
)


def run_pipeline(config: PipelineConfig) -> None:
    ensure_output_directories(
        config.raw_dir,
        config.processed_dir,
        config.results_dir,
        config.figures_dir,
    )

    pdb_id = config.pdb_id
    prefix = pdb_id.upper()

    print(f"Processando {pdb_id}...")
    structure_path = download_mmcif(pdb_id, config.raw_dir)

    nodes = extract_residue_ca_nodes(structure_path)
    save_dataframe(config.processed_dir / f"{prefix}_nodes.csv", nodes)
    print(f"  resíduos Cα: {len(nodes):,}")

    graph, pairs = build_contact_graph(nodes, config.cutoff_angstrom)
    save_edges(config.processed_dir / f"{prefix}_edges.csv", pairs)

    graph_summary = summarize_graph(pdb_id, graph, config.cutoff_angstrom)
    save_json(config.results_dir / f"{prefix}_graph_summary.json", graph_summary)

    centrality_table, centrality_summary = compute_centralities(
        graph,
        nodes,
        pdb_id,
        config.cutoff_angstrom,
    )
    save_dataframe(
        config.results_dir / f"{prefix}_centralities.csv",
        centrality_table,
    )
    save_json(
        config.results_dir / f"{prefix}_centrality_summary.json",
        centrality_summary,
    )

    membership, louvain_summary = run_louvain(
        graph,
        config.louvain_resolution,
        config.louvain_seed,
    )
    membership_table = nodes[
        [
            "node_index",
            "chain_id",
            "entity_id",
            "residue_number",
            "insertion_code",
            "residue_name",
        ]
    ].copy()
    membership_table["louvain_community"] = membership
    save_dataframe(
        config.results_dir / f"{prefix}_louvain_membership.csv",
        membership_table,
    )

    louvain_summary = {
        "pdb_id": prefix,
        "cutoff_angstrom": config.cutoff_angstrom,
        **louvain_summary,
    }
    save_json(
        config.results_dir / f"{prefix}_louvain_summary.json",
        louvain_summary,
    )

    if config.validate_entities:
        contingency, entity_metrics, community_metrics, validation_summary = (
            validate_communities_by_entity(nodes, membership)
        )
        contingency.to_csv(
            config.results_dir / f"{prefix}_entity_community_contingency.csv"
        )
        save_dataframe(
            config.results_dir / f"{prefix}_entity_metrics.csv",
            entity_metrics,
        )
        save_dataframe(
            config.results_dir / f"{prefix}_community_purity.csv",
            community_metrics,
        )
        save_json(
            config.results_dir / f"{prefix}_biological_validation.json",
            validation_summary,
        )
    else:
        validation_summary = None

    plot_degree_distribution(
        pdb_id,
        graph,
        config.cutoff_angstrom,
        config.figures_dir / f"{prefix}_degree_distribution.png",
    )
    plot_centrality_3d(
        pdb_id,
        centrality_table,
        centrality_table["degree"],
        "Centralidade de grau",
        config.cutoff_angstrom,
        config.figures_dir / f"{prefix}_degree_centrality_3d.png",
    )
    plot_centrality_3d(
        pdb_id,
        centrality_table,
        centrality_table["eigenvector_centrality"],
        "Centralidade de autovetor",
        config.cutoff_angstrom,
        config.figures_dir / f"{prefix}_eigenvector_centrality_3d.png",
    )
    plot_communities_3d(
        pdb_id,
        nodes,
        membership,
        louvain_summary["modularity"],
        config.louvain_resolution,
        config.cutoff_angstrom,
        config.figures_dir / f"{prefix}_louvain_communities_3d.png",
    )

    print(
        f"  grafo: {graph.vcount():,} vértices e {graph.ecount():,} arestas\n"
        f"  grau médio: {graph_summary['grau_medio']:.2f}\n"
        f"  comunidades: {louvain_summary['number_of_communities']}\n"
        f"  modularidade: {louvain_summary['modularity']:.4f}"
    )
    if validation_summary is not None:
        print(
            "  pureza ponderada: "
            f"{validation_summary['weighted_community_purity']:.4f}"
        )
    print("Concluído.")
