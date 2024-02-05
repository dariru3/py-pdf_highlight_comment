def debug_search_word_properties(page, search_word):
    """
    Search for a specific word in a PDF page and print its properties,
    especially checking if it's italic.

    Args:
    - page: The page object from PyMuPDF (fitz.Page).
    - search_word: The word to search for (str).
    """
    found = False  # Flag to check if the word was found
    text_instances = page.get_text("dict")["blocks"]
    
    for text_instance in text_instances:
        for line in text_instance.get("lines", []):
            for span in line.get("spans", []):
                # Check if the search_word is in the span's text
                if search_word.lower() in span.get("text", "").lower():
                    found = True
                    # Print the properties of the span containing the search word
                    print(f"Found '{search_word}' with properties:")
                    print(f"  Text: {span.get('text')}")
                    print(f"  Font: {span.get('font')}")
                    print(f"  Size: {span.get('size')}")
                    print(f"  Color: {span.get('color')}")
                    flags = span.get("flags", 0)
                    print(f"  Flags: {flags}")
                    print(f"  Italic: {'Yes' if flags & 2**1 else 'No'}")
                    print(f"  Bold: {'Yes' if flags & 2**4 else 'No'}")
                    # Add more properties as needed
                    
    if not found:
        # print(f"'{search_word}' not found on the page.")
        pass

def debug_search_by_font(page, target_font):
    """
    Search for text with a specific font in a PDF page and print its properties.

    Args:
    - page: The page object from PyMuPDF (fitz.Page).
    - target_font: The font name to search for (str).
    """
    found = False  # Flag to check if the font was found
    text_instances = page.get_text("dict")["blocks"]
    
    for text_instance in text_instances:
        for line in text_instance.get("lines", []):
            for span in line.get("spans", []):
                # Check if the current span's font matches the target font
                if span.get("font", "") == target_font:
                    found = True
                    # Print the properties of the span using the target font
                    print(f"Text with font '{target_font}' found:")
                    print(f"  Text: {span.get('text')}")
                    print(f"  Font: {span.get('font')}")
                    print(f"  Size: {span.get('size')}")
                    print(f"  Color: {span.get('color')}")
                    flags = span.get("flags", 0)
                    print(f"  Flags: {flags}")
                    print(f"  Italic: {'Yes' if flags & 2**1 else 'No'}")
                    print(f"  Bold: {'Yes' if flags & 2**4 else 'No'}")
                    # Add more properties as needed
                    print("-------------------------------")
                    
    if not found:
        # print(f"No text with font '{target_font}' found on the page.")
        pass
