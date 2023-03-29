import fitz, sys
import csv
import config

def comment_pdf(input_file:str, list_filename_csv:str, pages:list=None):
    comment_name = "LCI-QA"
    search_list = read_csv(list_filename_csv)
    # create matches dictionary for output summary
    matches_record = {search[0]: 0 for search in search_list}
    # open pdf
    pdfIn = fitz.open(input_file)
    # Iterate throughout pdf pages
    for pg,page in enumerate(pdfIn):
        pageID = pg+1
        sys.stdout.write(f"\rScanning page {pageID}...")
        sys.stdout.flush()
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
                highlight_text(matched_values, page, color, comment_name, comment)
    sys.stdout.write("Done!")
    
    # Save to output file
    output_file = input_file.split(".")[0] + " comments.pdf"
    pdfIn.save(output_file,garbage=3,deflate=True)
    pdfIn.close()
    
    create_summary(input_file, output_file, comment_name, matches_record)

def read_csv(list_filename_csv):
    with open(list_filename_csv, 'r') as csv_data:
        csv_reader = csv.reader(csv_data)
        header = next(csv_reader) # skips the first row
        search_list = [[row[0], row[1], row[2]] for row in csv_reader]
    return search_list

def highlight_text(matched_values, page, color, comment_title, comment):
    colors = {
        'blue': [0, 0, 1],
        'light blue': [.22, .9, 1],
        'green': [.42, .85, .16],
        'light green': [.77, .98, .45],
        'yellow': [1, .82, 0],
        'light yellow': [.99, .96, .52],
        'orange': [1, .44, .01],
        'light orange': [1, .75, .62],
        'red': [.90, .13, .22],
        'light red': [1, .50, .62],
        'pink': [.64, .19, .53],
        'light pink': [.98, .53, 1]
    }

    for item in matched_values:
        # Highlight found text
        annot = page.add_highlight_annot(item)
        if color:
            color = color.lower()
            if color in colors:
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
    
comment_pdf(input_file=config.config["source file"], list_filename_csv=config.config["keywords list"])