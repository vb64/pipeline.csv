"""Root class for testing iv package."""
import os
from unittest import TestCase


class TestIV(TestCase):
    """Base class for InspectionViewer tests."""

    fixtures_path = os.path.join(
      os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
      'fixtures'
    )

    def fixture(self, file_name):
        """Full file name for fixture."""
        return os.path.join(self.fixtures_path, file_name)
