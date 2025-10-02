"""Tests __init__.py file.

make test T=test_csv/test_statistics/test_init.py
"""
from . import TestStatistics


class TestInit(TestStatistics):
    """File __init__.py."""

    @staticmethod
    def test_counter():
        """Check Counter class."""
        from pipeline_csv.csvfile.statistics import Counter

        count = Counter()
        assert count.number == 1
        count.increment()
        assert count.number == 2
        assert ": 2" in str(count)

    def test_property_counter(self):
        """Check PropertyCounter class."""
        from pipeline_csv.csvfile.statistics import PropertyCounter

        count = PropertyCounter()
        assert count.number == 0
        assert ": 0" in str(count)
        assert count.tubes_all() == 0

        count.add_item(0, self.tube)
        assert count.tubes_all() == 1
        count.add_item(0, self.tube)
        assert count.tubes_all() == 1
        assert count.tubes_with(0) == 1
