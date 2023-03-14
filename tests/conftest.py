"""Pytest session setup."""
import sys
import os
import pytest


def path_setup():
    """Setup sys path."""
    test_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, os.path.join(test_dir, 'pipeline_csv'))


@pytest.fixture(scope="session", autouse=True)
def session_setup(request):
    """Auto session resource fixture."""
    build_path = 'build'
    if not os.path.exists(build_path):
        os.mkdir(build_path)

    path_setup()
