### Создание CSV-файла

Создать новый пустой CSV-файл для трубопровода диаметром 1000 мм.

```python
from pipeline_csv.csvfile import File

csv_file = File(1000)
```

Создаем трубу на дистанции 1.0 м длиной 11 м, с толщиной стенки 10.5 мм, с одним продольным швом на 3 часа 00 минут.

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

Добавляем на эту трубу наружный дефект на дистанции 5.0 м от начала трубы, длиной 20 мм, шириной 10 мм, глубиной 30% от толщины стенки.
Ориентация от 4 часов 00 минут до 5 часов 00 минут.
Точка максимальной глубины на дистанции 5.01 м от начала трубы, ориентация 4 часа 30 минут.
Примечание: 'потеря металла'.

```python
from pipeline_csv import DefektSide

csv_file.data.append(MyRow.as_defekt(
  6000,
  TypeDefekt.CORROZ,
  DefektSide.OUTSIDE
  '20', '10', '30',
  Orientation(4, 0), Orientation(5, 0),
  6010, Orientation(4, 30),
  'потеря металла'
))
```

Сохраняем данные в файл.

```python
import os

csv_file.to_file('example.csv')
assert os.path.getsize('example.csv') > 0
```
