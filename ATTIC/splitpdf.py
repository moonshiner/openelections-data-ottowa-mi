#!/usr/bin/env python

# Just takes the Ottowa-MI-precinctFile-210.pdf PDF
# and splits it up into single page PDFs.
# Also will skip the PDFs of localraces

import os
import argparse

from PyPDF2 import PdfReader, PdfWriter

def splitpdf(args):
    fname = os.path.splitext(os.path.basename(args.inputfile))[0]
    filename = f"InputFiles/{args.inputfile}"
    pdf = PdfReader(filename)
    numpages = len(pdf.pages)
    fillsize = len(str(numpages))
    for page in range(numpages):
        # zero pad the page numbers so they sort
        pgnum = f'{(page+1):0{fillsize}d}'
        output_filename = f'SplitPDFs/{args.county}/{fname}_page_{pgnum}.pdf'
        if os.path.exists(output_filename) and not args.overwrite:
            continue
        print(f'Creating: {output_filename}')
        if args.writefiles:
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf.pages[page])
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('county', help="Name of County")
    parser.add_argument('inputfile', help="Input PDF")
    parser.add_argument('--writefiles', action='store_true', help="write pdfs")
    parser.add_argument('--overwrite', action='store_true', help="overwrite pdf")
    parser.add_argument('--verbose', action='store_true', help="verbose")
    parser.add_argument('--skiplocal', action='store_true', help="Skip Local Races")
    args = parser.parse_args()
    splitpdf(args)

if __name__ == '__main__':
    main()
