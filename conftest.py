import pytest

def pytest_addoption(parser):
    """Add `--runslow` option to py.test."""
    parser.addoption("--runslow", action="store_true",
        help="run slow tests")

def pytest_runtest_setup(item):
    """pytest items marked `slow` should not run by default."""
    if 'slow' in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")