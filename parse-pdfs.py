#!/usr/bin/env python

import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

def lsnames(outdir):
    files = []
    for file in os.listdir(outdir):
        if file.endswith('.pdf'):
            files.append(file)
    files.sort()
    return files

class CurLine:
    # This is based on some code snippet in pypdf2 doc and
    # i find this horrible

    array = []
    parts = []
    oldy = 0.0
    precient = None
    def addprecient(self, ntext):
        if not self.precient:
            self.precient = ntext
    def addline(self, text):
        self.array.append(text)
    def addparts(self):
        if self.array:
            # print("cur", self.array)
            self.parts.append(self.array)
            # self.prparts()
            self.array = []
            # print("mpw", self.array)

    def getparts(self):
        return self.parts
    def prparts(self):
        print(f"{self.parts}")
    def visitor_body(self, text, cm, tm, fontDict, fontSize):
        y = tm[5]
        ntext = text.rstrip('\n')
        # print(f"{y}, {self.oldy}, '{ntext}'")

        if y > 165:
            # print(f"skipping, y={y} '{ntext}'")
            return
        # if 'Precinct' in ntext:
        #     print(f"NTEXT {ntext} {y}, {self.oldy}")
        if y != self.oldy:
            # print(f"mismatch {y} {self.oldy} {self.array}")
            if cm == tm:
                # print("Mismatch skip CM TM")
                return
            self.addparts()
        # else:
            # print(f"MATCH {y} {self.oldy} {self.array}")
        if cm == tm:
            # print("SKIP CM TM")
            return
        self.oldy = y
        if ntext:
            self.addline(ntext)

def getraces(orecords):
    office_types = [
        "Straight Party Ticket",
        "Governor and Lieutenant Governor",
        "Secretary of State",
        "Attorney General",
        "Representative in",
        "State Senator"
    ]
    Races = []
    newrace = []
    for r in orecords or []:
        if 'Vote for' in r[0]:
            if newrace:
                if not any(office for office in office_types if office in newrace[0][0]):
                    print(f"SKIPPING Race {newrace[0][0]}")
                else:
                    print(f"SAVING Race {newrace[0][0]}")
                    Races.append(newrace)

            newrace = [r]
        else:
            newrace.append(r)
    if newrace:
        if not any(office for office in office_types if office in newrace[0][0]):
            print(f"SKIPPING Race {newrace[0][0]}")
        else:
            print(f"SAVING Race {newrace[0][0]}")
            Races.append(newrace)

    for race in Races or []:
        for r in race:
            print(f"{','.join(r)}")
        print(",,,,")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pdfdirectory', nargs='?', default="OttowaPDFs")
    parser.add_argument('--filename', type=str, help="process one file")
    parser.add_argument('--writecsv', action='store_true', help="write csv")
    args = parser.parse_args()
    print(args)
    filename = "Ottowa-MI-precinctFile-210.pdf_page_0004.pdf"

    Line = CurLine()

    reader = PdfReader(f"OttowaPDFs/{filename}")
    rpage = reader.pages[0]
    rpage.extract_text(visitor_text=Line.visitor_body)
    records = Line.getparts()
    getraces(records)



if __name__ == '__main__':
    main()
