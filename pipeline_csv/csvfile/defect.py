"""Row with type Defect."""


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

    @property
    def at_weld_seam(self):
        """Return True if defect located at weld/seam."""
        return self.is_at_weld or self.is_at_seam

    @property
    def no_mp(self):
        """Return True if defect does not have maximum depth point."""
        return not self.row.mpoint_dist

    @property
    def mp_left_weld(self):
        """Return distance (mm) from maximum depth point to upstream weld."""
        if self.at_weld_seam or self.no_mp:
            return None

        return self.row.mpoint_dist - self.pipe.dist

    @property
    def mp_right_weld(self):
        """Return distance (mm) from maximum depth point to downstream weld."""
        if self.at_weld_seam or self.no_mp:
            return None

        return self.pipe.dist + self.pipe.length - self.row.mpoint_dist
