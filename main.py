def comment_pdf(input_file:str, list_filename_csv:str, pages:list=None):
    import fitz

    comment_title = "Python Highlighter"
    colors = {
        "red": [0.7, 0.35, 0.5],
        "green": [0.35, 0.7, 0.5],
        "blue": [0.35, 0.5, 0.7]
    }
    search_list = read_csv(list_filename_csv)
    # create matches dictionary for output summary
    matches_record = {search[0]: 0 for search in search_list}

    pdfIn = fitz.open(input_file)
    # Iterate throughout the document pages
    for pg,page in enumerate(pdfIn):
        pageID = pg+1
        # If required for specific pages
        if pages and pageID not in pages:
            continue

        # Use the search_for function to find the text
        for search_settings in search_list:
            word, comment, color = search_settings
            matched_values = page.search_for(word,hit_max=20)
            if matched_values:
                matches_record[word] += len(matched_values)
                #Loop through the matched values; item will contain the coordinates of the found text
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
    
    # Save to output file
    output_file = input_file.split(".")[0] + " comments.pdf"
    pdfIn.save(output_file,garbage=3,deflate=True)
    pdfIn.close()
    
    create_summary(input_file, output_file, comment_title, matches_record)

def read_csv(csv_filename):
    import csv
    with open(csv_filename, 'r') as csv_data:
        csv_reader = csv.reader(csv_data)
        header = next(csv_reader) # skips the first row
        search_list = [row for row in csv_reader]
    return search_list

def create_summary(input_file, output_file, comment_title, matches_record):
    summary = {
         "Input File": input_file
       , "Output File": output_file
       , "Comment Title": comment_title
       , "Matching Instances": "\n" + "\n".join("{}: {}".format(word, count) for word, count in matches_record.items())
    }
    # Export Process Summary
    with open('summary.txt', 'w') as summary_txt:
        summary_txt.write("\n".join("{}: {}".format(i, j) for i, j in summary.items()))
    

comment_pdf(input_file="report 2021 EN.pdf", list_filename_csv="scan_list.csv")