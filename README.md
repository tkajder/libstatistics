# libstatistics

Calculates the mean, median, mode, and range of a list of numbers.

This project is a simple exploration of the `ctypes` module of python.

This project was developed on and for a debian jessie system with python3.

To compile the shared library:

```bash
make
```

The `stats.py` file takes in a comma separated list of numbers and calculates their simple statistics.
The file can either be run reading from standard input or a file:

```bash
# From standard input
./stats.py
9,5,3,5,1,7

# From file
./stats.py -f example.csv
```
