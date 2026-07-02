# Redes complexas aplicadas à estrutura de proteínas

Projeto da disciplina de Redes Complexas para representar estruturas proteicas como grafos de contato, calcular medidas topológicas e detectar comunidades estruturais.

- **Proteína de teste:** 1PKN.
- **Proteína-alvo:** 6B1T.
- **Vértice:** resíduo de aminoácido representado pelo átomo Cα.
- **Aresta:** distância Cα–Cα menor ou igual a 8 Å.
- **Grafo:** simples, não direcionado e não ponderado.
- **Centralidades:** grau e autovetor.
- **Comunidades:** Louvain.

## Requisitos

- Python 3.10 ou superior;
- conexão com a internet no primeiro uso de cada estrutura;

## Instalação

### Clone do projeto
```bash
git clone https://github.com/Joao-Lucas-Pontes-Freitas/projeto-redes-complexas.git
cd projeto-redes-complexas
```

### Windows — PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Caso `py` não esteja disponível:

```powershell
python -m venv .venv
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Execução

### Proteína de teste — 1PKN

```powershell
python main.py --config config\test.json
```

Em Linux ou macOS:

```bash
python main.py --config config/test.json
```

Resultado de referência:

```text
Vértices: 514
Arestas: 2.627
Grau médio: 10,22
Comunidades: 5
Modularidade: 0,8139
```

### Proteína-alvo — 6B1T

```powershell
python main.py --config config\target.json
```

Em Linux ou macOS:

```bash
python main.py --config config/target.json
```

Resultado de referência:

```text
Vértices: 12.544
Arestas: 66.809
Grau médio: 10,65
Comunidades: 13
Modularidade: 0,9333
Pureza ponderada: 0,9249
```

Quando o arquivo `data/raw/<PDB>.cif.gz` já existe, o download é ignorado. As demais análises são executadas novamente e os resultados correspondentes são substituídos.

## Configurações

`config/test.json`:

```json
{
  "pdb_id": "1PKN",
  "cutoff_angstrom": 8.0,
  "louvain_resolution": 0.5,
  "louvain_seed": 42,
  "validate_entities": false
}
```

`config/target.json`:

```json
{
  "pdb_id": "6B1T",
  "cutoff_angstrom": 8.0,
  "louvain_resolution": 0.3,
  "louvain_seed": 42,
  "validate_entities": true
}
```

## Fluxo executado

```text
configuração
→ download ou reutilização do mmCIF
→ extração dos resíduos Cα
→ construção do grafo de contatos
→ distribuição de graus
→ centralidades de grau e autovetor
→ comunidades Louvain
→ validação por entidades, quando ativada
→ tabelas e figuras
```

## Saídas

```text
data/
├── raw/
│   └── <PDB>.cif.gz
├── processed/
│   ├── <PDB>_nodes.csv
│   └── <PDB>_edges.csv
└── results/
    ├── <PDB>_graph_summary.json
    ├── <PDB>_centralities.csv
    ├── <PDB>_centrality_summary.json
    ├── <PDB>_louvain_membership.csv
    ├── <PDB>_louvain_summary.json
    └── arquivos de validação biológica da 6B1T

figures/
├── <PDB>_degree_distribution.png
├── <PDB>_degree_centrality_3d.png
├── <PDB>_eigenvector_centrality_3d.png
└── <PDB>_louvain_communities_3d.png
```

Para a 6B1T também são produzidos:

```text
data/results/6B1T_entity_community_contingency.csv
data/results/6B1T_entity_metrics.csv
data/results/6B1T_community_purity.csv
data/results/6B1T_biological_validation.json
```

## Estrutura do projeto

```text
.
├── config/
│   ├── test.json
│   └── target.json
├── src/
│   ├── analysis.py
│   ├── biological_validation.py
│   ├── centrality.py
│   ├── community.py
│   ├── config.py
│   ├── downloader.py
│   ├── graph_builder.py
│   ├── io_utils.py
│   ├── parser.py
│   ├── pipeline.py
│   └── visualization.py
├── data/
├── figures/
├── main.py
├── requirements.txt
└── RELATORIO.pdf
```

## Relatório

A modelagem, as justificativas, os resultados, a validação biológica, as limitações e as referências estão em `RELATORIO.pdf`.
