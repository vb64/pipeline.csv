"""Tests totals.py file.

make test T=test_csv/test_statistics/test_totals.py
"""
from . import TestStatistics


def check_count_property(prop, val, num):
    """Check PropertyCounter with given val for num."""
    assert val in prop.data
    assert prop.data[val].number == num


def check_tube_property(prop, val, num, length):
    """Check TubeProperty with given val for num and length."""
    assert val in prop.data
    assert prop.data[val].number == num
    assert prop.data[val].length == length


class TestTotals(TestStatistics):
    """File totals.py."""

    def test_property_counter(self):
        """Check Totals class."""
        from pipeline_csv.csvfile.statistics.totals import Totals

        totals = Totals()
        totals.init_fill()
        assert not totals.markers
        assert "Tubes:" in str(totals)

        self.tube.length = 100
        totals.add_data(self.tube)

    def test_fill_base(self):
        """Check Totals.fill method."""
        from pipeline_csv.csvfile.statistics.totals import Totals
        from pipeline_csv import TypeHorWeld, DefektSide
        from pipeline_csv.oegiv import TypeDefekt

        totals = Totals()
        warns = []
        totals.fill(self.csv_file, warns)

        assert not warns
        assert totals.start == 0
        assert totals.length == 426625
        assert len(totals.markers) == 5

        assert totals.liners.number == 14
        assert len(totals.liners.tubes) == 3
        assert len(totals.liners.data) == 3
        assert totals.liners.tubes_all() == 13

        assert totals.pipes.number == 41
        assert totals.pipes.length == totals.length

        assert totals.pipes.thick.number == totals.pipes.number
        assert totals.pipes.thick.length == totals.length

        prop = totals.pipes.thick
        assert len(prop.data) == 3
        check_tube_property(prop, 70, 22, 232232)  # 7 mm thick: 22 pipes length 232232 mm
        check_tube_property(prop, 90, 6, 63324)
        check_tube_property(prop, 100, 13, 131069)

        prop = totals.pipes.category
        assert len(prop.data) == 3
        check_tube_property(prop, '1', 5, 51980)  # 1 category: 5 pipes length 51980 mm
        check_tube_property(prop, '2', 11, 118773)
        check_tube_property(prop, '3', 25, 255872)

        prop = totals.pipes.types
        assert len(prop.data) == 1
        check_tube_property(prop, TypeHorWeld.HORIZONTAL, totals.pipes.number, totals.length)

        assert totals.defects.number == 75
        assert 'total_num: 75' in str(totals.defects)

        prop = totals.defects.base_wallside
        assert len(prop.data) == 2
        check_count_property(prop, DefektSide.UNKNOWN, 6)
        check_count_property(prop, DefektSide.OUTSIDE, 69)

        prop = totals.defects.base_types
        assert len(prop.data) == 6
        check_count_property(prop, TypeDefekt.CORROZ, 56)
        check_count_property(prop, TypeDefekt.MECHANIC, 6)
        check_count_property(prop, TypeDefekt.DENT, 2)
        check_count_property(prop, TypeDefekt.GWAN, 1)
        check_count_property(prop, TypeDefekt.TECHNOLOGY, 8)
        check_count_property(prop, TypeDefekt.FACTORY, 2)

        assert totals.defects.base_angle_anomalies.hours == {
          0: 6, 1: 3, 2: 6, 3: 8, 4: 8, 5: 7, 6: 9, 7: 15, 8: 9, 9: 17, 10: 7, 11: 8
        }

    def test_fill_custom(self):
        """Check Totals.fill method with custom defect class."""
        from pipeline_csv.oegiv import File
        from pipeline_csv.csvfile.statistics.totals import Totals
        from pipeline_csv.csvfile.statistics.defects import (
          GRADE_OVER_MAX, Totals as DefectsTotalsBase,
          Depth, Dents, DangerValve, SingleDist, DistDanger, DistWallside, DistSingle
        )

        class DefectsTotals(DefectsTotalsBase):
            """Custom defect totals class."""

            def __init__(self, start, length, markers):
                """Make new defects total object with custom properties."""
                super().__init__(start, length, markers)
                self.depth = Depth(grades=[10])
                self.dents = Dents(grades=[5, 10])
                self.danger_valve = DangerValve(markers)
                self.distribution = SingleDist()
                self.distribution_bars = DistDanger(length)

                # 40 bars from start to ends with data divided by wallside
                self.dist_loss_wallside = DistWallside(start, length, 40)
                self.dist_dents = DistSingle(start, length, 40)

                # part of trace
                self.part_dist_loss_wallside = DistWallside(start + length / 4, length / 2, 40)

            def add_defect(self, defect, tube, warns):
                """Add defect to custom statistics."""
                super().add_defect(defect, tube, warns)

                self.danger_valve.add_data(defect)
                self.distribution.add_data(defect)
                self.distribution_bars.add_data(defect)

                if defect.is_metal_loss:
                    self.depth.add_data(defect)
                    self.dist_loss_wallside.add_data(defect)
                    self.part_dist_loss_wallside.add_data(defect)

                if defect.is_dent:
                    self.dents.add_data(defect)
                    self.dist_dents.add_data(defect)

        totals = Totals(defects_class=DefectsTotals)
        warns = []
        totals.fill(File.from_file(self.fixture('statistics.csv'), 1400), warns)

        assert totals.defects.depth.number == 56
        assert totals.defects.depth.max_percent == 12.0
        assert totals.defects.depth.pipes_with_grade(10) == 10
        assert totals.defects.depth.pipes_with_grade(GRADE_OVER_MAX) == 5

        assert totals.defects.dents.number == 2
        assert totals.defects.dents.data[5] == 1
        assert totals.defects.dents.data[10] == 1
        assert totals.defects.dents.data[GRADE_OVER_MAX] == 0
        assert list(totals.defects.dents.tubes[5].keys()) == ['W6332']
        assert list(totals.defects.dents.tubes[10].keys()) == ['W14736']

        assert totals.defects.distribution.number == totals.defects.number
        assert len(totals.defects.danger_valve.grades) == 1
        assert len(totals.defects.distribution_bars.grades) == 40
        assert 'total 2' in str(totals.defects.dist_dents)

        assert 'total 42' in str(totals.defects.part_dist_loss_wallside)
        assert len(totals.defects.part_dist_loss_wallside.after_end) > 0
        assert len(totals.defects.part_dist_loss_wallside.before_start) > 0
        # print('---')
        # [print(i) for i in totals.markers]
