"""Tests defects.py file.

make test T=test_csv/test_statistics/test_defects.py
"""
import pytest
from . import TestStatistics


class TestDefects(TestStatistics):
    """File defects.py."""

    def test_grade_tube(self):
        """Test GradeTube class."""
        from pipeline_csv.csvfile.statistics.defects import GradeTube
        assert 'total_num: 0' in str(GradeTube())

    def test_gradebase(self):
        """Test GradeBase class."""
        from pipeline_csv.csvfile.statistics.defects import GradeBase

        with pytest.raises(NotImplementedError) as err:
            GradeBase()
        assert 'grade_init' in str(err.value)

        class Grade(GradeBase):
            """Stub for tests."""

            def grade_init(self):
                """Stub for init."""

        grade = Grade()
        assert grade.extended_number(None) == 0

        with pytest.raises(NotImplementedError) as err:
            grade.get_grade(None, None)
        assert 'get_grade' in str(err.value)

        with pytest.raises(NotImplementedError) as err:
            grade.add_item(None, None, None)
        assert 'add_item' in str(err.value)

    @staticmethod
    def test_at_hours():
        """Check at_hours function."""
        from pipeline_csv.csvfile.statistics.defects import at_hours

        assert at_hours(702, 10) == [0]

        assert not at_hours(-1, -1)
        assert at_hours(120, -1) == [2]
        assert at_hours(120, 720) == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
        assert at_hours(700, 120) == [0, 1, 2]
        assert at_hours(500, 120) == [8, 9, 10, 11, 0, 1, 2]
