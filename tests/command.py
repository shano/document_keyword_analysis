import pytest
from flask_script import Command

class PytestCommand(Command):
    """Runs tests"""
    capture_all_args = True

    def __call__(self, app=None, *args):
        pytest.main(*args)