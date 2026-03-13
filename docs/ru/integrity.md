### Расчет степени опасности дефектов

В модуле библиотеки `pipeline_csv.integrity` доступны следующие методы расчета степени опасности дефектов.

- ASME B31G 1991
- ASME B31G 2012

![методика ASME B31G](/docs/img/asme1991.png)


Глубина дефектов будет задаваться в сотых долях миллиметра.

```python
from pipeline_csv.oegiv import Row as BaseRow
from pipeline_csv.csvfile.row import Depth

class Row(BaseRow):
    """Row with mm depth."""

    depth_units = Depth.HundredthsOfMillimeter
```

Труба диаметром 1420 мм, длиной 11.2 метра, с толщиной стенки 16 мм.

```python
from pipeline_csv.csvfile import Stream
from pipeline_csv.csvfile.tubes import Tube

pipe = Tube(Row.as_weld(10), Stream(diameter=1420), None)
pipe.length = 11200  # длина 11.2 метра
pipe.thick_mm = 16
```

Материал трубы.

```python
from pipeline_csv.integrity.material import PipeMaterial

material = PipeMaterial(
  "Сталь",
  295,  # предел текучести, Мпа
  smts=420  # предел прочности на растяжение, Мпа
)
```

Дефект потери металла (внутренняя коррозия) с указанным положением на трубе и заданной глубиной.

```python
from pipeline_csv import DefektSide
from pipeline_csv.orientation import Orientation
from pipeline_csv.oegiv import TypeDefekt

pipe.add_object(
  Row.as_defekt(
    1000,  # дефект начинается на расстоянии 1 метра от начала трубы
    TypeDefekt.CORROZ,
    DefektSide.INSIDE,
    100,  # длина дефекта 100 мм
    10,  # ширина дефекта 10 мм
    str(1 * 100),  # глубина дефекта 1 мм
    # по окружности трубы дефект начинается на 10 угловых минут от верхней точки трубы
    Orientation.from_minutes(10),
    # размер дефекта по окружности составляет 20 угловых минут
    Orientation.from_minutes(10 + 20),
    None,  # MPoint orient
    None,  # MPoint dist
    ''  # comment
  )
)
defect = pipe.defects[-1]
```

Контекст для вычисления степени опасности дефекта по методике ASME B31G при давлении 7 Мпа.

```python
from pipeline_csv.integrity.method.asme.b31g_2012 import Context

asme = Context(defect, material, 7.0)
```

Глубина дефекта менее 10% толщины стенки трубы, рассчитанный КБД (ERF) дефекта менее 1, опасности нет.

```python
assert defect.depth_mm == 1
assert pipe.thick_mm == 16
assert 0.94 < asme.erf() < 0.97
assert asme.years() > 1
```

Для случаев очень низкого давления ремонт не требуется никогда (специальное значение REPAIR_NOT_REQUIRED=777).

```python
asme.maop = 0.01
assert asme.years() == asme.REPAIR_NOT_REQUIRED
```

Глубина дефекта 50% от толщины стенки трубы требует ремонта при указанном рабочем давлении в трубе (КБД > 1).

```python
asme.maop = 20
defect.depth_mm = 8
defect.length = 200
assert asme.years() == 0
assert asme.erf() > 1
```

При снижении рабочего давления до безопасной величины дефект не требует ремонта.

```python
asme.maop = asme.safe_pressure - 0.1

assert asme.years() > 0
assert asme.erf() < 1
```

В свойстве контекста `is_explain` можно задать словарь.

```python
from pipeline_integrity.i18n import Lang

asme.is_explain = asme.lang(Lang.Ru)
assert asme.years() > 0
```

После сделанного расчета метод `asme.explain()` вернет объяснение сделанного расчета в текстовом виде на русском языке.

```text
Вычисляем КБД по ASME B31G 2012 классический.
Вычисляем величину напряжения разрыва классическим методом.
Параметр Sflow = 1.1 * предел_текучести.
Sflow = 1.1 * 295 = 324.5.
Параметр Z = длина^2 / (диаметр * толщина).
Z = 200^2 / (1420 * 16) = 1.761.
Параметр M = sqrt(1 + 0.8 * Z).
M = sqrt(1 + 0.8 * 1.761) = 1.552.
Параметр Z = 1.761 <= 20.
Напряжение разрыва = Sflow * (1 - 2/3 * (глубина / толщина)) / (1 - 2/3 * (глубина / толщина) / M).
stress_fail = 324.5 * (1 - 2/3 * (8 / 16)) / (1 - 2/3 * (8 / 16 / 1.552)) = 275.509.
Давление разрыва = 2 * stress_fail * толщина / диаметр.
press_fail = 2 * 275.509 * 16 / 1420 = 6.209.
КБД = рабочее_давление / давление_разрыва.
ERF = 6.108663279971968 / 6.209 = 0.984

На данный момент ремонт не требуется, вычисляем время до ремонта.
При скорости коррозии 0.4 мм/год, толщине стенки 16 и глубине дефекта 8, сквозной дефект образуется через лет: 21.
Вычисляем через сколько лет дефект потребует ремонта при заданной скорости коррозии.
Года: 1 КБД: 0.995.
Года: 2 КБД: 1.007.
Дефект нужно будет отремонтировать через лет: 1.
```
