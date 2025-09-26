"""Tests totals.py file.

make test T=test_csv/test_statistics/test_totals.py
"""
from . import TestStatistics


class TestTotals(TestStatistics):
    """File totals.py."""

    def test_property_counter(self):
        """Check Totals class."""
        from pipeline_csv.oegiv import File
        from pipeline_csv.csvfile.statistics.totals import Totals

        totals = Totals()
        assert not totals.markers
        assert "Tubes:" in str(totals)

        self.tube.length = 100
        totals.add_data(self.tube)

        csv_file = File.from_file(self.fixture('DefTable.csv'), 1400)
        warns = []
        totals.fill(csv_file, warns)
        assert not warns
