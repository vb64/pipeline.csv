# Библиотека PipelineCsv

[На английском](README.md)

Бесплатная, с открытым исходным кодом библиотека PipelineCsv
предназначена для работы с результатами анализа данных внутритрубной дефектоскопии в виде CSV-файла.

Библиотека предоставляет набор высокоуровневых операция с CSV-файлом.

Данные можно

- зеркально переворачивать
- склеивать вместе несколько CSV-файлов
- растягивать/сжимать по дистанции по заданному набору опорных точек
- интерпретировать как последовательность труб с геоданными

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
    FACTORY = 2

class MyRow(Row):

    @staticmethod
    def defekts_dict():
        return {
          TypeDefekt.CORROZ: "Коррозия",
          TypeDefekt.DENT: "Вмятина",
          TypeDefekt.FACTORY: "Производственный дефект",
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

- [Создание CSV-файла](docs/ru/csv_file.md)
- [Отзеркаливание данных](docs/ru/mirror.md)
- [Пристыковка новых данных и сжатие/растяжение](docs/ru/join.md)
- [Последовательность труб](docs/ru/pipes.md)
- [Положение дефекта на трубе](docs/ru/defekt_location.md)
- [Глубина дефекта](docs/ru/defekt_depth.md)
- [Изменение диаметра трубопровода](docs/ru/diam.md)

## Разработка

```bash
git clone git@github.com:vb64/pipeline.csv.git
cd pipeline.csv
make setup PYTHON_BIN=/path/to/python3
make tests
```
