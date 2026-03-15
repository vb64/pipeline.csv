### Calculation of the degree of danger of defects

The following methods for calculating the severity of defects are available in the `pipeline_csv.integrity` library module.

- [ASME B31G 1991](/docs/integrity/asme/b31g_1991/b31g_1991.md)
- ASME B31G 2012

![method ASME B31G](/docs/img/asme1991.png)

## Usage

The depth of defects will be specified in hundredths of a millimeter.

```python
from pipeline_csv.oegiv import Row as BaseRow
from pipeline_csv.csvfile.row import Depth

class Row(BaseRow):
    """Row with mm depth."""

    depth_units = Depth.HundredthsOfMillimeter
```

The pipe has a diameter of 1420 mm a length of 11.2 meters, and a wall thickness of 16 mm.

```python
from pipeline_csv.csvfile import Stream
from pipeline_csv.csvfile.tubes import Tube

pipe = Tube(Row.as_weld(10), Stream(diameter=1420), None)
pipe.length = 11200
pipe.thick_mm = 16
```

Pipe material.

```python
from pipeline_csv.integrity.material import PipeMaterial

material = PipeMaterial(
  "Steel",
  295,  # yield strength, MPa
  smts=420  # tensile strength, MPa
)
```

Metal loss defect (internal corrosion) with a specified position on the pipe and a given depth.

```python
from pipeline_csv import DefektSide
from pipeline_csv.orientation import Orientation
from pipeline_csv.oegiv import TypeDefekt

pipe.add_object(
  Row.as_defekt(
    1000,  # the defect starts at a distance of 1 meter from the beginning of the pipe
    TypeDefekt.CORROZ,
    DefektSide.INSIDE,
    100,  # defect length 100 mm
    10,  # defect width 10 mm
    str(1 * 100),  # defect depth 1 mm
    # around the circumference of the pipe, the defect begins at 10 minutes of arc from the top point of the pipe
    Orientation.from_minutes(10),
    # the size of the defect along the circumference is 20 arc minutes
    Orientation.from_minutes(10 + 20),
    None,  # MPoint orient
    None,  # MPoint dist
    ''  # comment
  )
)
defect = pipe.defects[-1]
```

Context for calculating the degree of defect hazard using the ASME B31G method at a pressure of 7 MPa.

```python
from pipeline_csv.integrity.method.asme.b31g_2012 import Context

asme = Context(defect, material, 7.0)
```

The depth of the defect is less than 10% of the pipe wall thickness, the calculated ERF of the defect is less than 1, there is no danger.

```python
assert defect.depth_mm == 1
assert pipe.thick_mm == 16
assert 0.94 < asme.erf() < 0.97
assert asme.years() > 1
```

For very low pressure cases, repair is never required (special value REPAIR_NOT_REQUIRED=777).

```python
asme.maop = 0.01
assert asme.years() == asme.REPAIR_NOT_REQUIRED
```

A defect depth of 50% of the pipe wall thickness requires repair at the specified working pressure in the pipe (ERF> 1).

```python
asme.maop = 20
defect.depth_mm = 8
defect.length = 200
assert asme.years() == 0
assert asme.erf() > 1
```

When the operating pressure is reduced to a safe value, the defect does not require repair.

```python
asme.maop = asme.safe_pressure - 0.1

assert asme.years() > 0
assert asme.erf() < 1
```

If you set context property `is_explain = True`, then you can get explanation in text form.

```python
asme.is_explain = True
assert asme.years() > 0
```

After the calculation is completed, the `asme.explain()` method will return an explanation of the calculation in text form.

```text
Calculate ERF by ASME B31G 2012 classic.
Calculate failure stress level by the classic way.
Parameter Sflow = 1.1 * material_smys.
Sflow = 1.1 * 52000 = 57200.0.
Parameter Z = length^2 / (diameter * wallthickness).
Z = 30^2 / (56 * 0.63) = 25.51.
Parameter Z = 25.51 > 20.
Failure stress level = Sflow * (1 - depth / wallthickness).
stress_fail = 57200.0 * (1 - 0.31 / 0.63) = 29053.968.
Failure pressure = 2 * stress_fail * wallthickness / diameter.
press_fail = 2 * 29053.968 * 0.63 / 56 = 653.714.
ERF = pipe_maop / press_fail.
ERF = 500 / 653.714 = 0.765

Repair is not required at the moment, calculate the time before repair.
With corrosion rate 0.016 mm/year, pipe wall 0.63 and depth 0.31 a through hole is formed after years: 21.
Calculating the year in which the corrosion growth of the defect will require repair.
Years: 4 ERF: 0.952.
Years: 5 ERF: 1.014.
Defect will require repair after years: 4.
```

## Examples

Living version of online calculator example, that use this library, can be [found here](https://clan-panel-na.appspot.com/).
The source code of this example placed in this repo in [example dir](/example/integrity/web/gae/).

The source code for the example for running the online calculator on a local computer is contained in the [localhost directory](/example/integrity/web/localhost/) of the repository.
