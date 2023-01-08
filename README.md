# openelections-data-ottowa-mi
Processing used in parsing Ottowa-MI election data

This repo works on parsing and processing the Ottowa MI election data.
This work uses data from https://github.com/openelections/openelections-data-mi/issues/56

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

