"""Row with type Defect."""
from pipeline_csv import TypeHorWeld
from pipeline_csv.orientation import Orientation


class Defect:
    """Defect at the pipe."""

    def __init__(self, row, pipe):
        """Create defect at the pipe from csv Row."""
        self.row = row
        self.pipe = pipe

        self.orient1 = None
        if self.row.orient_td:
            self.orient1 = Orientation.from_csv(self.row.orient_td)

        self.orient2 = None
        if self.row.orient_bd:
            self.orient2 = Orientation.from_csv(self.row.orient_bd)

    def __str__(self):
        """As text."""
        return '{} at {}'.format(self.row.object_code_t, self.pipe)

    @property
    def code(self):
        """Return object code as integer."""
        return int(self.row.object_code)

    @property
    def is_metal_loss(self):
        """Return True if metal loss defect."""
        return self.code in self.row.mloss_dict()

    @property
    def is_dent(self):
        """Return True if dent defect."""
        return self.code in self.row.dents_dict()

    @property
    def is_at_weld(self):
        """Return True if weld placed defect."""
        return self.code in self.row.atweld_dict()

    @property
    def is_at_seam(self):
        """Return True if seam placed defect."""
        return self.code in self.row.atseam_dict()

    def _with_mp(prop):  # pylint: disable=no-self-argument
        """Return decorator for property.

        https://stackoverflow.com/questions/1263451/python-decorators-in-classes
        """
        def wrapper(self):
            """Return None if defect does not have maximum depth point, or defect is located on a seam/weld."""
            if self.is_at_weld or self.is_at_seam or (not self.row.mpoint_dist):
                return None
            return prop(self)  # pylint: disable=not-callable

        return wrapper

    @property
    @_with_mp
    def mp_left_weld(self):
        """Return distance (mm) from maximum depth point to upstream weld."""
        return self.row.mpoint_dist - self.pipe.dist

    @property
    @_with_mp
    def mp_right_weld(self):
        """Return distance (mm) from maximum depth point to downstream weld."""
        return self.pipe.dist + self.pipe.length - self.row.mpoint_dist

    @property
    @_with_mp
    def mp_seam(self):
        """Return distance (angle minutes) from maximum depth point to nearest seam."""
        if not self.pipe.seams:
            return None
        if self.pipe.seams[0].object_code == TypeHorWeld.SPIRAL:
            return None

        mpoint = Orientation.from_csv(self.row.mpoint_orient)
        dist = mpoint.dist_to(self.pipe.seam1)
        if self.pipe.seam2:
            dist = min(dist, mpoint.dist_to(self.pipe.seam2))

        return self.pipe.minutes2mm(dist)

    @property
    @_with_mp
    def mp_seam_weld(self):
        """Return distance (mm) from maximum depth point to nearest seam/weld.

        If the defect does not have maximum depth point, return None.
        """
        values = [i for i in [self.mp_seam, self.mp_left_weld, self.mp_right_weld] if i is not None]
        return min(values)

    @property
    def to_left_weld(self):
        """Return distance (mm) from left defect border to upstream weld."""
        return self.row.dist - self.pipe.dist

    @property
    def to_right_weld(self):
        """Return distance (mm) from right defect border to downstream weld."""
        return self.pipe.dist + self.pipe.length - (self.row.dist + int(self.row.length))

    @property
    def to_seam(self):  # pylint: disable=too-complex
        """Return distance (mm) from defect borders to nearest seam or None if pipe does not have seams."""
        if (not self.pipe.seams) or (self.pipe.seams[0].object_code == TypeHorWeld.SPIRAL):
            return None

        if self.orient1 and self.orient2:
            if self.pipe.seam1.is_inside(self.orient1, self.orient2):
                return 0
            if self.pipe.seam2:
                if self.pipe.seam2.is_inside(self.orient1, self.orient2):
                    return 0

        up_seam1 = None
        up_seam2 = None
        if self.orient1:
            up_seam1 = self.orient1.dist_to(self.pipe.seam1)
            if self.pipe.seam2:
                up_seam2 = self.orient1.dist_to(self.pipe.seam2)

        dn_seam1 = None
        dn_seam2 = None
        if self.orient2:
            dn_seam1 = self.orient2.dist_to(self.pipe.seam1)
            if self.pipe.seam2:
                dn_seam2 = self.orient2.dist_to(self.pipe.seam2)

        dists = [i for i in [up_seam1, up_seam2, dn_seam1, dn_seam2] if i is not None]
        if not dists:
            return None

        return min(dists)
