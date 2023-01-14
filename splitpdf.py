#!/usr/bin/env python

# Reads in a PDF file,
import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

def splitpdfs(args):
    if "SplitPDFs" not in args.outputdir:
        OutputPath = f"SplitPDFs/{args.outputdir}"
    else:
        OutputPath = f"{args.outputdir}"
    fname = os.path.splitext(os.path.basename(args.inputfile))[0]
    pdf = PdfReader(args.inputfile)
    numpages = len(pdf.pages)
    fillsize = len(str(numpages))
    for page in range(numpages):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page])
        pgnum = f'{(page+1):0{fillsize}d}'
        output_filename = f'{OutputPath}/{fname}_page_{pgnum}.pdf'
        if os.path.exists(output_filename) and not args.overwrite:
            print(f'Will Not Overwrite: {output_filename}')
            continue
        if args.writefiles:
            # print(f'Created: {output_filename}')
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)

def main():
    parser = argparse.ArgumentParser(description="Split a PDF into 1 page files")
    parser.add_argument('inputfile', help="Input PDF")
    parser.add_argument('outputdir', help="Output Directory (usually SplitPDFs/County)")
    parser.add_argument('--writefiles', action='store_true', default=True, help="write files")
    parser.add_argument('--overwrite', action='store_true', help="overwrite files")
    parser.add_argument('--verbose', action='store_true', help="verbose")
    args = parser.parse_args()
    splitpdfs(args)

if __name__ == '__main__':
    main()
