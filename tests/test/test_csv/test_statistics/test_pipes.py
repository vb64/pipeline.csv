"""Tests pipes.py file.

make test T=test_csv/test_statistics/test_pipes.py
"""
from . import TestStatistics


class TestPipes(TestStatistics):
    """File pipes.py."""

    def test_counter_length(self):
        """Check CounterLength class."""
        from pipeline_csv.csvfile.statistics.pipes import CounterLength

        counter = CounterLength(100)
        assert "len: 100" in str(counter)
