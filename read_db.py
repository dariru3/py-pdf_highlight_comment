import shelve

with shelve.open('input_folder/scanned_files') as db:
    for key in db:
        print(f"{key}: {db[key]}")
