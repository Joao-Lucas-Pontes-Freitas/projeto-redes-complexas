from pathlib import Path

import gemmi
import numpy as np
import pandas as pd


def _clean_text(value: object) -> str:
    text = str(value).strip()
    return "" if text in {"", ".", "?", "\x00", "None"} else text


def _select_ca_atom(residue: gemmi.Residue):
    candidates = [atom for atom in residue if atom.name.strip().upper() == "CA"]
    if not candidates:
        return None

    preferred = [atom for atom in candidates if _clean_text(atom.altloc) in {"", "A"}]
    return max(preferred or candidates, key=lambda atom: float(atom.occ))


def extract_residue_ca_nodes(structure_path: Path) -> pd.DataFrame:
    structure = gemmi.read_structure(str(structure_path), merge_chain_parts=False)
    if len(structure) == 0:
        raise ValueError(f"Nenhum modelo encontrado em {structure_path}")

    model = structure[0]
    records: list[dict] = []

    for chain in model:
        for residue in chain:
            residue_info = gemmi.find_tabulated_residue(residue.name.strip())
            if not residue_info.is_amino_acid():
                continue

            ca_atom = _select_ca_atom(residue)
            if ca_atom is None:
                continue

            records.append(
                {
                    "node_index": len(records),
                    "chain_id": _clean_text(chain.name),
                    "entity_id": _clean_text(residue.entity_id),
                    "residue_number": int(residue.seqid.num),
                    "insertion_code": _clean_text(residue.seqid.icode),
                    "residue_name": residue.name.strip().upper(),
                    "x": float(ca_atom.pos.x),
                    "y": float(ca_atom.pos.y),
                    "z": float(ca_atom.pos.z),
                }
            )

    nodes = pd.DataFrame.from_records(records)
    if nodes.empty:
        raise ValueError("Nenhum resíduo aminoacídico com átomo Cα foi encontrado.")

    nodes[["x", "y", "z"]] = nodes[["x", "y", "z"]].astype(np.float32)
    return nodes
