"""Module orientation.py.

make test T=test_orientation.py
"""
from . import TestIV


class TestOrientation(TestIV):
    """Check orientation.py file."""

    def test_init(self):
        """Check init and errors."""
        from oeg_iv.orientation import Orientation, Error

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

    @staticmethod
    def test_from_infotech_html():
        """Check from_infotech_html."""
        from oeg_iv.orientation import from_infotech_html

        orient = from_infotech_html("5,5")
        assert orient.hours == 5
        assert orient.minutes == 30
