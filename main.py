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
        matched_values = page.search_for(search_text,hit_max=20)
        found_matches += len(matched_values) if matched_values else 0

        #Loop through the matches values
        #item will contain the coordinates of the found text
        for item in matched_values:
            # Enclose the found text with a bounding box
            annot = page.add_rect_annot(item)
            annot.set_border({"dashes":[2],"width":0.2})
            annot.set_colors({"stroke":BLUE_COLOR})

            # Add comment to the found match
            info = comment_title
            # info = annot.info
            # info["title"]   = comment_title
            # info["content"] = comment_info
            #info["subject"] = "Educative subject"
            annot.set_name(info)

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

comment_pdf("muji report 2021 EN.pdf"
            , "human rights"
            , "human rights"
            , "人権"
            , "muji report 2021 EN comments.pdf"
            )