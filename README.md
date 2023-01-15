# openelections-data-ottowa-mi
Processing used in parsing Ottowa-MI election data

This repo works on parsing and processing the Ottowa MI election data.
This work uses data from
https://github.com/openelections/openelections-data-mi/issues/56

## Completed

Keweenaw-MI-totals.csv
Muskegon-MI-Totals.csv
Ottawa-MI-Totals.csv

## commands

splitpdf.py         Takes a single PDF file and splits it into a dir of 1 page PDFs


pdfextract.py         Parse a single page PDF and extract the text (and poisitions
                    the page).  Write out the extract CSV file

ottawa-results.py         Reads an extracted CSV file from above and generate the
                    Election Results CSV

muskegon-results.py


### Outstanding Issues


- I was running them per page. A few things I've noticed

- DONE - I had the districts in these but appear to have dropped them in this batch.

- Ottawa(and the rest of this format) count election day and absentee separate.

- Also in your example I don't see how you handle the under/over/rejected/unreseolved
 vote tallies.

- DONE I have some mangled elected for school board (page 4 as an example). Have the code to drop it also
 just not turned on

- DONE Shorten Gov Candidate names


