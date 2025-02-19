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
