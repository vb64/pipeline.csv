"""Root class for testing iv package."""
import os
from unittest import TestCase


class TestIV(TestCase):
    """Base class for InspectionViewer tests."""

    def setUp(self):
        """Make pipe for tests."""
        super().setUp()
        from pipeline_csv.csvfile import Stream
        from pipeline_csv.csvfile.tubes import Tube
        from pipeline_csv.csvfile.row import Row

        stream = Stream(diameter=700)
        self.pipe = Tube(Row.as_weld(10), stream, '1')

    def make_defect(self, dist, length, orient1, orient2, mp_orient, mp_dist):
        """Make new defect."""
        from pipeline_csv import DefektSide
        from pipeline_csv.oegiv import TypeDefekt, Row
        from pipeline_csv.csvfile.defect import Defect

        defect = Defect(
          Row.as_defekt(
            dist, TypeDefekt.CORROZ, DefektSide.INSIDE, str(length), '10', '15',
            orient1, orient2,
            mp_orient, mp_dist, ''
          ),
          self.pipe
        )
        self.pipe.defects.append(defect)

        return defect

    @staticmethod
    def fixture(*path):
        """Return full path for file in 'fixtures' dir."""
        return os.path.join('fixtures', *path)

    @staticmethod
    def build(*path):
        """Return full path for file in 'build' dir."""
        if not path:
            return 'build'
        return os.path.join('build', *path)
