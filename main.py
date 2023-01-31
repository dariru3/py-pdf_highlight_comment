def comment_pdf(input_file:str, list_filename_csv:str, output_file:str, pages:list=None):
    import fitz, csv
    comment_title = "Python Highlighter"
    colors = {
        "red": [0.7, 0.35, 0.5],
        "green": [0.35, 0.7, 0.5],
        "blue": [0.35, 0.5, 0.7]
    }
    """
    Search for a particular string value in a PDF file and add comments to it.
    """
    with open(list_filename_csv, 'r') as csv_data:
        csv_reader = csv.reader(csv_data)
        header = next(csv_reader) # skips the first row
        search_list = [row for row in csv_reader]

    pdfIn = fitz.open(input_file)
    
    # create matches dictionary for output summary
    matches = {}
    for search in search_list:
        matches[search[0]] = 0
    
    # Iterate throughout the document pages
    for pg,page in enumerate(pdfIn):
        pageID = pg+1
        # If required for specific pages
        if pages:
           if pageID not in pages:
              continue

        # Use the search_for function to find the text
        for search in search_list:
            word = search[0]
            comment = search[1]
            color = search[2]

            matched_values = page.search_for(word,hit_max=20)
            # found_matches += len(matched_values) if matched_values else 0
            if(matched_values):
                matches[word] += len(matched_values)

                #Loop through the matches values
                #item will contain the coordinates of the found text
                for item in matched_values:
                    # Highlight found text
                    annot = page.add_highlight_annot(item)
                    if color:
                        annot.set_colors(stroke=colors[color])

                    # Add comment to the found match
                    info = annot.info
                    info["title"] = comment_title
                    info["content"] = comment
                    annot.set_info(info)

                    annot.update()

    #Save to output file
    pdfIn.save(output_file,garbage=3,deflate=True)
    pdfIn.close()

    #Process Summary
    summary = {
         "Input File": input_file
        , "Output File": output_file
        , "Comment Title": comment_title
        , "Matching Instances": "\n" + "\n".join("{}: {}".format(word, count) for word, count in matches.items())
    }

    # Export Process Summary
    with open('summary.txt', 'w') as summary_txt:
        summary_txt.write("\n".join("{}: {}".format(i, j) for i, j in summary.items()))

comment_pdf(input_file="final_test_2022.pdf"
            , list_filename_csv="Sample Glossary for Daryl.csv"
            , output_file="final_test_2022 comments.pdf"
            )