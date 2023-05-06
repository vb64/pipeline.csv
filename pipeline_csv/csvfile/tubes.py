"""Tubes iterator interface for csv file."""
from .. import Error, TypeHorWeld


def summary_text(objects, names):
    """Return summary text for given items."""
    items = {}
    for item in objects:
        code = int(item.object_code)
        if code in items:
            items[code] += 1
        else:
            items[code] = 1

    return ', '.join(["{}: {}".format(names[key], items[key]) for key in sorted(items.keys())])


class Tube:
    """Represent one pipe."""

    def __init__(self, row, stream, auto_number):
        """Construct new tube object from csv row with given data stream state."""
        self.row = row
        self.dist = int(row.dist_od)
        self.auto_number = auto_number
        self.stream = stream

        self.length = None
        self.thick = None
        self.category = None

        self.is_thick_change = False
        self.is_category_change = False

        self.seams = []
        self.lineobjects = []
        self.defects = []
        self.categories = []
        self.thicks = []

    def __str__(self):
        """Return as text."""
        return "Tube len {} wall {}".format(
          self.length,
          self.thick
        )

    def finalize(self, dist):
        """Finalize tube data at given dist."""
        self.length = int(dist) - self.dist
        self.thick = self.stream.thick
        self.category = self.stream.category

    def add_object(self, row):
        """Add data to tube from csv row."""
        if row.is_defect:
            self.defects.append(row)

        elif row.is_lineobj:
            self.lineobjects.append(row)

        elif row.is_seam:
            self.seams.append(row)

        elif row.is_category:
            category = row.depth_max
            if self.stream.category != category:
                self.stream.category = category
                self.is_category_change = True
            self.categories.append(row)

        elif row.is_thick:
            thick = int(row.depth_max)
            if self.stream.thick != thick:
                self.stream.thick = thick
                self.is_thick_change = True
            self.thicks.append(row)

        else:
            raise Error("Tube at dist {} has wrong row: {}".format(self.dist, str(row)))

    def set_geo(self, latitude, longtitude, altitude):
        """Set geo coords for tube."""
        self.row.set_geo(latitude, longtitude, altitude)

    @property
    def latitude(self):
        """Tube start latitude."""
        return self.row.latitude

    @property
    def longtitude(self):
        """Tube start longtitude."""
        return self.row.longtitude

    @property
    def altitude(self):
        """Tube start altitude."""
        return self.row.altitude

    @property
    def radius(self):
        """Return tube curve radius."""
        return self.row.depth_min

    def set_radius(self, val):
        """Set tube curve radius."""
        self.row.depth_min = val

    @property
    def min_diam(self):
        """Return optional minimal pipe diameter as string (mm)."""
        return self.row.depth_max

    @min_diam.setter
    def min_diam(self, value):
        """Set optional minimal pipe diameter as string (mm)."""
        self.row.depth_max = value

    @property
    def number(self):
        """Tube custom or auto number."""
        num = self.row.object_name.strip()
        if not num:
            num = self.auto_number
        return num

    @property
    def summary(self):
        """Return string with summary for given tube."""
        defect_names = {}
        if self.defects:
            defect_names = self.defects[0].__class__.defekts_dict()

        line_names = {}
        if self.lineobjects:
            line_names = self.lineobjects[0].__class__.lineobj_dict()

        return ', '.join([i for i in [
          summary_text(self.defects, defect_names),
          summary_text(self.lineobjects, line_names)
        ] if i])

    @property
    def typ(self):
        """Pipe type according pipe seams data."""
        if not self.seams:
            return TypeHorWeld.UNKNOWN

        return int(self.seams[0].object_code)

    @property
    def seam_info(self):
        """Return text string with seams orientation."""
        text = ''
        if self.typ == TypeHorWeld.HORIZONTAL:
            text = self.seams[0].orient_td
        elif self.typ == TypeHorWeld.SECOND:
            text = self.seams[0].orient_td + ' / ' + self.seams[0].orient_bd
        elif self.typ == TypeHorWeld.SPIRAL:
            text = ' / '.join([i.orient_td for i in self.seams])

        return text

    def features(self):
        """Return defects and lineobjects of the pipe, arranged by distance."""
        return sorted(self.lineobjects + self.defects, key=lambda i: i.dist)
