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
        """Check function add180."""
        from pipeline_csv.orientation import Orientation, add180

        assert str(add180(Orientation(3, 0))) == '9,00'
        assert str(add180(Orientation(9, 0))) == '3,00'
        assert str(add180(Orientation(9, 30))) == '3,30'

    @staticmethod
    def test_from_csv():
        """Check method from_csv."""
        from pipeline_csv.orientation import Orientation

        assert Orientation.from_csv('1,10').as_minutes == 70
        assert Orientation.from_csv('') is None

    @staticmethod
    def test_from_minutes():
        """Check method from_minutes."""
        from pipeline_csv.orientation import Orientation

        ornt = Orientation.from_minutes(700)
        assert ornt.hours == 11
        assert ornt.minutes == 40

    @staticmethod
    def test_dist_to():
        """Check method dist_to."""
        from pipeline_csv.orientation import Orientation

        ornt = Orientation.from_minutes(60)
        assert ornt.dist_to(Orientation.from_minutes(0)) == 60
        assert ornt.dist_to(Orientation.from_minutes(120)) == 60
        assert ornt.dist_to(Orientation.from_minutes(420)) == 360
        assert ornt.dist_to(Orientation.from_minutes(700)) == 80
        assert ornt.dist_to(Orientation.from_minutes(600)) == 180

    @staticmethod
    def test_dist_to_int():
        """Check method dist_to_int."""
        from pipeline_csv.orientation import Orientation

        ornt = Orientation.from_minutes(60)
        assert ornt.dist_to_int(Orientation.from_minutes(50)) == (710, 10)
        assert ornt.dist_to_int(Orientation.from_minutes(70)) == (10, 710)
        assert ornt.dist_to_int(Orientation.from_minutes(60)) == (0, 0)

    @staticmethod
    def _test_is_inside():
        """Check method is_inside."""
        from pipeline_csv.orientation import Orientation

        ornt = Orientation.from_minutes(60)

        assert ornt.is_inside(Orientation.from_minutes(10), Orientation.from_minutes(60))
        assert ornt.is_inside(Orientation.from_minutes(60), Orientation.from_minutes(180))
        assert ornt.is_inside(Orientation.from_minutes(10), Orientation.from_minutes(180))
        assert not ornt.is_inside(Orientation.from_minutes(180), Orientation.from_minutes(10))

        assert ornt.is_inside(Orientation.from_minutes(700), Orientation.from_minutes(180))
        assert ornt.is_inside(Orientation.from_minutes(700), Orientation.from_minutes(60))
        assert not ornt.is_inside(Orientation.from_minutes(180), Orientation.from_minutes(700))
