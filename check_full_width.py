import fitz, unicodedata

def check_full_width(input_file:str, pages:list=None):
    comment_title = "Full-Width Highlighter"
    comment = "Found"
    output_file = input_file.split(".")[0] + " comments.pdf"
    # create matches dictionary for output summary
    results_summary = {}
    # open pdf
    pdfIn = fitz.open(input_file)
    # Iterate throughout pdf pages
    for pg,page in enumerate(pdfIn):
        pageID = pg+1
        # If required to look in specific pages
        if pages and pageID not in pages:
              continue

        # Get all the text in the page
        text = page.get_text("text")

        # Split the text by characters and check if each character is full-width
        for char in text:
            status = unicodedata.east_asian_width(char)
            full_status = ['W', 'F', 'A']
            if status in full_status:
                # Get the positions of full-width characters in the page
                start_idx = text.find(char)
                end_idx = start_idx + len(char)
                matches = page.search_for(text[start_idx:end_idx])
                if matches:
                    for match in matches:
                        annot = page.add_highlight_annot(match)
                        annot.update()
                # Update summary
                if char in results_summary:
                    results_summary[char][0] += 1
                else:
                    results_summary[char] = [1, status]

    print(results_summary)

    # Save to output file
    pdfIn.save(output_file,garbage=3,deflate=True)
    pdfIn.close()

check_full_width(input_file="Test Full Width.pdf")