"""Root class for testing iv package."""
from .. import TestIV


class TestCsv(TestIV):
    """Base class for InspectionViewer csv tests."""

    def setUp(self):
        """Init tube tests."""
        super().setUp()
        from pipeline_csv.csvfile import Stream
        from pipeline_csv.csvfile.row import Row
        from pipeline_csv.csvfile.tubes import Tube

        stream = Stream(diameter=700)
        self.tube = Tube(Row.as_weld(10), stream, '1')
