
import csv
import os

filepath = "data/table-data (2).csv"

if not os.path.exists(filepath):
    print(f"File not found at {os.path.abspath(filepath)}")
else:
    print(f"Analyzing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"Total characters: {len(content)}")
        q_count = content.count('\"')
        print(f"Total quote characters: {q_count}")
        
    try:
        with open(filepath, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            print(f"Headers: {headers}")
            count = 0
            for row in reader:
                count += 1
            print(f"Successfully counted {count} data rows with csv.reader")
    except Exception as e:
        print(f"Error reading with csv.reader: {e}")
