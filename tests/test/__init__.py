"""Root class for testing iv package."""
import os
from unittest import TestCase


class TestIV(TestCase):
    """Base class for InspectionViewer tests."""

    @staticmethod
    def fixture(*path):
        """Return full path for file in 'fixtures' dir."""
        return os.path.join('fixtures', *path)

    @staticmethod
    def build(*path):
        """Return full path for file in 'build' dir."""
        if not path:
            return 'build'
        return os.path.join('build', *path)
