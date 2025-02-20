### Глубина дефекта

Строки csv-файла могут содержать данные о глубине дефекта в следующих единицах.

- процент от толщины стенки трубы для потерь металла либо от диаметра трубы для вмятин (по умолчанию)
- сотые доли миллиметра

Атрибут `Row.depth_units` описывает единицы измерения для глубины дефекта.

```python
from pipeline_csv.csvfile.row import Row, Depth

class MyRow(Row):

    depth_units == Depth.HundredthsOfMillimeter

```

Метод `Row.dents_dict` задает список типов дефектов, которые интерпретируются как вмятины.

```python
class MyRow(Row):

    @staticmethod
    def dents_dict():
        return [TypeDefekt.DENT]
```

Вмятина размером 10x10 глубиной 70 мм на трубе диаметром 700 мм c толщиной стенки 10 мм.

```python
from pipeline_csv.csvfile import Stream
from pipeline_csv.csvfile.tubes import Tube
from pipeline_csv.csvfile.defect import Defect

pipe = Tube(Row.as_weld(10), Stream(diameter=700), None)
pipe.thick = 100  # 10 mm

row = Row.as_defekt(
  11, TypeDefekt.DENT, 0, '10', '10',
  '7000',  # 70 mm
  None, None, None, None, ''
)

dent = Defect(row, pipe)

assert dent.depth_mm == 70
```

В процентах от диаметра трубы глубина вмятины 10 %.

```python
assert dent.depth_percent == 10
```

Метод `Row.mloss_dict` задает список типов дефектов, которые интерпретируются как потери металла.

```python
class MyRow(Row):

    @staticmethod
    def mloss_dict():
        return [TypeDefekt.CORROZ]
```

Потеря металла размером 10x10 глубиной 5 мм.

```python
row = Row.as_defekt(
  11, TypeDefekt.CORROZ, 0, '10', '10',
  '500',  # 5 mm
  None, None, None, None, ''
)
mloss = Defect(row, pipe)

assert mloss.depth_mm == 5
```

В процентах от толщины стенки трубы глубина дефекта 50 %.

```python
assert mloss.depth_percent == 50
```

Для типов дефектов, не являющихся потерей металла или вмятиной глубина дефекта не определена.

```python
row = Row.as_defekt(
  11, TypeDefekt.FACTORY, 0, '10', '10',
  '500',  # 5 mm
  None, None, None, None, ''
)
factory = Defect(row, pipe)

assert factory.depth_mm is None
assert factory.depth_percent is None
```
