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

Распределение дефектов по часам ориентации.

```python
assert totals.defects.base_angle_anomalies.hours == {
  0: 6,  # 6 дефектов в секторе на 12 часов
  1: 3,  # 3 дефекта в секторе на 1 час
  2: 6,  # и т.д.
  3: 8,
  4: 8,
  5: 7,
  6: 9,
  7: 15,
  8: 9,
  9: 17,
  10: 7,
  11: 8
}
```

Класс `Totals` позволяет также получать расширенную статистику путем переопределения классов статистики для труб и дефектов.

Чтобы получить статистику дефектов по собственным требованиям, нужно определить класс, унаследовав его от базового класса `pipeline_csv.csvfile.statistics.defects.Totals`.
В этом классе нужно переопределить методы `__init__` и `add_defect`.

```python
from pipeline_csv.csvfile.statistics.defects import Totals as DefectsTotalsBase, Dents

class DefectsTotals(DefectsTotalsBase):
    """Custom defect totals class."""

    def __init__(self, start, length, markers):
        """Make new defects total object with custom properties."""
        super().__init__(start, length, markers)
        self.dents = Dents(grades=[5, 10])

    def add_defect(self, defect, tube, warns):
        """Add defect to custom statistics."""
        super().add_defect(defect, tube, warns)
        if defect.is_dent:
            self.dents.add_data(defect)
```

В данном классе при помощи библиотечного класса `Dents` собирается пользовательская статистика с градацией вмятин по глубине.

- до 5% диаметра
- от 5% до 10% диаметра
- более 10% диаметра

При создании экземпляра класса статистики csv-файла нужно передать ему в качестве параметра имя пользовательского класса.

```python
from pipeline_csv.csvfile.statistics.totals import Totals

totals = Totals(defects_class=DefectsTotals)
totals.fill(csv_file, None)
```

После этого вы получите доступ к данным статистики по вмятинам.

Всего имеется две вмятины.

```python
assert totals.defects.dents.number == 2
```

Нет вмятин глубиной более 10% диаметра.

```python
from pipeline_csv.csvfile.statistics.totals import GRADE_OVER_MAX

assert totals.defects.dents.data[GRADE_OVER_MAX] == 0
```
Имеется по одной вмятине глубиной до 5% и от 5 до 10%.

```python
assert totals.defects.dents.data[5] == 1
assert totals.defects.dents.data[10] == 1
```

Вмятина глубиной до 5% находится на трубе с номером `W6332`, а вмятина глубиной до 10% на трубе с номером `W14736`.

```python
assert list(totals.defects.dents.tubes[5].keys()) == ['W6332']
assert list(totals.defects.dents.tubes[10].keys()) == ['W14736']
```

Вы можете использовать следующие библиотечные классы статистики дефектов:

- DistSingle: распределение по дистанции
- DistWallside: распределение по дистанции с разбивкой по положению на стенке трубы
- DangerValve: распределение между кранами
- Depth: группировка потерь металла по заданным интервалам глубин (в % от толщины стенки трубы)
- Dents: группировка вмятин по заданным интервалам глубин (в % от диаметра трубы)
- Angles: распределение по часам ориентации
- PropertyCounter: распределение по значениям указанного свойства дефекта

Также вы можете определять собственные классы статистики дефектов для сбора нужнфх данных.
