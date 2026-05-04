"""ASME B31G method for metal loss defects.

Another libs:

https://pypi.org/project/pyintegrity/
https://github.com/novanumeric/WebIntegrity
"""
import os

from .. import Context as ContextBase
from ...i18n import load_po

EXPL_ROUND = 3


class Context(ContextBase):
    """Context of the ASME B31G method."""

    # ANSI/NACE SP0502-2010 (formerly RP0502) Appendix C: Postassessment: Corrosion Rate Estimation C3.2
    # https://github.com/vb64/pipeline.integrity/blob/main/docs/SOP_Pipeline_External_Corrosion.pdf
    corrosion_rate = 0.4  # mm/year
    design_factor = 1.0

    def __init__(self, defect, material, maop):
        """ASME B31G context."""
        super().__init__(defect, material, maop)
        self.safe_pressure = None

    def lang(self, lang_code):
        """Load language dict for localize explain text."""
        name = os.path.join(os.path.dirname(__file__), 'locale', lang_code, 'LC_MESSAGES', 'messages.po')
        return load_po(name)

    @property
    def relative_depth(self):
        """Return defect depth as percent from pipe wall thickness."""
        return self.anomaly.depth_percent
