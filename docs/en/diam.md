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
