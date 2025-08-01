from click.testing import CliRunner

from structlint.cli import (
    structlint_cli,
)


def test_structlint_cli(capsys):
    runner = CliRunner()
    result = runner.invoke(structlint_cli)
    assert result.exit_code == 0
    assert "No problems detected." in result.output


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


def test_show_config():
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["show-config"])
    assert "[tool.structlint]" in result.output


def test_show_default_config():
    runner = CliRunner()
    result = runner.invoke(structlint_cli, ["show-default-config"])
    assert "[tool.structlint]" in result.output
