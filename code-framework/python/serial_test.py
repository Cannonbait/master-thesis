import sys
sys.path.append('../cython/')


import serial_framework
import pattern_designs


path = "../data-preparation/babesia-bovis/babesia_bovis_raw1.prep"

a = serial_framework.PySerialFramework(path)

bits = 10
patterns = 20
store = 10
blocks = 3
pat = pattern_designs.comp(bits, patterns, store, blocks)
print(a.test(pat, bits, store, blocks, 100))
