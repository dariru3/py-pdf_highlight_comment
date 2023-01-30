def comment_pdf(input_file:str
              , search_list:list
              , comment_title:str
              , output_file:str
              , pages:list=None
              ):
    import fitz
    colors = {
        "red": [0.7, 0.35, 0.5],
        "green": [0.35, 0.7, 0.5],
        "blue": [0.35, 0.5, 0.7]
    }
    """
    Search for a particular string value in a PDF file and add comments to it.
    """
    pdfIn = fitz.open(input_file)
    found_matches = 0
    # Iterate throughout the document pages
    for pg,page in enumerate(pdfIn):
        pageID = pg+1
        # If required for specific pages
        if pages:
           if pageID not in pages:
              continue

        # Use the search_for function to find the text
        for word in search_list:
            matched_values = page.search_for(word[0],hit_max=20)
            found_matches += len(matched_values) if matched_values else 0

            #Loop through the matches values
            #item will contain the coordinates of the found text
            for item in matched_values:
                # Highlight found text
                annot = page.add_highlight_annot(item)
                annot.set_colors(stroke=colors[word[2]])

                # Add comment to the found match
                info = annot.info
                info["title"] = comment_title # author
                info["content"] = word[1]
                annot.set_info(info)

                annot.update()

    #Save to output file
    pdfIn.save(output_file,garbage=3,deflate=True)
    pdfIn.close()

    #Process Summary
    summary = {
         "Input File": input_file
       , "Matching Instances": found_matches
       , "Output File": output_file
       , "Comment Title": comment_title
       # , "Comment Info":  comment_info
    }

    # Print process Summary
    print("## Summary ########################################################")
    print("\n".join("{}: {}".format(i, j) for i, j in summary.items()))
    print("###################################################################")

comment_pdf(input_file="report 2021 EN.pdf"
            , search_list=[["human rights","人権","red"], ["global", "グローバル", "green"], ["sustainability", "持続可能性", "blue"]]
            , comment_title="Python Highlighter"
            , output_file="report 2021 EN comments.pdf"
            )