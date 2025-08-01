import tomllib
from pathlib import Path

from click.testing import CliRunner

from structlint.cli import (
    structlint_cli,
)


def get_version() -> str:
    return tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"]


def test_structlint_cli(capsys):
    runner = CliRunner()
    result = runner.invoke(structlint_cli)
    assert result.exit_code == 0
    assert "No problems detected." in result.output


def test_version(capsys):
    expected_version = get_version()
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["version"])
    assert result.exit_code == 0
    assert expected_version in result.output

    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["--version"])
    assert result.exit_code == 0
    assert expected_version in result.output


def test_run_all(capsys):
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["all"])
    assert result.exit_code == 0
    assert "No problems detected." in result.output


def test_docs(capsys):
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["docs"])
    assert result.exit_code == 0
    assert "No problems detected." in result.output


def test_imports(capsys):
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["imports"])
    assert result.exit_code == 0
    assert "No problems detected." in result.output


def test_methods(capsys):
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["methods"])
    assert result.exit_code == 0
    assert "No problems detected." in result.output


def test_tsts(capsys):
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["tests"])
    assert result.exit_code == 0
    assert "No problems detected." in result.output


def test_show_config() -> None:
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["show-config"])
    assert "[tool.structlint]" in result.output


def test_show_default_config() -> None:
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["show-default-config"])
    assert "[tool.structlint]" in result.output
