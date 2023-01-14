#!/usr/bin/env python

import os
import csv
import argparse

# I was running them per page. A few things I've noticed

# DONE - I had the districts in these but appear to have dropped them in this batch.

# - Ottawa(and the rest of this format) count election day and absentee separate.

# DONE Also in your example I don't see how you handle the under/over/rejected/unreseolved
# vote tallies.

# - I have some mangled elected for school board (page 4 as an example). Have the code to drop it also
# just not turned on

# - Shorten Gov Candidate names

AllOffices = {
    "Straight Party Ticket": "Straight Party",
    "Governor and Lieutenant Governor":  "Governor",
    "Secretary of State": "Secretary of State",
    "Attorney General": "Attorney General",
    "Representative in Congress": "U.S. House",
    "State Senator": "State Senate",
    "Representative in State Legislature": "State House"
}

def isRace(text):
    return next((True for k in AllOffices if text.startswith(k)), False)

def shortRace(text):
    return next((v for k,v in AllOffices.items() if text.startswith(k)), None)

def readf(filename):
    with open(filename, encoding="ascii") as csvf:
        csvreader = csv.reader(csvf)
        lines = list(csvreader)
        lines.pop(0)
        return lines

def writef(filename, records):
    print(f"Writing: {filename}")
    with open(filename, "w", encoding="ascii") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(records)

class Race:
    Offices = {
        "Straight Party Ticket": "Straight Party",
        "Governor and Lieutenant Governor":  "Governor",
        "Secretary of State": "Secretary of State",
        "Attorney General": "Attorney General",
        "Representative in Congress": "U.S. House",
        "State Senator": "State Senate",
        "Representative in State Legislature": "State House"
    }
    ShortDistricts = ["U.S. House", "State House", "State Senate"]

    DistrictRaces = [
        "Representative in Congress",
        "State Senator",
        "Representative in State Legislature",
    ]

    def __init__(self, text):
        self.race = {}
        self.district = None
        self.office = self._shortOffice(text)
        if self.office in self.ShortDistricts:
            self.district = self._getDistrict(text)

    def _getDistrict(self, text):
        district = None
        ans = next((d for d in self.DistrictRaces if text.startswith(d)), None)
        if ans:
            fields = text.replace(ans, '').split()
            district = ''.join(list(fields[0])[:-2])
            # print(f"ZZ, '{text}',  '{ans}' {fields} '{district}'")
            self.add_item("district", district)
        return district

    def _shortOffice(self, text):
        # If exists return the shortened versuion
        ans = next((v for k,v in self.Offices.items() if text.startswith(k)), None)
        if ans:
            self.add_item("office", ans)
        return ans

    def add_item(self, key, value):
        if key not in self.race:
            self.race[key] = value
        else:
            print(f"add_item: has key {key},{self.race.get(key)},{value}")

    def add_candidate(self, crecord):
        if not crecord:
            print("empty record")
        else:
            self.race.setdefault("candidates", []).append(crecord)
        # print("add_candidate", self.getdict())

    def getdict(self):
        return self.race

class Candidate:
    # candidate, party, votes, office

    GovCandidates = {
        "Gretchen Whitmer Garlin D. Gilchrist II": "Gretchen Whitmer",
        "Tudor M. Dixon Shane Hernandez": "Tudor M. Dixon",
        "Mary Buzuma Brian Ellison": "Mary Buzuma",
        "Donna Brandenburg Mellissa Carone": "Donna Brandenburg",
        "Kevin Hogan Destiny Clayton": "Kevin Hogan",
        "Daryl M. Simpson Doug Dern": "Daryl M. Simpson"
    }

    def __init__(self, office, localrecord):
        # print(f"NewCandidate: '{office}' {len(localrecord)} '{localrecord}'")
        if not localrecord:
            print("Candidate: empty record")
            return
        self.candidate = {}
        self.add_item("office", office)
        self.add_record(localrecord)

    def add_item(self, key, value):
        if key not in self.candidate:
            self.candidate[key] = value
        else:
            print(f"add_item: has key {key},{self.candidate.get(key)},{value}")
        # print(self.candidate)

    def getdict(self):
        return self.candidate

    def add_record(self, localrecord):
        ckeys = ['c_name', 'party', 'election_day', 'absentee', 'total']
        if not localrecord:
            return
        if len(localrecord) == 5:
            self.candidate.update(dict(zip(ckeys, localrecord)))
        # else:
            # print(f"TOOSHORT {len(localrecord)} {localrecord}")
        # print("add_record", self.candidate)

class PageData:
    # DistrictRaces = [
    #     "Representative in Congress",
    #     "State Senator",
    #     "Representative in State Legislature",
    # ]
    Offices = {
        "Straight Party Ticket": "Straight Party",
        "Governor and Lieutenant Governor":  "Governor",
        "Secretary of State": "Secretary of State",
        "Attorney General": "Attorney General",
        "Representative in Congress": "U.S. House",
        "State Senator": "State Senate",
        "Representative in State Legislature": "State House"
    }

    Skips = [
        "Choice",
        "Party",
        "Election Day Voting",
        "Absentee Voting",
        "Total",
    ]
    def __init__(self, args, alldata):
        self.args = args
        self.county = args.county
        self.precinct = self.getPrecinct(alldata)
        self.office = None
        self.AllRaces = []

    def getPrecinct(self, alldata):
        for r in alldata or []:
            if 'Precinct' in r[2]:
                # print(f"Precinct: {r}")
                return r[2]
        return None

    def getDistrict(self, text, ans):
        print(f"getDistrict: '{text}', '{ans}'")
        district = ""
        if ans in self.DistrictRaces:
            fields = text.replace(ans, '').split()
            district = ''.join(list(fields[0])[:-2])
            # print(f"FOUNDDISTRICT '{text}'  {district}")
            self.district = district
        return district

    def isNewRace(self, text):
        ans = next((k for k in self.Offices if text.startswith(k)), None)
        if ans:
            self.office = self.Offices.get(ans)
        return ans

    def parsefile(self, records):
        if not self.precinct:
            self.precinct = self.getPrecinct(records)
        prevx = 0.0
        prevy = 0.0
        # office = None
        newcandidate = None
        newrace = None
        localrecord = []
        for r in records:
            curx, cury, text = r
            if 'Precinct' in text:
                # Done
                if localrecord:
                    newcandidate = Candidate(self.office, localrecord)
                    newrace.add_candidate(newcandidate.getdict())
                self.AllRaces.append(newrace.getdict())
                # print(f"add_race {self.AllRaces}")
                # print("DONE", self.AllRaces)
                return self.AllRaces
            if text in self.Skips or text.endswith('%'):
                # print(f"Skipping {text}")
                prevx = curx
                prevy = cury
                continue

            if prevx != curx and prevy != cury:
                # print(f"prevx != curx && prevy != cur: {prevx}, {curx} {prevy}, {cury} {text}")
                ans = self.isNewRace(text)
                if ans:
                    # print("NEWRACE", ans, localrecord)
                    if localrecord:
                        newcandidate = Candidate(self.office, localrecord)
                        localrecord = []
                    if newrace:
                        newrace.add_candidate(newcandidate.getdict())
                        self.AllRaces.append(newrace.getdict())
                        # print(f"add_race {self.AllRaces}")
                    newrace = Race()
                    newrace.add_item("county", self.county)
                    newrace.add_item("precinct", self.precinct)
                    newrace.add_item("office", self.office)
                    district = self.getDistrict(text, ans)
                    newrace.add_item("district", district)
                    # print(f"newrace {newrace.getdict()}")
                else:
                    # print("NEW Candidate", text)
                    if localrecord:
                        newcandidate = Candidate(self.office, localrecord)
                        # print("proces record", localrecord)
                        newrace.add_candidate(newcandidate.getdict())
                        localrecord = []
                    localrecord.append(text)
                    if ':' in text or "(W)" in text:
                        localrecord.append("")
                        # print("append", text, localrecord)

            elif prevx != curx:
                # print(f"prevx != curx: {prevx}, {curx}, '{text}'")
                localrecord.append(text)
                if ':' in text or "(W)" in text:
                    localrecord.append("-")

            # elif prevy != cury:
            #     print(f"prevy != cur: {prevy}, {cury}, '{text}'")
            # else:
            #     print(f"x/y equals {curx} {cury}")
            prevx = curx
            prevy = cury
        return None


def printraces(filename, outputdir, races):
    basen = os.path.basename(filename)
    fname = os.path.splitext(basen)[0]
    ofile =  f"{outputdir}/{fname}.csv"
    print(f"Output File: {ofile}")
    ckeys = ['c_name', 'party', 'election_day', 'absentee', 'total']
    orecords = [['county','precinct','office','district','candidate','party',
        'election_day', 'absentee', 'total']]
    for r in races:
        curr = [r.get('county'), r.get('precinct'), r.get('office'), r.get('district')]
        for candidate in r.get('candidates') or []:
            orecords.append((curr + [candidate.get(ck) for ck in ckeys or []]))

    writef(ofile, orecords)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('county', help="Name of County")
    parser.add_argument('inputdir', help="Input CSV Directory (PDFs2CSV)")
    parser.add_argument('outputdir', help="Output Parsed Results Directory (ParsedData)")
    parser.add_argument('--writefiles', action='store_true', default=True, help="write files")
    parser.add_argument('--overwrite', action='store_true', help="overwrite file")
    parser.add_argument('--verbose', action='store_true', help="verbose")
    args = parser.parse_args()

    Files = [f"{args.inputdir}/{file}" for file in os.listdir(args.inputdir)
             if file.endswith(".csv")]
    Files.sort()
    for infile in Files or []:
        records = readf(infile)
        pageresults = PageData(args, records)
        races = pageresults.parsefile(list(records))
        printraces(infile, args.outputdir, races)

if __name__ == "__main__":
    main()
