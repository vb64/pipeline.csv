### Docking new data and compression/stretching

Append to initial CSV empty pipe with length 10.0 m and reversed copy from the file.

```python
csv_file.join([10000, 'reversed.csv'])
assert csv_file.total_length == 28000
assert len(csv_file.data) == 11
```

Compress distances and length of all objects in half.

```python
csv_file.dist_modify(
  # table of corrections
  # each node define as pair 'existing distance', 'new distance'
  [[0, 0],
  [28000, 14000],
])
assert csv_file.total_length == 14000
```

Save file with compress distances.

```python
csv_file.to_file('transformed.csv')
assert os.path.getsize('transformed.csv') > 0
```
