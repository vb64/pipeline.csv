### Data mirroring

Create copy from saved file.

```python
csv_copy = File.from_file('example.csv', 1000)
```

Check distance of the last object in copy and defect orientation.

```python
assert csv_copy.total_length == 12000
assert len(csv_copy.data) == 6

defect_row = csv_copy.data[4]
assert defect_row.is_defect
assert defect_row.orient_td == '4,00'
assert defect_row.orient_bd == '5,00'
```

Reverse copy.

```python
csv_copy.reverse()
```

Relative position of defekt must change and defect orientation must be mirrored.

```python
defect_row = csv_copy.data[3]
assert defect_row.is_defect

assert defect_row.orient_td == '7,00'
assert defect_row.orient_bd == '8,00'
```

Save reversed copy to file.

```python
csv_file.to_file('reversed.csv')
assert os.path.getsize('reversed.csv') > 0
```
