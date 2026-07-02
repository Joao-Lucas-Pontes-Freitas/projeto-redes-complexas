import numpy as np
import pandas as pd


def validate_communities_by_entity(
    nodes: pd.DataFrame,
    membership: tuple[int, ...],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    if len(nodes) != len(membership):
        raise ValueError("O vetor de comunidades não corresponde aos resíduos.")

    assignments = nodes[["entity_id"]].copy()
    assignments["entity_id"] = assignments["entity_id"].astype(str)
    assignments["louvain_community"] = np.asarray(membership, dtype=np.int64)
    assignments = assignments[assignments["entity_id"] != ""]

    if assignments.empty:
        raise ValueError("A estrutura não possui entidades anotadas para validação.")

    contingency = pd.crosstab(
        assignments["entity_id"],
        assignments["louvain_community"],
    )

    entity_metrics = pd.DataFrame(
        [
            {
                "entity_id": str(entity_id),
                "residue_count": int(counts.sum()),
                "dominant_community": int(counts.idxmax()),
                "dominant_count": int(counts.max()),
                "dominant_community_coverage": float(counts.max() / counts.sum()),
            }
            for entity_id, counts in contingency.iterrows()
        ]
    )

    community_metrics = pd.DataFrame(
        [
            {
                "louvain_community": int(community_id),
                "residue_count": int(counts.sum()),
                "dominant_entity_id": str(counts.idxmax()),
                "dominant_count": int(counts.max()),
                "entity_purity": float(counts.max() / counts.sum()),
            }
            for community_id, counts in contingency.items()
        ]
    )

    total_residues = int(contingency.to_numpy().sum())
    summary = {
        "entity_count": int(contingency.shape[0]),
        "community_count": int(contingency.shape[1]),
        "annotated_residue_count": total_residues,
        "weighted_community_purity": float(
            contingency.max(axis=0).sum() / total_residues
        ),
    }

    return contingency, entity_metrics, community_metrics, summary
