import bz2
from demo_reader_cahvs.util import writer


opener = bz2.open


if __name__ == '__main__':
    writer.main(opener)