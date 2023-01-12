# openelections-data-ottowa-mi
Processing used in parsing Ottowa-MI election data

This repo works on parsing and processing the Ottowa MI election data.
This work uses data from
https://github.com/openelections/openelections-data-mi/issues/56

## Multiple Counties use this format

- Genesee
- Livingston
- Montcalm
- Muskegon
- Ottawa

The Ottowa MI data from 2022 General is 1438 Pages!
2/3 of the pages involve local races, which we ignore.

## Notes on processing the data

I always run Tabula initially to get a sense how messy the PDF source is.
Each Precient has four relevant pages:
    - Straight Party results
    - Governor/Lt. Gov
    - Secretary of State/Attorney General
    - Statehouse races.

One thing I noticed is Tabula could not parse the SoS/AG and Statehouse pages
cleanly.  For every precient.

### Splitting the PDF

splitpdf.py uses pyPDF2 to read in the PDF and write out each page as a
seperate file. Additionaly it has a check to see if the page contains
results for the relevanct races, and writes those only.



splitpdf.py         Takes a single PDF file and splits it into a dir of 1 page PDFs


pdfextract.py         Parse a single page PDF and extract the text (and poisitions
                    the page).  Write out the extract CSV file

getresults.py         Reads an extracted CSV file from above and generate the
                    Election Results CSV


###
