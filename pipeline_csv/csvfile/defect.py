"""Row with type Defect."""
from pipeline_csv.orientation import Orientation


class Defect:
    """Defect at the pipe."""

    def __init__(self, row, pipe):
        """Create defect at the pipe from csv Row."""
        self.row = row
        self.pipe = pipe

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

    def minutes2mm(self, minutes):
        """Translate angle minutes to mm."""
        return minutes

    @property
    @_with_mp
    def mp_seam(self):
        """Return distance (angle minutes) from maximum depth point to nearest seam."""
        if not self.pipe.seams:
            return None

        mpoint = Orientation.from_csv(self.row.mpoint_orient)
        dist = mpoint.dist_to(self.pipe.seams[0])

        if len(self.pipe.seams) == 1:
            return self.minutes2mm(dist)

        return self.minutes2mm(min(dist, mpoint.dist_to(self.pipe.seams[1])))
