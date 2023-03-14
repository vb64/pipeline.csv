# PipelineCsv library

[In Russian](READMEru.md)

The free, open source PipelineCsv library is designed to work with the results of analysis of in-line flaw detection data in the form of a CSV file.

The library provides a set of high-level operations with CSV file.

Data can be

-   mirrored
-   glued together from several CSV files
-   stretched/compressed along the distance according to a given set of intermediate points
-   interpreted as an iterable sequence of pipes with geodata

## Installation

```bash
pip install pipeline-csv
```

## Usage

It is necessary to define the sets of defects and markers used in your project.

```python
```
## Development

```
$ git clone git@github.com:vb64/pipeline.csv.git
$ cd pipeline.csv
$ make setup PYTHON_BIN=/path/to/python3
$ make tests
```
