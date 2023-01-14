#!/usr/bin/env python

# Take a directory of PDF files, and extract the text portions from them.

import os
import argparse
import csv
from PyPDF2 import PdfReader, PdfWriter

class PDFText:
    Offices = ("Straight Party Ticket",
        "Governor and Lieutenant Governor",
        "Secretary of State",
        "Attorney General",
        "Representative in Congress",
        "State Senator",
        "Representative in State Legislature")

    def __init__(self, args):
        self.args = args
        self.prev_xy = (0.0,0.0)
        self.textdata = []

    def _log(self, logmsg):
        if self.args.verbose:
            print(logmsg)

    @staticmethod
    def mkof(filename, outdir):
        basen = os.path.basename(filename)
        fname = os.path.splitext(basen)[0]
        return f"{outdir}/{fname}.csv"

    def validpage(self):
        return next((True for l in self.textdata if l[2].startswith(self.Offices)), False)

    def writef(self, filename):
        self._log(f"Writing: {filename}")
        with open(filename, "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['x','y','text'])
            writer.writerows(self.textdata)

    def details(self, xy, text):
        if ',' in text:
            if len(text.split(' ')) == 1:
                text = text.replace(',', '')
        self.textdata.append([xy[0],xy[1],text])
        self.prev_xy = xy

    def visitor(self, text, cm, tm, fontDict, fontSize):
        text = text.replace('\n', '')
        cur_xy = (tm[4],tm[5])
        self._log(f"cur_xy={cur_xy[0]},{cur_xy[1]} prev_xy={self.prev_xy[0]},{self.prev_xy[1]}, '{text}'")
        if cur_xy == (0.0, 0.0) and not text:
            self._log("cur_xy == 0 and !text")
            # self.prev_xy = cur_xy
            return
        if cur_xy == self.prev_xy and not text:
            self._log("cur_xy == prev_xy and !text")
            # self.prev_xy = cur_xy
            return
        self.details(cur_xy, text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', help="Directory of PDF Files (SplitPDFs)")
    parser.add_argument('outputdir', help="Output CSV Directory (PDFs2CSV)")
    parser.add_argument('--writefiles', action='store_true', default=True, help="write files")
    parser.add_argument('--overwrite', action='store_true', help="overwrite files")
    parser.add_argument('--verbose', action='store_true', help="verbose")
    args = parser.parse_args()

    Files = [f"{args.inputdir}/{file}" for file in os.listdir(args.inputdir)
             if file.endswith(".pdf")]
    Files.sort()

    for infile in Files or []:
        Line = PDFText(args)
        reader = PdfReader(infile)
        page = reader.pages[0]
        page.extract_text(visitor_text=Line.visitor)
        # Does file have relevant races?
        if not Line.validpage():
            print(f"Skipping Not Relevant: {infile}")
            continue

        output_filename = Line.mkof(infile, args.outputdir)
        if os.path.exists(output_filename) and not args.overwrite:
            print(f'Will Not Overwrite: {output_filename}')
            continue
        if args.writefiles:
            Line.writef(output_filename)

if __name__ == '__main__':
    main()
