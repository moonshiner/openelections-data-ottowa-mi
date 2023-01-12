#!/usr/bin/env python

# import csv

# "Choice Party Election Day Voting,Absentee Voting,Total"
# "Democratic Party ",
# "Republican Party ",
# "Libertarian Party ",
# "U.S. Taxpayers Party ",
# "Working Class Party ",
# "Green Party ",
# "Natural Law Party ",
# RaceTypes = [
#     "Secretary of State",
#     "Straight Party Ticket",
#     "Governor and Lieutenant Governor",
#     "State Senator"
# ]

CVTS = {
    "Choice Party Election Day Voting,Absentee Voting,Total": "Choice,Party,Election Day Voting,Absentee Voting,Total",
    "Democratic Party ": "Democratic Party,",
    "Green Party ": "Green Party,",
    "Libertarian Party ": "Libertarian Party,",
    "Natural Law Party ": "Natural Law Party,",
    "Republican Party ": "Republican Party,",
    "U.S. Taxpayers Party ": "U.S. Taxpayers Party,",
    "Working Class Party ": "Working Class Party,",
    " DEM ": ",DEM,",
    " GRE ": ",GRE,",
    " LIB ": ",LIB,",
    " NAL ": ",NAL,",
    " REP ": ",REP,",
    " UST ": ",UST,",
    " WC ": ",WC,",
    "% ": "%,",
    }

def chkparty(line):
    newline = line
    for k, v in CVTS.items():
        if k in newline:
            # print("MATCH", newline, k)
            newline = newline.replace(k, v)

    # if line == "Choice Party Election Day Voting,Absentee Voting,Total":
    #     print("LINE", line)
    #     newline = "Choice,Party,Election Day Voting,Absentee Voting,Total"
    #     return newline
    # for p in parties:
    #     psp = f"{p} "
    #     pc = f"{p},"
    #     if line.startswith(psp):
    #         newline = line.replace(psp, pc)
    #         print("PSP", newline)
    #         return newline
    return newline

def readf(filename):
    with open(filename, encoding="ascii") as f:
        # csvreader = csv.reader(f)
        # lines = list(csvreader)
        lines = f.readlines()
        lines = [l.rstrip() for l in lines or []]
        return lines

def main():
    records = readf("tabula-Ottowa-a.csv")
    for r in records:
        # print(r)
        newr = chkparty(r)
        print(newr)


if __name__ == "__main__":
    main()
