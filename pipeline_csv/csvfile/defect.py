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
