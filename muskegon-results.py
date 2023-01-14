#!/usr/bin/env python

import os
import csv
import argparse

# I was running them per page. A few things I've noticed

# DONE - I had the districts in these but appear to have dropped them in this batch.

# - Ottawa(and the rest of this format) count election day and absentee separate.

# DONE - Also in your example I don't see how you handle the under/over/rejected/unreseolved
# vote tallies. removed commetns

# - I have some mangled elected for school board (page 4 as an example). Have the code to drop it also
# just not turned on

# - Shorten Gov Candidate names

def log(verbose, logmsg):
    if verbose:
        print(logmsg)

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
    # print(f"Writing: {filename}")
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
        self.text = text
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

    def get_item(self, key):
        if key in self.race:
            return self.race.get(key)
        return None

    def set_item(self, key, value):
        if not value:
            print(f"NoValue {key} {value} {self.race.get(key)}")
        else:
            self.race[key] = value

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

    Parties = {
        "Democratic Party": "Democratic",
        "Green Party": "Green",
        "Libertarian Party": "Libertarian",
        "Natural Law Party": "Natural Law",
        "Republican Party": "Republican",
        "Straight Party Ticket": "Straight Party",
        "U.S. Taxpayers Party": "U.S. Taxpayers",
        "Working Class Party": "Working Class",
    }

    GovCandidates = {
        "Gretchen Whitmer Garlin D. Gilchrist II": "Gretchen Whitmer",
        "Tudor M. Dixon Shane Hernandez": "Tudor M. Dixon",
        "Mary Buzuma Brian Ellison": "Mary Buzuma",
        "Donna Brandenburg Mellissa Carone": "Donna Brandenburg",
        "Kevin Hogan Destiny Clayton": "Kevin Hogan",
        "Daryl M. Simpson Doug Dern": "Daryl M. Simpson"
    }

    def __init__(self, office, localrecord):
        # print(f"NewCandidate: '{office}' {len(localrecord)} Offices'{localrecord}'")
        self.candidate = {}
        if not localrecord:
            print("Candidate: empty record")
            return
        if localrecord[0] == "Choice":
            print(f"Skip Record {localrecord}")
            return
        self.office = office
        self.set_item("office", office)
        self.add_record(localrecord)

    def set_item(self, key, value):
        if not value:
            print(f"NoValue {key} {value} {self.candidate.get(key)}")
        else:
            self.candidate[key] = value

    def add_item(self, key, value):
        if key not in self.candidate:
            self.candidate[key] = value
        else:
            print(f"add_item: has key {key},{self.candidate.get(key)},{value}")

    def getdict(self):
        if self.candidate:
            return self.candidate
        return None

    def add_record(self, localrecord):
        ckeys = ['c_name', 'party', 'election_day', 'absentee', 'total']
        if not localrecord:
            return
        if ':' in localrecord[0]:
            cand = localrecord[0].replace(':', '')
            cand = cand.replace('write-in votes', '').rstrip()
            localrecord[0] = cand
        if self.office == "Straight Party":
            cand = localrecord[0].replace('Party', '').rstrip()
            localrecord[0] = cand
            if 'Party' in localrecord[1]:
                cpart = localrecord[1].replace('Party', '').rstrip()
                localrecord[1] = cpart
        if len(localrecord) == 5:
            self.candidate.update(dict(zip(ckeys, localrecord)))
        else:
            print(f"TOOSHORT {len(localrecord)} {localrecord}")

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
    LtGovs = (
        "Garlin D. Gilchrist II",
        "Shane Hernandez",
        "Brian Ellison",
        "Mellissa Carone",
        "Destiny Clayton",
        "Doug Dern"
    )

    def __init__(self, args, alldata):
        self.args = args
        self.county = args.county
        self.precinct = self.getPrecinct(alldata)
        self.office = None
        self.AllRaces = []

    def getPrecinct(self, alldata):
        for r in alldata or []:
            if 'Precinct ' in r[2]:
                # print(f"Precinct: {r}")
                return r[2]
        return None

    def isNewRace(self, text):
        ans = next((k for k in self.Offices if text.startswith(k)), None)
        if ans:
            self.office = self.Offices.get(ans)
        return ans

    def initRace(self, text):
        newrace = Race(text)
        newrace.set_item("county", self.county)
        newrace.set_item("precinct", self.precinct)
        self.office = newrace.get_item("office")
        # newrace.add_item("office", self.office)
        print(f"initrace {newrace.getdict()}")
        return newrace

    def parsefile(self, records):
        newcandidate = None
        localrecord = []
        shrec = records.pop(0)
        newrace = self.initRace(shrec[2])
        prevx = shrec[0]
        prevy = shrec[1]
        for r in records:
            print(r)
            curx, cury, text = r
            if text in self.LtGovs:
                print(f"Skip Lt Gov {text}")
                continue
            if 'Precinct ' in text:
                # Done
                # print("DONE", r, localrecord)
                if localrecord:
                    newcandidate = Candidate(self.office, localrecord)
                    if newcandidate:
                        newrace.add_candidate(newcandidate.getdict())
                # if newrace:
                self.AllRaces.append(newrace.getdict())
                # print(f"add_race {self.AllRaces}")
                return self.AllRaces
            if text.endswith('%'):
                # print(f"Skipping {text}")
                prevx = curx
                prevy = cury
                continue

            if prevx != curx and prevy != cury:
                # print(f"prevx != curx && prevy != cur: {prevx}, {curx} {prevy}, {cury} {text}")
                ans = self.isNewRace(text)
                if ans:
                    print("NEWRACE", ans, localrecord)
                    if localrecord:
                        newcandidate = Candidate(self.office, localrecord)
                        localrecord = []
                    if newrace:
                        if newcandidate:
                            newrace.add_candidate(newcandidate.getdict())
                        self.AllRaces.append(newrace.getdict())
                        # print(f"add_race {self.AllRaces}")
                    newrace = self.initRace(text)
                    localrecord.append(text)
                else:
                    print(f"{prevx},{prevy} {curx},{cury}")
                    print("NEW Candidate", text, localrecord)
                    if localrecord:
                        newcandidate = Candidate(self.office, localrecord)
                        if newcandidate:
                            newrace.add_candidate(newcandidate.getdict())
                        localrecord = []
                    localrecord.append(text)
                    if ':' in text or "(W)" in text:
                        localrecord.append("")

            elif prevx != curx:
                # print(f"prevx != curx: {prevx}, {curx}, '{text}'")
                localrecord.append(text)
                if ':' in text or "(W)" in text:
                    # print(f"colon: {text}")
                    localrecord.append("-")
            # elif prevy != cury:
                # print(f"prevy != cury: {prevy}, {cury}, '{text}'")
                # localrecord.append(text)
            else:
                # print(f"x/y equals {curx} {cury}")
                localrecord.append(text)
            prevx = curx
            prevy = cury
        return None


def printraces(filename, outputdir, races):
    basen = os.path.basename(filename)
    fname = os.path.splitext(basen)[0]
    ofile =  f"{outputdir}/{fname}.csv"
    # print(f"Output File: {ofile}")
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

    # Files = [
        # "PDFs2CSV/Muskegon/Muskegon-MI-Precinct-Results-11-18-2022-11-26-05-AM_202211181207249918_page_001.csv",
        # "Muskegon-MI-Precinct-Results-11-18-2022-11-26-05-AM_202211181207249918_page_002.csv",
        # "PDFs2CSV/Muskegon/Muskegon-MI-Precinct-Results-11-18-2022-11-26-05-AM_202211181207249918_page_003.csv",
    # ]
    Files = [f"{args.inputdir}/{file}" for file in os.listdir(args.inputdir)
             if file.endswith(".csv")]
    Files.sort()
    for infile in Files or []:
        records = readf(infile)
        print(infile)
        pageresults = PageData(args, records)
        races = pageresults.parsefile(list(records))
        printraces(infile, args.outputdir, races)

if __name__ == "__main__":
    main()
