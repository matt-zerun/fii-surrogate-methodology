"""Checks public GitHub metadata and code-only publication boundary."""
from pathlib import Path
import tomllib

import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_software_identity_and_citation():
    citation = yaml.safe_load((ROOT / 'CITATION.cff').read_text(encoding='utf-8'))
    assert citation['version'] == '2.0.0'
    assert citation['license'] == 'MIT'
    assert citation['repository-code'] == 'https://github.com/matt-zerun/fii-surrogate-methodology'
    assert citation['identifiers'][0]['value'] == '10.5281/zenodo.21414810'
    project = tomllib.loads((ROOT / 'pyproject.toml').read_text(encoding='utf-8'))['project']
    assert project['version'] == '2.0.0'
    assert project['urls']['Archive'] == 'https://doi.org/10.5281/zenodo.21414810'
    assert project['urls']['Related publication'] == 'https://doi.org/10.1038/s41598-026-65202-3'


def test_code_only_scope():
    assert not (ROOT / 'reference_outputs').exists()
    assert not (ROOT / '.zenodo.json').exists()
    assert not (ROOT / 'MANIFEST.sha256').exists()
    assert not (ROOT / 'scripts/make_manuscript_repeated_partition_figures.py').exists()
    assert not (ROOT / 'scripts/make_figure_10_manuscript.py').exists()
    assert (ROOT / 'src/fii_surrogate/plots.py').is_file()
    assert (ROOT / 'CODE_ONLY_SCOPE.md').is_file()
    assert (ROOT / 'data/synthetic_example/fii_synthetic_example.csv').is_file()
