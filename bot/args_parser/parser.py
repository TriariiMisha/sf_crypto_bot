import argparse

parser = argparse.ArgumentParser(description='Data collector')

parser.add_argument('-t', '--tickers', type=str, help='file with tickers')
parser.add_argument(
    '-d', '--duration', type=str, help='process duration in [int|float][d|h|m|s] format'
)
