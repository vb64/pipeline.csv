### Последовательность труб

Перебираем последовательность трубы.

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

Задаем геоданные для трубы.

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

Загружаем сохраненный файл и проверяем геоданные для последней трубы.

```python
csv_geo = File.from_file('geo.csv', 1000)
last_tube = list(csv_geo.get_tubes(warnings))[-1]

assert last_tube.latitude == '10'
assert last_tube.longtitude == '11'
assert last_tube.altitude == '12'
```
