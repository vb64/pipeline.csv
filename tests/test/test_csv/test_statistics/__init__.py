"""Root class for testing iv package."""
from .. import TestCsv


class TestStatistics(TestCsv):
    """Base class for InspectionViewer csv statistics tests."""

    def setUp(self):
        """Init tube tests."""
        super().setUp()
        from pipeline_csv.oegiv import File

        self.csv_file = File.from_file(self.fixture('DefTable.csv'), 1400)
