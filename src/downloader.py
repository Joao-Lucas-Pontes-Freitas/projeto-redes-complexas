import gzip
from pathlib import Path

import requests

RCSB_DOWNLOAD_BASE = "https://files.rcsb.org/download"


def download_mmcif(pdb_id: str, destination_dir: Path) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{pdb_id.upper()}.cif.gz"

    if destination.exists() and destination.stat().st_size > 0:
        print(f"{pdb_id}: arquivo estrutural já existe; download ignorado.")
        return destination

    url = f"{RCSB_DOWNLOAD_BASE}/{pdb_id.upper()}.cif.gz"
    temporary = destination.with_suffix(destination.suffix + ".part")

    try:
        with requests.get(url, stream=True, timeout=(15, 180)) as response:
            response.raise_for_status()
            with temporary.open("wb") as output:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        output.write(chunk)

        if not temporary.exists() or temporary.stat().st_size == 0:
            raise RuntimeError("O download resultou em arquivo vazio.")

        with gzip.open(temporary, "rb") as compressed:
            if not compressed.read(32):
                raise RuntimeError("O arquivo baixado não contém dados.")

        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    print(f"{pdb_id}: arquivo estrutural baixado.")
    return destination
