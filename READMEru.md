# Библиотека PipelineCsv

[На английском](README.md)

Бесплатная, с открытым исходным кодом библиотека PipelineCsv
предназначена для работы с результатами анализа данных внутритрубной дефектоскопии в виде CSV-файла.

Библиотека предоставляет набор высокоуровневых операция с CSV-файлом.

Данные можно

-   зеркально переворачивать
-   склеивать вместе несколько CSV-файлов
-   растягивать/сжимать по дистанции по заданному набору опорных точек
-   интерпретировать как последовательность труб с геоданными

## Установка

```bash
pip install pipeline-csv
```

## Использование

Необходимо определить наборы дефектов и линейных объектов, используемых в вашем проекте.
Для этого нужно определить ваш класс строки CSV-файла, унаследовав его от класса `pipeline_csv.csvfile.row.Row` и
переопределить два метода данного класса: `defekts_dict` и `lineobj_dict`.

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
          TypeDefekt.CORROZ: "Коррозия",
          TypeDefekt.DENT: "Вмятина",
        }

    @staticmethod
    def lineobj_dict():
        return {
          TypeMarker.VALVE: "Кран",
          TypeMarker.CASE_START: "Патрон начало",
          TypeMarker.CASE_END: "Патрон конец",
        }
```

Для операции отзеркаливания данных нужно переопределить метод `markers_reverse`, который возвращает словарь, задающий правила замен при отзеркаливании.

```python
class MyRow(Row):

    @staticmethod
    def markers_reverse():
        return {
          TypeMarker.CASE_START: TypeMarker.CASE_END,
          TypeMarker.CASE_END: TypeMarker.CASE_START,
        }
```

Далее класс MyRow можно использовать в операциях с данными CSV-файлов.

### Создание CSV-файла

Создать новый пустой CSV-файл.

```python
from pipeline_csv.csvfile import File

csv_file = File()
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

### Отзеркаливание данных

Загружаем данные из сохраненного файла.

```python
csv_copy = File.from_file('example.csv')
```

Проверяем дистанцию последнего объекта и ориентацию дефекта.

```python
assert csv_copy.total_length == 12000
assert len(csv_copy.data) == 5

defect_row = csv_copy.data[3]
assert defect_row.is_defect
assert defect_row.orient_td == '4,00'
assert defect_row.orient_bd == '5,00'
```

Зеркалим данные.

```python
csv_copy.reverse()
```

У дефекта должна измениться относительная позиция в данных и отзеркалиться ориентация.

```python
defect_row = csv_copy.data[2]
assert defect_row.is_defect

assert defect_row.orient_td == '7,00'
assert defect_row.orient_bd == '8,00'
```

Сохраняем перевернутую копию в файл.

```python
csv_file.to_file('reversed.csv')
assert os.path.getsize('reversed.csv') > 0
```

### Пристыковка новых данных и сжатие/растяжение

Добавляем к исходному CSV пустую трубу длиной 10.0 м и перевернутые данные из файла.

```python
csv_file.join([10000, 'reversed.csv'])
assert csv_file.total_length == 28000
assert len(csv_file.data) == 11
```

Сжать дистанции и длины всех объектов в два раза.

```python
csv_file.dist_modify(
  # таблица поправок
  # каждый элемент задает пару 'существующая дистанция', 'новая дистанция'
  [[0, 0],
  [28000, 14000],
])
assert csv_file.total_length == 14000
```

Сохраняем в файл данные со сжатыми дистанциями.

```python
csv_file.to_file('transformed.csv')
assert os.path.getsize('transformed.csv') > 0
```

### Последовательность труб

Перебираем последовательность трубы.

```python
csv_trans = File.from_file('transformed.csv')
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
csv_geo = File.from_file('geo.csv')
last_tube = list(csv_geo.get_tubes(warnings))[-1]

assert last_tube.latitude == '10'
assert last_tube.longtitude == '11'
assert last_tube.altitude == '12'
```

### Положение дефекта на трубе

```python
from pipeline_csv.csvfile.tubes import Tube
```

Задать диаметр трубопровода 1000 мм.

```python
Tube.diam = 1000
```

Создать одну трубу на дистанци 1.0 м, длиной 11 м с одним продольным швом на 3 часа и одним дефектом на расстоянии 5.0 м отначала трубы.
Дефект длиной 20 мм, шириной 10 мм, глубиной 30% толщины стенки трубы, ориентацией от 4 до 5 часов.
Точка максимальной глубины дефекта на расстоянии 10 мм от левой границы дефекта, ориентацией 4 часа 30 минут.

```python
csv = File()
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

## Разработка

```
$ git clone git@github.com:vb64/pipeline.csv.git
$ cd pipeline.csv
$ make setup PYTHON_BIN=/path/to/python3
$ make tests
```
