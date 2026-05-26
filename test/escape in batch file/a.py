#!/usr/bin/env python3
import sys

print(f"Total: {len(sys.argv)} arguments\n")

for i, arg in enumerate(sys.argv):
    print(f"[{i}] {arg}")
