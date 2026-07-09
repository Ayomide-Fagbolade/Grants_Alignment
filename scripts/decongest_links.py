import csv
from collections import defaultdict
import os

input_csv = r'c:\Users\ayo\Desktop\Grants_Alignment\media_data\allafrica_results.csv'
output_csv = r'c:\Users\ayo\Desktop\Grants_Alignment\media_data\allafrica_results_unique.csv'

def decongest():
    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} not found.")
        return
        
    url_to_data = defaultdict(lambda: {'Crops': set(), 'Title': ''})
    
    print("Reading original links...")
    total_rows = 0
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            url = row['Link']
            crop = row['Crop']
            title = row['Title']
            
            if url and crop:
                # Filter by year (2000 to 2024)
                try:
                    parts = url.split('/stories/')
                    if len(parts) > 1:
                        year = int(parts[1][:4])
                        if not (2000 <= year <= 2024):
                            continue
                except ValueError:
                    pass # Keep if year parse fails (unexpected format)
                
                url_to_data[url]['Crops'].add(crop.strip().lower())
                if not url_to_data[url]['Title']:
                    url_to_data[url]['Title'] = title
                
    # Write unique rows
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Crops', 'Title', 'Link'])
        writer.writeheader()
        
        for url, data in url_to_data.items():
            writer.writerow({
                'Crops': ';'.join(sorted(list(data['Crops']))), # Semicolon separated list
                'Title': data['Title'],
                'Link': url
            })
            
    print(f"Total rows processed: {total_rows}")
    print(f"Unique URLs extracted: {len(url_to_data)}")
    print(f"Decongested CSV saved to: {output_csv}")

if __name__ == '__main__':
    decongest()
