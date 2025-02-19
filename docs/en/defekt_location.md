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
