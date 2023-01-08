#!/usr/bin/env python

# Just takes the Ottowa-MI-precinctFile-210.pdf PDF
# and splits it up into single page PDFs.
# Also will skip the PDFs of localraces


from PyPDF2 import PdfReader, PdfWriter

def main(filename, outdir, skiplocal=True):
    race_types = [
        "Secretary of State",
        "Straight Party Ticket",
        "Governor and Lieutenant Governor",
        "State Senator"
    ]
    pdf = PdfReader(filename)
    numpages = len(pdf.pages)
    for page in range(numpages):
        if skiplocal:
            pgtext = pdf.pages[page].extract_text()
            if not any(race for race in race_types if race in pgtext):
                print(f"Skipping: Page {page}")
                continue

        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page])
        # zero pad the page numbers so they sort
        pgnum = f'{(page+1):04d}'
        output_filename = f'{outdir}/{filename}_page_{pgnum}.pdf'
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        print(f'Created: {output_filename}')

if __name__ == '__main__':
    main("Ottowa-MI-precinctFile-210.pdf", "OttowaPDFs")
