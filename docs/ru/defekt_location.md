### Положение дефекта на трубе

Диаметр трубопровода 1000 мм.

```python
csv = File(1000)
```

Создать одну трубу на дистанци 1.0 м, длиной 11 м с одним продольным швом на 3 часа и одним дефектом на расстоянии 5.0 м отначала трубы.

Дефект длиной 20 мм, шириной 10 мм, глубиной 30% толщины стенки трубы, ориентацией от 4 до 5 часов.

Точка максимальной глубины дефекта на расстоянии 10 мм от левой границы дефекта, ориентацией 4 часа 30 минут.

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

Один дефект на трубе.

```python
assert len(pipe.defects) == 1
defect = pipe.defects[0]
```

Дефект является потерей металла, не вмятиной.
Дефект не находится на поперечном либо продольном шве.

```python
assert defect.is_metal_loss
assert not defect.is_dent
assert not defect.is_at_weld
assert not defect.is_at_seam
```

Ориентация дефекта как точки соотвествует ориентации точки максимальной глубины на 4:30.

```python
assert defect.orientation_point.as_minutes == 270
```

Расстояние (мм) от точки максимальной глубины до начала трубы.

```python
assert defect.mp_left_weld == 5010
```

Расстояние (мм) от точки максимальной глубины до конца трубы.

```python
assert defect.mp_right_weld == 5990
```

Расстояние (мм) от точки максимальной глубины до продольного шва.

```python
assert defect.mp_seam == 392
```

Расстояние (мм) от точки максимальной глубины до ближайшего сварного шва.

```python
assert defect.mp_seam_weld == 392
```

Расстояние (мм) от левой границы дефекта до начала трубы.

```python
assert defect.to_left_weld == 5000
```

Расстояние (мм) от правой границы дефекта до конца трубы.

```python
assert defect.to_right_weld == 5980
```

Расстояние (мм) от границы дефекта до продольного шва.

```python
assert defect.to_seam == 60
```

Расстояние (мм) от границы дефекта до ближайшего сварного шва.

```python
assert defect.to_seam_weld == 60
```
