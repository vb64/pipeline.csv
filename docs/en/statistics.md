### Object statistics

You can get statistical data about objects in a csv file using the `Totals` class.

```python
from pipeline_csv.oegiv import File
from pipeline_csv.csvfile.statistics.totals import Totals

csv_file = File.from_file('DefTable.csv', 1400)
totals = Totals()
warns = []
totals.fill(csv_file, warns)
assert not warns
```

The statistical data contains the start and length marks of the section, as well as a list of markers.

```python
assert totals.start == 0
assert totals.length == 426625
assert len(totals.markers) == 5
```

The csv file contains 14 linear objects, which are located on 13 pipes.

```python
assert totals.liners.number == 14
assert totals.liners.tubes_all() == 13
```

Total number of pipes in csv file: 41.

```python
assert totals.pipes.number == 41
```

There are three pipe wall thicknesses in total: 7, 9, and 10 mm.

```python
assert list(sorted(totals.pipes.thick.data.keys())) == [70, 90, 100]
```

The number of pipes with a wall thickness of 7 mm is 22 units, with a total length of 232232 mm.

```python
pipes_7_mm = totals.pipes.thick.data[70]
assert pipes_7_mm.number == 22
assert pipes_7_mm.length == 232232
```

All pipes in the file are of the same type - straight-seam.

```python
from pipeline_csv.oegiv import TypeDefekt

assert list(totals.pipes.types.data.keys()) == [TypeDefekt.HORIZONTAL]
```

There are 75 defects in the file.

```python
assert totals.defects.number == 75
```

By location on the pipe wall, there are 6 defects with an undefined position and 69 external defects.

```python
from pipeline_csv import DefektSide

assert list(sorted(totals.defects.base_wallside.data.keys())) == [DefektSide.UNKNOWN, DefektSide.OUTSIDE]
assert totals.defects.base_wallside.data[DefektSide.UNKNOWN].number == 6
assert totals.defects.base_wallside.data[DefektSide.OUTSIDE].number == 69
```

There are 6 types of defects.

```python
types = totals.defects.base_types.data
assert len(types) == 6
```

56 defects of 'corrosion', 6 mechanical damage, etc.

```python
assert types[TypeDefekt.CORROZ].number == 56
assert types[TypeDefekt.MECHANIC].number == 6
assert types[TypeDefekt.DENT].number == 2
assert types[TypeDefekt.GWAN].number == 1
assert types[TypeDefekt.TECHNOLOGY].number == 8
assert types[TypeDefekt.FACTORY].number == 2
```

Distribution of defects by orientation hours.

```python
assert totals.defects.base_angle_anomalies.hours == {
  0: 6,  # 6 defects in the 12 o'clock sector
  1: 3,  # 3 defects in the 1 o'clock sector
  2: 6,  # etc
  3: 8,
  4: 8,
  5: 7,
  6: 9,
  7: 15,
  8: 9,
  9: 17,
  10: 7,
  11: 8
}
```

The `Totals` class also allows you to obtain extended statistics by overriding the statistics classes for pipes and defects.

To obtain defect statistics based on your own requirements, you need to define a class inheriting from the `pipeline_csv.csvfile.statistics.defects.Totals` base class.
In this class, you need to override the `__init__` and `add_defect` methods.

```python
from pipeline_csv.csvfile.statistics.defects import Totals as DefectsTotalsBase, Dents

class DefectsTotals(DefectsTotalsBase):
    """Custom defect totals class."""

    def __init__(self, start, length, markers):
        """Make new defects total object with custom properties."""
        super().__init__(start, length, markers)
        self.dents = Dents(grades=[5, 10])

    def add_defect(self, defect, tube, warns):
        """Add defect to custom statistics."""
        super().add_defect(defect, tube, warns)
        if defect.is_dent:
            self.dents.add_data(defect)
```

This class uses the `Dents` library class to collect user-defined statistics grading dent depth.

- up to 5% of the diameter
- from 5% to 10% of the diameter
- more than 10% of the diameter

When creating an instance of the CSV file statistics class, you must pass the name of the user-defined class as a parameter.

```python
from pipeline_csv.csvfile.statistics.totals import Totals

totals = Totals(defects_class=DefectsTotals)
totals.fill(csv_file, None)
```

After this, you will have access to dent statistics.

There are two dents in total.

```python
assert totals.defects.dents.number == 2
```

There are no dents deeper than 10% of the diameter.

```python
from pipeline_csv.csvfile.statistics.totals import GRADE_OVER_MAX

assert totals.defects.dents.data[GRADE_OVER_MAX] == 0
```

There is one dent with a depth of up to 5% and one from 5 to 10%.

```python
assert totals.defects.dents.data[5] == 1
assert totals.defects.dents.data[10] == 1
```

A dent of up to 5% depth is found on pipe number `W6332`, and a dent of up to 10% depth is found on pipe number `W14736`.

```python
assert list(totals.defects.dents.tubes[5].keys()) == ['W6332']
assert list(totals.defects.dents.tubes[10].keys()) == ['W14736']
```

You can use the following defect statistics library classes:

- DistSingle: distribution by distance
- DistWallside: distribution by distance broken down by position on the pipe wall
- DangerValve: distribution between valves
- Depth: grouping metal loss by specified depth intervals (as a percentage of the pipe wall thickness)
- Dents: grouping dents by specified depth intervals (as a percentage of the pipe diameter)
- Angles: distribution by orientation hours
- PropertyCounter: distribution by values of a specified defect property

You can also define your own defect statistics classes to collect the required data.
