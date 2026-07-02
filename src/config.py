import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    pdb_id: str
    cutoff_angstrom: float
    louvain_resolution: float
    louvain_seed: int
    validate_entities: bool
    project_root: Path

    @property
    def raw_dir(self) -> Path:
        return self.project_root / "data" / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.project_root / "data" / "processed"

    @property
    def results_dir(self) -> Path:
        return self.project_root / "data" / "results"

    @property
    def figures_dir(self) -> Path:
        return self.project_root / "figures"


def load_config(path: str | Path) -> PipelineConfig:
    config_path = Path(path).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Configuração não encontrada: {config_path}")

    data = json.loads(config_path.read_text(encoding="utf-8"))

    pdb_id = str(data["pdb_id"]).strip().upper()
    if len(pdb_id) != 4 or not pdb_id.isalnum():
        raise ValueError(f"PDB ID inválido: {pdb_id!r}")

    cutoff = float(data.get("cutoff_angstrom", 8.0))
    if cutoff <= 0:
        raise ValueError("cutoff_angstrom deve ser positivo.")

    resolution = float(data.get("louvain_resolution", 1.0))
    if resolution <= 0:
        raise ValueError("louvain_resolution deve ser positiva.")

    return PipelineConfig(
        pdb_id=pdb_id,
        cutoff_angstrom=cutoff,
        louvain_resolution=resolution,
        louvain_seed=int(data.get("louvain_seed", 42)),
        validate_entities=bool(data.get("validate_entities", False)),
        project_root=Path(__file__).resolve().parents[1],
    )
