#!/usr/bin/env python

# Take a directory of PDF files, and extract the text portions from them.

import os
import argparse
import csv
from PyPDF2 import PdfReader, PdfWriter

class TextData:
    def __init__(self):
        self.prev_xy = (0.0,0.0)
        self.textdata = []

    @staticmethod
    def mkof(filename, outdir):
        basen = os.path.basename(filename)
        fname = os.path.splitext(basen)[0]
        return f"{outdir}/{fname}.csv"

    def validpage(self):
        strchk = ("Straight Party Ticket",
            "Governor and Lieutenant Governor",
            "Secretary of State",
            "Attorney General",
            "Representative in Congress",
            "State Senator",
            "Representative in State Legislature")
        return next((True for l in self.textdata if l[2].startswith(strchk)), False)

    def write_details(self, filename):
        print(f"Writing: {filename}")
        with open(filename, "w", encoding="ascii") as csvfile:
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
        if cur_xy == (0.0, 0.0) and not text:
            return
        if cur_xy == self.prev_xy and not text:
            return
        self.details(cur_xy, text)

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('county', help="Name of County")
    parser.add_argument('inputdir', help="Directory of PDF Files")
    parser.add_argument('outputdir', help="Output Directory")
    parser.add_argument('--verbose', action='store_true', help="verbose")
    args = parser.parse_args()

    Files = []
    for file in os.listdir(args.inputdir):
        if file.endswith('.pdf'):
            Files.append(f"{args.inputdir}/{file}")
    Files.sort()
    Files = ["SplitPDFs/Ottawa/Ottawa-MI-precinctFile-210_page_0001.pdf"]
    for infile in Files or []:
        Line = TextData()
        # print(f"Reading: {infile}")
        reader = PdfReader(infile)
        page = reader.pages[0]
        page.extract_text(visitor_text=Line.visitor)
        # Does file have relevant races?
        if not Line.validpage():
            print(f"Skipping Not Relevant: {infile}")
            continue

        ofile = Line.mkof(infile, args.outputdir)
        Line.write_details(ofile)


if __name__ == '__main__':
    main()
