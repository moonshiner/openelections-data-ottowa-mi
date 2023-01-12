#!/usr/bin/env python

import os
from PyPDF2 import PdfReader, PdfWriter

def lsnames(outdir):
    files = []
    for file in os.listdir(outdir):
        if file.endswith('.pdf'):
            files.append(file)
    files.sort()
    return files

if __name__ == '__main__':
    files = lsnames("Ottowa")
    for f in files:
        print(f)
