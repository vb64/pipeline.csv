### Изменение диаметра трубопровода

Диаметр трубопровода 1200 мм.

```python
csv_file = File(1200)
```

Четыре трубы с переходом диаметра с 1200 на 1400.

```python
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

Первая труба диаметром 1200 без перехода диаметра.

```python
assert pipes[0].diameter == 1200
assert pipes[0].is_diameter_change is None
```

Вторая труба с переходом диаметра 1200 -> 1400.

```python
assert pipes[1].diameter == 1200
assert pipes[1].is_diameter_change == 1400
```

Последние две трубы диаметром 1400 без перехода диаметра.

```python
assert pipes[2].diameter == 1400
assert pipes[2].is_diameter_change is None
assert pipes[3].diameter == 1400
assert pipes[3].is_diameter_change is None
```

Зеркалим данные.

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

Первые две трубы диаметром 1400 без перехода диаметра.

```python
assert int(pipes[0].diameter) == 1400
assert pipes[0].is_diameter_change is None
assert int(pipes[1].diameter) == 1400
assert pipes[1].is_diameter_change is None
```

Третья труба с переходом диаметра 1400 -> 1200.

```python
assert int(pipes[2].diameter) == (1400)
assert int(pipes[2].is_diameter_change) == 1200
```

Последняя труба диаметром 1200 без перехода диаметра.

```python
assert int(pipes[3].diameter) == 1200
assert pipes[3].is_diameter_change is None
```
