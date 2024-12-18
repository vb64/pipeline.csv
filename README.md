# PipelineCsv library

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/pipeline.csv/pep257.yml?label=Pep257&style=plastic&branch=main)](https://github.com/vb64/pipeline.csv/actions?query=workflow%3Apep257)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/pipeline.csv/py3.yml?label=Python%203.8-3.13&style=plastic&branch=main)](https://github.com/vb64/pipeline.csv/actions?query=workflow%3Apy3)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/031838411159440885e8c4a28f233c4e)](https://app.codacy.com/gh/vb64/pipeline.csv/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/031838411159440885e8c4a28f233c4e)](https://app.codacy.com/gh/vb64/pipeline.csv/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

[In Russian](READMEru.md)

The free, open source PipelineCsv library is designed to work with the results of analysis of in-line flaw detection data in the form of a CSV file.

The library provides a set of high-level operations with CSV file.

Data can be

- mirrored
- glued together from several CSV files
- stretched/compressed along the distance according to a given set of intermediate points
- interpreted as an iterable sequence of pipes with geodata

## Installation

```bash
pip install pipeline-csv
```

## Usage

It is necessary to define the sets of defects and markers used in your project.
To do this, you need to define your class for CSV row by deriving it from the `pipeline_csv.csvfile.row.Row` class and
override two methods of this class: `defekts_dict` and `lineobj_dict`.

```python
from pipeline_csv.csvfile.row import Row

class TypeMarker:
    VALVE = 0
    CASE_START = 1
    CASE_END = 2

class TypeDefekt:
    CORROZ = 0
    DENT = 1

class MyRow(Row):

    @staticmethod
    def defekts_dict():
        return {
          TypeDefekt.CORROZ: "Corrosion",
          TypeDefekt.DENT: "Dent",
        }

    @staticmethod
    def lineobj_dict():
        return {
          TypeMarker.VALVE: "Valve",
          TypeMarker.CASE_START: "Casing start",
          TypeMarker.CASE_END: "Casing end",
        }
```

For the data mirroring operation, you need to override the `markers_reverse` method, which returns a dictionary that specifies the rules for replacing when mirroring.

```python
class MyRow(Row):

    @staticmethod
    def markers_reverse():
        return {
          TypeMarker.CASE_START: TypeMarker.CASE_END,
          TypeMarker.CASE_END: TypeMarker.CASE_START,
        }
```

Further, the MyRow class can be used in operations with data of CSV files.

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

### Data mirroring

Create copy from saved file.

```python
csv_copy = File.from_file('example.csv', 1000)
```

Check distance of the last object in copy and defect orientation.

```python
assert csv_copy.total_length == 12000
assert len(csv_copy.data) == 5

defect_row = csv_copy.data[3]
assert defect_row.is_defect
assert defect_row.orient_td == '4,00'
assert defect_row.orient_bd == '5,00'
```

Reverse copy.

```python
csv_copy.reverse()
```

Relative position of defekt must change and defect orientation must be mirrored.

```python
defect_row = csv_copy.data[3]
assert defect_row.is_defect

assert defect_row.orient_td == '7,00'
assert defect_row.orient_bd == '8,00'
```

Save reversed copy to file.

```python
csv_file.to_file('reversed.csv')
assert os.path.getsize('reversed.csv') > 0
```

### Docking new data and compression/stretching

Append to initial CSV empty pipe with length 10.0 m and reversed copy from the file.

```python
csv_file.join([10000, 'reversed.csv'])
assert csv_file.total_length == 28000
assert len(csv_file.data) == 11
```

Compress distances and length of all objects in half.

```python
csv_file.dist_modify(
  # table of corrections
  # each node define as pair 'existing distance', 'new distance'
  [[0, 0],
  [28000, 14000],
])
assert csv_file.total_length == 14000
```

Save file with compress distances.

```python
csv_file.to_file('transformed.csv')
assert os.path.getsize('transformed.csv') > 0
```

### Pipe sequence

Iterate by pipes.

```python
csv_trans = File.from_file('transformed.csv', 1000)
warnings = []
current_dist = 0
for i in csv_trans.get_tubes(warnings):
    assert i.dist >= current_dist
    current_dist = i.dist
    tube = i

assert not warnings
```

Set geodata for tube

```python
assert tube.latitude == ''
assert tube.longtitude == ''
assert tube.altitude == ''

tube.set_geo(10, 11, 12)

assert tube.latitude == 10
assert tube.longtitude == 11
assert tube.altitude == 12

csv_trans.to_file('geo.csv')
assert os.path.getsize('geo.csv') > 0
```

Load from saved file and check geodata from last pipe.

```python
csv_geo = File.from_file('geo.csv', 1000)
last_tube = list(csv_geo.get_tubes(warnings))[-1]

assert last_tube.latitude == '10'
assert last_tube.longtitude == '11'
assert last_tube.altitude == '12'
```

### Defect location at the pipe

Pipeline diameter 1000 mm.

```python
csv = File(1000)
```

Define one pipe at distance 1.0 m, length = 11.0 m with one seam with orientation 3 hour 00 minutes and one defect at distance 5.0 m from left tube weld.

Defect length = 20 mm, width = 10 mm, depth = 30% tube wall thickness, orientation from 4 hours 00 minutes to 5 hours 00 minutes.

Maximum depth point at 10 mm from left border of defect, orientation 4 hours 30 minutes.

```python
csv.data = [
  Row.as_weld(1000),
  Row.as_seam(1020, TypeHorWeld.HORIZONTAL, Orientation(3, 0), None),
  Row.as_defekt(
    6000,
    TypeDefekt.CORROZ, DefektSide.INSIDE,
    '20', '10', '30',
    Orientation(4, 0), Orientation(5, 0),
    Orientation(4, 30), 6010,
    'corrozion'
  ),
  Row.as_weld(12000),
]

pipes = list(csv.get_tubes())
assert len(pipes) == 1
pipe = pipes[0]
assert pipe.diam == 1000
```

One defect at the pipe.

```python
assert len(pipe.defects) == 1
defect = pipe.defects[0]
```

Defect is metal loss, not dent.
Defect is not located at the weld/seam.

```python
assert defect.is_metal_loss
assert not defect.is_dent
assert not defect.is_at_weld
assert not defect.is_at_seam
```

Defect as point orientation is maximum depth point orientation at 4:30.

```python
assert defect.orientation_point.as_minutes == 270
```

Distance (mm) from maximum depth point to upstream weld.

```python
assert defect.mp_left_weld == 5010
```

Distance (mm) from maximum depth point to downstream weld.

```python
assert defect.mp_right_weld == 5990
```

Distance (mm) from maximum depth point to seam.

```python
assert defect.mp_seam == 392
```

Distance (mm) from maximum depth point to nearest seam/weld.

```python
assert defect.mp_seam_weld == 392
```

Distance (mm) from left defect border to upstream weld.

```python
assert defect.to_left_weld == 5000
```

Distance (mm) from right defect border to downstream weld.

```python
assert defect.to_right_weld == 5980
```

Distance (mm) from defect borders to seam.

```python
assert defect.to_seam == 60
```

Distance (mm) from defect borders to nearest seam/weld.

```python
assert defect.to_seam_weld == 60
```

### Pipeline diameter changing

Pipeline diameter 1200 mm.
Four pipes with a diameter change from 1200 to 1400.

```python
csv_file = File(1200)

csv_file.data += [
  Row.as_weld(0),
  Row.as_weld(1000),
  Row.as_diam(1001, 1200, 1400),
  Row.as_weld(2000),
  Row.as_weld(3000),
  Row.as_weld(4000),
]

pipes = list(csv_file.get_tubes())
assert len(pipes) == 4
```

The first pipe has a diameter of 1200 without a diameter change.

```python
assert pipes[0].diameter == 1200
assert pipes[0].is_diameter_change is None
```

The second pipe with a diameter change of 1200 -> 1400.

```python
assert pipes[1].diameter == 1200
assert pipes[1].is_diameter_change == 1400
```

The last two pipes have a diameter of 1400 without a diameter change.

```python
assert pipes[2].diameter == 1400
assert pipes[2].is_diameter_change is None
assert pipes[3].diameter == 1400
assert pipes[3].is_diameter_change is None
```

Mirroring data.

```python
fname = 'diam.csv'
csv_file.to_file(fname)
csv_file = File.from_file(fname)

csv_file.reverse()
csv_file.to_file(fname)
csv_file = File.from_file(fname)

pipes = list(csv_file.get_tubes())
assert len(pipes) == 4
```

The first two pipes have a diameter of 1400 without a diameter change.

```python
assert int(pipes[0].diameter) == 1400
assert pipes[0].is_diameter_change is None
assert int(pipes[1].diameter) == 1400
assert pipes[1].is_diameter_change is None
```

The third pipe has a diameter change of 1400 -> 1200.

```python
assert int(pipes[2].diameter) == (1400)
assert int(pipes[2].is_diameter_change) == 1200
```

The last pipe has a diameter of 1200 without a diameter change.

```python
assert int(pipes[3].diameter) == 1200
assert pipes[3].is_diameter_change is None
```

## Development

```bash
git clone git@github.com:vb64/pipeline.csv.git
cd pipeline.csv
make setup PYTHON_BIN=/path/to/python3
make tests
```
