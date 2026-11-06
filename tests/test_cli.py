from pathlib import Path

from fii_surrogate.cli import run_from_config


def test_example_config_runs_end_to_end(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])
    config = Path("config/example_config.yml").read_text(encoding="utf-8")
    config = config.replace(
        "outputs/synthetic_example", str(tmp_path.as_posix())
    ).replace("enabled: true", "enabled: false")
    config_path = tmp_path / "config.yml"
    config_path.write_text(config, encoding="utf-8")
    outputs = run_from_config(config_path)
    assert outputs["validation"].is_file()
    assert (outputs["main"] / "model_results.csv").is_file()
    assert (outputs["main"] / "surface_predictions.csv").is_file()
