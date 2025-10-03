### Статистика объектов

Вы можете получать статистические данные об обьектах csv-файла при помощи класса `Totals`.

```python
from pipeline_csv.oegiv import File
from pipeline_csv.csvfile.statistics.totals import Totals

csv_file = File.from_file('DefTable.csv', 1400)
totals = Totals()
warns = []
totals.fill(csv_file, warns)
assert not warns
```

В стат.данных есть отметки начала и дины участка, а также список маркеров.

```python
assert totals.start == 0
assert totals.length == 426625
assert len(totals.markers) == 5
```

В csv-файле есть 14 линейных обьектов, которые расположены на 13 трубах.

```python
assert totals.liners.number == 14
assert totals.liners.tubes_all() == 13
```

Общее количество труб в csv-файле: 41.

```python
assert totals.pipes.number == 41
```

Всего имеется три толщины стенки труб: 7, 9, и 10 мм.

```python
assert list(sorted(totals.pipes.thick.data.keys())) == [70, 90, 100]
```

Число труб с толщиной стенки 7 мм - 22 штуки, общей длиной 232232 мм.

```python
pipes_7_mm = totals.pipes.thick.data[70]
assert pipes_7_mm.number == 22
assert pipes_7_mm.length == 232232
```

Все трубы в файле одного типа - прямошовные.

```python
from pipeline_csv.oegiv import TypeDefekt

assert list(totals.pipes.types.data.keys()) == [TypeDefekt.HORIZONTAL]
```

В файле имеется 75 дефектов.

```python
assert totals.defects.number == 75
```

По расположению на стенке трубы 6 дефектов с неопределенным положением и 69 наружных дефектов.

```python
from pipeline_csv import DefektSide

assert list(sorted(totals.defects.base_wallside.data.keys())) == [DefektSide.UNKNOWN, DefektSide.OUTSIDE]
assert totals.defects.base_wallside.data[DefektSide.UNKNOWN].number == 6
assert totals.defects.base_wallside.data[DefektSide.OUTSIDE].number == 69
```

Имеются дефекты 6 типов.

```python
types = totals.defects.base_types.data
assert len(types) == 6
```

56 дефектов 'коррозия', 6 мехповреждений и т.д.

```python
assert types[TypeDefekt.CORROZ].number == 56
assert types[TypeDefekt.MECHANIC].number == 6
assert types[TypeDefekt.DENT].number == 2
assert types[TypeDefekt.GWAN].number == 1
assert types[TypeDefekt.TECHNOLOGY].number == 8
assert types[TypeDefekt.FACTORY].number == 2
```

Распределение числа дефектов по часам ориентации.
