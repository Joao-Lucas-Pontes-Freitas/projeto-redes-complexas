import argparse

from src.config import load_config
from src.pipeline import run_pipeline


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analisa uma estrutura proteica como rede de contatos Cα."
    )
    parser.add_argument(
        "--config",
        default="config/test.json",
        help="Arquivo JSON de configuração.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    run_pipeline(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
