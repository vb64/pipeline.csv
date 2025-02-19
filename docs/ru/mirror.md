### Отзеркаливание данных

Загружаем данные из сохраненного файла.

```python
csv_copy = File.from_file('example.csv', 1000)
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
defect_row = csv_copy.data[3]
assert defect_row.is_defect

assert defect_row.orient_td == '7,00'
assert defect_row.orient_bd == '8,00'
```

Сохраняем перевернутую копию в файл.

```python
csv_file.to_file('reversed.csv')
assert os.path.getsize('reversed.csv') > 0
```
