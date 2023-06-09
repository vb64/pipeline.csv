"""Module orientation.py.

make test T=test_orientation.py
"""
from . import TestIV


class TestOrientation(TestIV):
    """Check orientation.py file."""

    def test_init(self):
        """Check init and errors."""
        from pipeline_csv.orientation import Orientation, Error

        with self.assertRaises(Error) as context:
            Orientation(99, 0)
        assert 'Wrong hours: 99' in str(context.exception)

        with self.assertRaises(Error) as context:
            Orientation(5, 99)
        assert 'Wrong minutes: 99' in str(context.exception)

        assert str(Orientation(5, 15)) == "5,15"
        assert str(Orientation(0, 5)) == "12,05"
        assert str(Orientation.from_hour_float(1.5)) == "1,30"

        assert str(Orientation.from_minutes(60)) == "1,00"
        assert str(Orientation.from_minutes(90)) == "1,30"

        assert str(Orientation.from_degree(30)) == "1,00"
        assert str(Orientation.from_degree(45)) == "1,30"

    @staticmethod
    def test_from_infotech_html():
        """Check from_infotech_html."""
        from pipeline_csv.orientation import from_infotech_html

        orient = from_infotech_html("5,5")
        assert orient.hours == 5
        assert orient.minutes == 30

    @staticmethod
    def test_add180():
        """Function add180."""
        from pipeline_csv.orientation import Orientation, add180

        assert str(add180(Orientation(3, 0))) == '9,00'
        assert str(add180(Orientation(9, 0))) == '3,00'
        assert str(add180(Orientation(9, 30))) == '3,30'

    @staticmethod
    def test_from_csv():
        """Method from_csv."""
        from pipeline_csv.orientation import Orientation

        assert Orientation.from_csv('1,10').as_minutes == 70
        assert Orientation.from_csv('') is None
