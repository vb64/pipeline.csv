"""Material of the pipe."""


class PipeMaterial:
    """Pipe material."""

    def __init__(self, name, smys):
        """Create new material."""
        self.name = name
        self.smys = smys  # yield stress
        self.smts = None  # tensile strength
        self.toughness = None  # ductility

    def __str__(self):
        """Return as text."""
        return "{} smys {} smts {}".format(
          self.name,
          round(self.smys, 2) if self.smys else '',
          round(self.smts, 2) if self.smts else ''
        )
