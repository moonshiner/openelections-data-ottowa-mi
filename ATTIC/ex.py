#!/usr/bin/env python

f=open("state-example.csv")
lines = f.readlines()
records = [l.rstrip('\n').split(',') for l in lines]
for r in records:
    print(f"{len(r)}, {r}")
