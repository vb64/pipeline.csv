"""Material of the pipe."""


class PipeMaterial:
    """Pipe material."""

    def __init__(self, name, smys, smts=None, toughness=None, ksv=None, k1c=None):
        """Create new material."""
        self.name = name
        self.smys = smys  # yield stress, MPa
        self.smts = smts  # tensile strength, MPa
        self.toughness = toughness  # ductility, %%
        self.ksv = ksv  # impact strength, Dj/sm2
        self.k1c = k1c  # fracture toughness, MPa * m1/2

    def __str__(self):
        """Return as text."""
        return "{} smys {} smts {}".format(
          self.name,
          round(self.smys, 2) if self.smys else '',
          round(self.smts, 2) if self.smts else ''
        )
