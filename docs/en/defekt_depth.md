### Depth of defect

Rows of the csv file can contain data on the depth of the defect in the following units.

- percentage of the pipe wall thickness for metal loss or of the pipe diameter for dents (default)
- hundredths of a millimeter

The `Row.depth_units` attribute describes the units of measurement for the depth of the defect.

```python
from pipeline_csv.csvfile.row import Row, Depth

class MyRow(Row):

    depth_units = Depth.HundredthsOfMillimeter

```

The `Row.dents_dict` method specifies a list of defect types that are interpreted as dents.

```python
class MyRow(Row):

    @staticmethod
    def dents_dict():
        return [TypeDefekt.DENT]
```

A dent measuring 10x10 and 70 mm deep on a pipe with a diameter of 700 mm and a wall thickness of 10 mm.

```python
from pipeline_csv.csvfile import Stream
from pipeline_csv.csvfile.tubes import Tube
from pipeline_csv.csvfile.defect import Defect

pipe = Tube(Row.as_weld(10), Stream(diameter=700), None)
pipe.thick = 100  # 10 mm

row = Row.as_defekt(
  11, TypeDefekt.DENT, 0, '10', '10',
  '7000',  # 70 mm
  None, None, None, None, ''
)

dent = Defect(row, pipe)

assert dent.depth_mm == 70
```

As a percentage of the pipe diameter, the dent depth is 10%.

```python
assert dent.depth_percent == 10
```

The `Row.mloss_dict` method specifies a list of defect types that are interpreted as metal loss.

```python
class MyRow(Row):

    @staticmethod
    def mloss_dict():
        return [TypeDefekt.CORROZ]
```

Metal loss measuring 10x10, 5mm deep.

```python
row = Row.as_defekt(
  11, TypeDefekt.CORROZ, 0, '10', '10',
  '500',  # 5 mm
  None, None, None, None, ''
)
mloss = Defect(row, pipe)

assert mloss.depth_mm == 5
```

As a percentage of the pipe wall thickness, the depth of the defect is 50%.

```python
assert mloss.depth_percent == 50
```

For defect types other than metal loss or dent, the depth of the defect is not defined.

```python
row = Row.as_defekt(
  11, TypeDefekt.FACTORY, 0, '10', '10',
  '500',  # 5 mm
  None, None, None, None, ''
)
factory = Defect(row, pipe)

assert factory.depth_mm is None
assert factory.depth_percent is None
```
