### Creating a CSV file

Construct new csv file from scratch for pipeline 1000 mm diameter.

```python
from pipeline_csv.csvfile import File

csv_file = File(1000)
```

Define tube at distance 1.0 m length = 11.0 m, thick = 10.5 mm with one seam with orientation 3 hour 00 minutes.

```python
from pipeline_csv import TypeHorWeld
from pipeline_csv.orientation import Orientation

csv_file.data = [
  MyRow.as_weld(1000),
  MyRow.as_thick(1010, 105),
  MyRow.as_seam(1020, TypeHorWeld.HORIZONTAL, Orientation(3, 0), None),
  MyRow.as_weld(12000),
]
```

Add outside defect to tube at distance 5.0 m from left tube weld,
length = 20 mm, width = 10 mm, depth = 30% tube wall thickness,
orientation from 4 hours 00 minutes to 5 hours 00 minutes,
maximum depth point at distance 5.01 m from left tube weld, orientation 4 hours 30 minutes
with comment 'metal loss'.

```python
from pipeline_csv import DefektSide

csv_file.data.append(MyRow.as_defekt(
  6000,
  TypeDefekt.CORROZ,
  DefektSide.OUTSIDE
  '20', '10', '30',
  Orientation(4, 0), Orientation(5, 0),
  6010, Orientation(4, 30),
  'metal loss'
))
```

Save csv to file.

```python
import os

csv_file.to_file('example.csv')
assert os.path.getsize('example.csv') > 0
```
