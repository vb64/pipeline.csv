"""Danger calculation methods."""


class Context:
    """Base class for Context of the danger method."""

    name = "not defined"

    def __init__(self, defect, material, maop, extended_data=None):
        """Create new context instance."""
        self.anomaly = defect
        self.material = material
        self.maop = maop
        self.extended_data = extended_data
        self.explain_text = []
        self.is_explain = False

    def __str__(self):
        """Return as text."""
        return "{}\nPipe {}\nDfct {}".format(
          self.name,
          str(self.anomaly.pipe),
          str(self.anomaly)
        )

    def lang(self, _lang_code):
        """Load language dict for localize explain text."""
        raise NotImplementedError("{}.lang".format(self.__class__.__name__))

    def explain(self):
        """Return text with explanation for calculation."""
        return ''.join(self.explain_text)

    def add_explain(self, msg_list):
        """Add messages from the list to explain array."""
        if self.is_explain:
            self.explain_text.extend(msg_list)
