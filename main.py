def comment_pdf(input_file:str
              , search_text:str
              , comment_title:str
              , comment_info:str
              , output_file:str
              , pages:list=None
              ):
    import fitz
    """
    Search for a particular string value in a PDF file and add comments to it.
    """
    BLUE_COLOR = (0,0,1)
    pdfIn = fitz.open(input_file)
    found_matches = 0
    # Iterate throughout the document pages
    for pg,page in enumerate(pdfIn):
        pageID = pg+1
        # If required for specific pages
        if pages:
           if pageID not in pages:
              continue

        # Use the search for function to find the text
        matched_values = page.searchFor(search_text,hit_max=20)
        found_matches += len(matched_values) if matched_values else 0

        #Loop through the matches values
        #item will contain the coordinates of the found text
        for item in matched_values:
            # Enclose the found text with a bounding box
            annot = page.addRectAnnot(item)
            annot.setBorder({"dashes":[2],"width":0.2})
            annot.setColors({"stroke":BLUE_COLOR})

            # Add comment to the found match
            info = annot.info
            info["title"]   = comment_title
            info["content"] = comment_info
            #info["subject"] = "Educative subject"
            annot.setInfo(info)

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
       , "Comment Info":  comment_info
    }

    # Print process Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")