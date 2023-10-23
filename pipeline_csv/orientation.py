"""Orientation object."""
import math


class Error(Exception):
    """Orientation exception."""


class Orientation:
    """Orientation units conversions."""

    def __init__(self, hours, minutes):
        """Construct object from integer hours and minutes."""
        if not (0 <= hours <= 12):
            raise Error("Wrong hours: {}. Must be 0-12".format(hours))

        if not (0 <= minutes <= 59):
            raise Error("Wrong minutes: {}. Must be 0-59".format(minutes))

        self.hours = hours
        self.minutes = minutes

    def __str__(self):
        """Return orientation string in csv format."""
        hours = int(self.hours)
        if hours == 0:
            hours = '12'

        minutes = self.minutes
        if minutes < 10:
            minutes = '0{}'.format(minutes)

        return "{},{}".format(hours, minutes)

    @property
    def as_minutes(self):
        """Return orientation as integer minutes."""
        return (self.hours * 60 + self.minutes) % 720

    @classmethod
    def from_hour_float(cls, hour_float):
        """Construct object from hours as float."""
        parttial_hour, hours = math.modf(hour_float)
        minutes = parttial_hour * 60
        return cls(int(hours), int(minutes))

    @classmethod
    def from_minutes(cls, minutes):
        """Construct object from integer minutes."""
        return cls(int(minutes / 60), minutes % 60)

    @classmethod
    def from_degree(cls, degree):
        """Construct object from float degree."""
        return cls.from_minutes(int(degree * 2))

    @classmethod
    def from_csv(cls, text):
        """Construct object from from text 'hours,minites'."""
        if ',' not in text:
            return None

        hours, minutes = text.split(',')
        return cls(int(hours), int(minutes))

    def dist_to_int(self, ornt):
        """Return two distances (clockwise and counterclock-wise) in angle minutes to given orientation object."""
        clockwise = int(ornt.as_minutes - self.as_minutes)
        if clockwise < 0:
            clockwise = 720 + clockwise

        return (clockwise, (720 - clockwise) % 720)

    def dist_to(self, ornt):
        """Return distance in angle minutes to given orientation object."""
        clockwise, counterclock_wise = self.dist_to_int(ornt)
        return min([clockwise, counterclock_wise])

    def is_inside(self, ornt1, ornt2):
        """Return True if orientation located inside given arc."""
        arc, _ = ornt1.dist_to_int(ornt2)
        dst, _ = self.dist_to_int(ornt2)
        return dst <= arc

    def add_minutes(self, minutes):
        """Increases the orientation angle by a specified number of minutes. Returns the new minutes value."""
        ornt = self.from_minutes((self.as_minutes + minutes) % 720)
        self.hours = ornt.hours
        self.minutes = ornt.minutes
        return self.as_minutes


def from_infotech_html(text):
    """Return orientation from infotech string."""
    return Orientation.from_hour_float(float(text.replace(',', '.')))


def add180(ornt):
    """Return the orientation 180 degrees away from the given one."""
    new_ornt = Orientation.from_minutes(ornt.as_minutes)
    new_ornt.add_minutes(180 * 2)  # degree to minutes
    return new_ornt
