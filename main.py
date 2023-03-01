import fitz, csv

def comment_pdf(input_file:str, list_filename_csv:str, pages:list=None):
    comment_title = "Python Highlighter"
    search_list = read_csv(list_filename_csv)
    # create matches dictionary for output summary
    matches_record = {search[0]: 0 for search in search_list}
    # open pdf
    pdfIn = fitz.open(input_file)
    # Iterate throughout pdf pages
    for pg,page in enumerate(pdfIn):
        pageID = pg+1
        # If required to look in specific pages
        if pages and pageID not in pages:
            continue
        # Use the search_for function to find text
        for search_settings in search_list:
            word, comment, color = search_settings
            matched_values = page.search_for(word)
            if matched_values:
                # Update matches_record
                matches_record[word] += len(matched_values)
                highlight_text(matched_values, page, color, comment_title, comment)
    
    # Save to output file
    output_file = input_file.split(".")[0] + " comments.pdf"
    pdfIn.save(output_file,garbage=3,deflate=True)
    pdfIn.close()
    
    create_summary(input_file, output_file, comment_title, matches_record)

def read_csv(list_filename_csv):
    with open(list_filename_csv, 'r') as csv_data:
        csv_reader = csv.reader(csv_data)
        header = next(csv_reader) # skips the first row
        search_list = [row for row in csv_reader]
    return search_list

def highlight_text(matched_values, page, color, comment_title, comment):
    colors = {
        "red": [0.7, 0.35, 0.5],
        "green": [0.35, 0.7, 0.5],
        "blue": [0.35, 0.5, 0.7]
    }
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
        annot.update(opacity=0.4)

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
    
comment_pdf(input_file="./test_files/final_test_2022.pdf", list_filename_csv="./test_files/sample_glossary.csv")