#!/usr/bin/env python
# county,precinct,office,district,party,candidate,votes
# state: 99
# sen 36
# house 1
import json
import csv

def readj(filename):
    with open(filename, encoding="ascii") as f:
        allf = json.load(f)
        return allf

def readf(filename):
    with open(filename, encoding="ascii") as f:
        csvreader = csv.reader(f)
        lines = list(csvreader)
        # header = lines.pop(0)
        return lines

def writef(filename, records):
    # print(f"Writing: {filename}")
    with open(filename, "w", newline='', encoding="ascii") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(records)

# county,precinct,office,district,candidate,party,election_day,absentee,total
#

SecOfState = {
    "DEM": "Jocelyn Benson",
    "REP": "Kristina Elaine Karamo",
    "LIB": "Gregory Scott Stempfle",
    "UST": "Christine C. Schwartz",
    "GRN": "Larry James Hutchinson Jr.",
    "Total": "Total",
    "Unresolved": "Unresolved Write-In"
}

AG = {
    "DEM":  "Dana Nessel",
    "REP":  "Matthew DePerno",
    "LIB": "Joseph W. McHugh Jr.",
    "UST": "Gerald T. Van Sickle",
    "Total": "Total",
    "Unresolved": "Unresolved Write-In"
}

Races = {
    "AG": "Attorney General",
    "SoS": "Secretary of State",
    "Governor": "Governor",
    "Straight": "Straight Party",
    "StateHouse48": "State House",
    "StateHouse49": "State House",
    "StateHouse50": "State House",
    "StateHouse72": "State House",
    "StateSenate37": "State Senate",
    "USHouse7": "U.S. House",
}

Districts = {
    "StateHouse48": "48",
    "StateHouse49": "49",
    "StateHouse50": "50",
    "StateHouse72": "72",
    "StateSenate37": "37",
    "USHouse7": "7",
}

Party = {
    "DEM": "Democratic Party",
    "REP": "Republican Party",
    "LIB": "Libertarian Party",
    "UST": "U.S. Taxpayers",
    "WCP": "Working Class Party",
    "GRN": "Green Party",
    "NLP": "Natural Law Party",
    # "Total": "Total",
    # "Unresolved": "Unresolved Write-In"
}

MiscData = {
    "Cast Votes": "Cast Votes",
    "Undervotes": "Undervotes",
    "Overvotes": "Overvotes",
    "Rejected write-in votes": "Rejected",
    "Unassigned write-ins": "Unassigned",
    "Absentee Ballots Cast": "Absentee",
    "Precinct Ballots Cast": "Election",
    "Total Ballots Cast": "Total"
}

allcandidates = readj("Livingston-Candidates.json")
allfiles = readj("Livingston-Files.json")

# def parsestraight():
#     lines = readf("straight.csv")
#     header = lines.pop(0)
# "GRN"
#     outputs = []
#     outputs.append(["county","precinct","office","district","party","candidate","votes"])
#     # print(header)
#     for l in lines or []:
#         record = dict(zip(header, l))
#         # print(record)
#         for p in Party:
#             if p in record:
#                 outputs.append(["Mackinac", l[0], "Straight Ticket", "", p, Party.get(p), record.get(p)])

#     writef("makinac-straight.csv", outputs)

def getprecincts(race, records):
    precincts = []
    precinct = []
    for r in records or []:
        if "Precinct" in r and len(precinct) > 0:
            if len(race) > len(precinct):
                print(f"HERE {len(race)} {len(precinct)}")
                # pop off extra
                precinct.pop()
            pdict = dict(zip(race, precinct))
            precincts.append(pdict)
            precinct = []
        precinct.append(r)
    pdict = dict(zip(race, precinct))
    precincts.append(pdict)
    return precincts

def printresults(race, allcands, precincts):
    # allcands = list(Gov.values())
    orecords = []
    orecords.append(["county","precinct","office","district","party","candidate","votes"])
    office = Races.get(race)
    district = Districts.get(race, '')
    for precinctd in precincts:
        if not precinctd:
            continue
        # print(precinctd)
        precinct = precinctd.pop("Precinct")
        for k, v in precinctd.items():
            if k in allcands:
                if ',' in k:
                    cand, party = k.split(',')
                    party = party.strip()
                    # print(f"\"{cand}\" \"{party}\"")
                else:
                    print("NO ,", k)
            else:
                cand = k
                party = ""
            orecords.append(["Livingston" ,precinct, office, district, party, cand, v])
    writef(f"Livingston-{race}-Totals.csv", orecords)

def parsestv():
    race = "Straight"
    Files = allfiles.get(race)
    allcands = allcandidates.get(race)
    precincts = []
    allrecords = []
    for filename in Files or []:
        print(filename)
        lines = readf(filename)
        lines.pop(0)
        # lines.pop(0) # pop off first '19.008', '-204.67700000000002', 'Precinct'
        lines = [l for l in lines or [] if l[2]]
        records = []
        candidates = {}
        candidates.setdefault(race, []).append("Precinct")
        prevx = None
        for l in lines:
            if l[0] == '19.008' and prevx == l[0]:
                records[-1] += l[2]
            elif l[2].startswith("Livingston County"):
                break
            elif l[2] in ["Registered Voters ", "Turnout Percentage ", "Precinct", "GRN "]:
                continue
            elif "%" in l[2] or "Percentage" in l[2]:
                continue
            else:
                l[2] = l[2].rstrip(" ")
                if MiscData.get(l[2]):
                    l[2] = MiscData.get(l[2])
                    candidates.setdefault(race, []).append(l[2])
                elif l[2] in allcands:
                    candidates.setdefault(race, []).append(l[2])
                else:
                    records.append(l[2])
            prevx = l[0]
        # print(candidates)
        # print(records)
        precincts = getprecincts(candidates.get(race), records)
        allrecords.extend(precincts)
        # print(precincts)

    printresults(race, allcands, allrecords)

def parsesos():
    race = "SoS"
    Files = allfiles.get(race)
    allcands = allcandidates.get(race)
    precincts = []
    allrecords = []
    for filename in Files or []:
        # print(filename)
        lines = readf(filename)
        lines.pop(0)
        # lines.pop(0) # pop off first '19.008', '-204.67700000000002', 'Precinct'
        lines = [l for l in lines or [] if l[2]]
        records = []
        candidates = {}
        candidates.setdefault(race, []).append("Precinct")
        prevx = None
        for l in lines:
            if l[0] == '19.008' and prevx == l[0]:
                records[-1] += l[2]
            elif l[2].startswith("Livingston County"):
                break
            elif l[2] in ["Registered Voters ", "Turnout Percentage ", "Precinct", "GRN "]:
                continue
            elif "%" in l[2] or "Percentage" in l[2]:
                continue
            else:
                l[2] = l[2].rstrip(" ")
                if MiscData.get(l[2]):
                    l[2] = MiscData.get(l[2])
                    candidates.setdefault(race, []).append(l[2])
                elif l[2] == "Larry James Hutchinson Jr.,":
                    candidates.setdefault(race, []).append(f"{l[2]} GRN")
                elif l[2] in allcands:
                    candidates.setdefault(race, []).append(l[2])
                else:
                    records.append(l[2])
            prevx = l[0]

        precincts = getprecincts(candidates.get(race), records)
        allrecords.extend(precincts)

    printresults(race, allcands, allrecords)

def parsegov():
    Gov = {
        "Bob Scott (W)": "Bob Scott, W",
        "Daryl M. Simpson Doug Dern,": "Daryl M. Simpson, NLP",
        "Donna Brandenburg Mellissa": "Donna Brandenburg, UST",
        "Elizabeth Ann Adkisson (W)": "Elizabeth Ann Adkisson, W",
        "Ervin Joseph Lamie (W)": "Ervin Joseph Lamie, W",
        "Eugene Rosell Hunt Jr. (W)": "Eugene Rosell Hunt Jr., W",
        "Evan S. Space (W)": "Evan S. Space, W",
        "Gretchen Whitmer Garlin D.": "Gretchen Whitmer, DEM",
        "Joseph Irving (W)": "Joseph Irving, W",
        "Joseph Michael Hunt (W)": "Joseph Michael Hunt, W",
        "Joyce Priscilla Gipson (W)": "Joyce Priscilla Gipson, W",
        "Justin Paul Backburn (W)": "Justin Paul Backburn, W",
        "Kevin Hogan Destiny Clayton,": "Kevin Hogan, GRN",
        "Mary Buzuma Brian Ellison, LIB": "Mary Buzuma, LIB",
        "Michael David Kelley (W)": "Michael David Kelley, W",
        "Tudor M. Dixon Shane": "Tudor M. Dixon, REP",
        "Michael Ray Deck (W)": "Michael Ray Deck, W"
    }
    race = "Governor"
    Files = allfiles.get(race)
    precincts = []
    allrecords = []
    for filename in Files or []:
        lines = readf(filename)
        lines.pop(0)
        lines.pop(0) # pop off first '19.008', '-204.67700000000002', 'Precinct'
        lines = [l for l in lines or [] if l[2]]
        records = []
        candidates = {}
        candidates.setdefault(race, []).append("Precinct")
        prevx = None
        for l in lines:
            if l[0] == '19.008' and prevx == l[0]:
                records[-1] += l[2]
            elif l[2] in ["Gilchrist II, DEM ", "Hernandez, REP ", "Carone, UST ", "GRN ", "NLP "]:
                continue
            elif l[2].startswith("Livingston County"):
                break
            elif l[2] in ["Registered Voters ", "Turnout Percentage "]:
                continue
            elif "%" in l[2] or "Percentage" in l[2]:
                continue
            else:
                l[2] = l[2].rstrip(" ")
                if MiscData.get(l[2]):
                    l[2] = MiscData.get(l[2])
                    candidates.setdefault(race, []).append(l[2])
                elif l[2] in Gov:
                    candidates.setdefault(race, []).append(Gov.get(l[2]))
                else:
                    if "(W)" in l[2]:
                        print(f"MISSING: {l[2]}")
                    records.append(l[2])
            prevx = l[0]
        precincts = getprecincts(candidates.get(race), records)
        allrecords.extend(precincts)
        # print(precincts)

    allcands = list(Gov.values())
    printresults(race, allcands, allrecords)

# readnewf - reads one CSV file, pulls out the race info
#  returns a list of precinct totals
# Will not work for Governor, SoS, or Straight Ticket
#
def readresults(race, filename):
    allcands = allcandidates.get(race)
    lines = readf(filename)
    lines.pop(0)
    lines.pop(0) # pop off first '19.008', '-204.67700000000002', 'Precinct'
    lines = [l for l in lines or [] if l[2]]

    candidates = {}
    candidates.setdefault(race, []).append("Precinct")
    records = []
    for l in lines:
        if l[0] == '19.008' and prevx == l[0]:
            records[-1] += l[2]
        elif l[2].startswith("Livingston County"):
            break
        # skip Percentages
        elif l[2] in ["Registered Voters ", "Turnout Percentage "]:
            continue
        elif "%" in l[2] or "Percentage" in l[2]:
            continue
        else:
            l[2] = l[2].rstrip(" ")
            if MiscData.get(l[2]):
                l[2] = MiscData.get(l[2])
                candidates.setdefault(race, []).append(l[2])
            elif l[2] in allcands:
                candidates.setdefault(race, []).append(l[2])
            else:
                records.append(l[2])
        prevx = l[0]

    racec = candidates.get(race)
    # precincts = getprecincts(racec, records)
    print(racec)
    precincts = []
    precinct = []
    for r in records or []:
        if "Precinct" in r and precinct:
            precinct.pop()
            pdict = dict(zip(racec, precinct))
            precincts.append(pdict)
            precinct = []
        precinct.append(r)
    pdict = dict(zip(racec, precinct))
    precincts.append(pdict)
    return precincts

#     outputs.append(["county","precinct","office","district","party","candidate","votes"])
# parsefiles - take all the CSV files for a specific race, process them, and
# returns
def parsefiles(race, Files):
    print(race)
    records = []
    for file in Files or []:
        precincts = readresults(race, file)
        records.extend(precincts)

    allcands = allcandidates.get(race)
    printresults(race, allcands, records)

def main():
    parsestv()
    # parsesos()
    # parsegov()
    # for race in ["USHouse7", "StateSenate37", "StateHouse48", "StateHouse49", "StateHouse50",
    #     "StateHouse71", "AG"]:
    #     Files = allfiles.get(race)
    #     parsefiles(race, Files)

if __name__ == "__main__":
    main()
