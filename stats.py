#!/usr/bin/env python3

import argparse
import errno
import ctypes
import csv
import os
import sys


class Statistics:

    def __init__(self, mean, median, mode, rng, count):
        self.mean = mean
        self.median = median
        self.mode = mode
        self.rng = rng
        self.count = count

    def __str__(self):
        return 'Mean:\t{:.8f}\n'
        'Median:\t{:.8f}\n'
        'Mode:\t{:.8f}\n'
        'Range\t{:.8f}\n'
        'Count:\t{:,}'.format(
            self.mean, self.median, self.mode, self.rng, self.count)

# Load the libstats shared c library
LIBSTATSNAME = 'libstats.so.1'
_script_dir_name = os.path.dirname(os.path.realpath(__file__))
_libstats_loc = os.path.join(_script_dir_name, LIBSTATSNAME)
libstats = ctypes.CDLL(_libstats_loc, use_errno=True)

# Define C functions return types as c_double
libstats.mean.restype = ctypes.c_double
libstats.median.restype = ctypes.c_double
libstats.mode.restype = ctypes.c_double
libstats.range.restype = ctypes.c_double


def cli():
    '''Parse the command line settings and arguments'''
    parser = argparse.ArgumentParser(
        description='Print the mean, median, mode, and '
        'range of a comma separated list of numbers')
    parser.add_argument(
        '-f',
        '--file',
        help='The file containing the comma separated '
        'list of numbers, default is standard input')
    args = parser.parse_args()
    return args


def parse_csv_file(csvfile):
    '''A generator that returns all of the elements in the first row of'''
    '''the csv as floats'''
    reader = csv.reader(csvfile, delimiter=',')
    row = next(reader)
    for element in row:
        yield float(element)


def check_error(errcode):
    '''Check the errno and exit with message if the errno indicates error'''
    if errcode != 0:
        print('{}: {}'.format(
            errno.errorcode[errcode], os.strerror(errcode)), file=sys.stderr)
        sys.exit(1)


def calculate_statistics(numbers):
    '''Calculate the mean, median, mode, and range using the shared'''
    '''statistics library'''
    # Make the arr and arrlen values ctypes compatible
    arr = (ctypes.c_double * len(numbers))(*numbers)
    arrlen = ctypes.c_size_t(len(numbers))

    # Calculate and check errno after each call
    mean = libstats.mean(arr, arrlen)
    check_error(ctypes.get_errno())
    median = libstats.median(arr, arrlen)
    check_error(ctypes.get_errno())
    mode = libstats.mode(arr, arrlen)
    check_error(ctypes.get_errno())
    rng = libstats.range(arr, arrlen)
    check_error(ctypes.get_errno())

    stats = Statistics(
        mean=mean,
        median=median,
        mode=mode,
        rng=rng,
        count=len(numbers))

    return stats


def main():
    args = cli()

    csvfile = sys.stdin
    if args.file:
        csvfile = open(args.file, 'r')
    numbers = list(parse_csv_file(csvfile))
    csvfile.close()

    stats = calculate_statistics(numbers)

    print(stats)

if __name__ == '__main__':
    main()
