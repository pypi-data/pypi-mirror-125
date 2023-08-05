import sys

from demo_reader_cahvs.multireader import MultiReader


filename = sys.argv[1]
r = MultiReader(filename)
print(r.read())
r.close()