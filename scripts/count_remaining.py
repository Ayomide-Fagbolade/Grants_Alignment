import csv, os
csv.field_size_limit(2**20)
input_csv = r'c:\Users\ayo\Desktop\Grants_Alignment\media_data\allafrica_results_unique.csv'
output_dir = r'c:\Users\ayo\Desktop\Grants_Alignment\media_data\articles_by_year'

processed = set()
for fname in os.listdir(output_dir):
    if not fname.endswith('.csv'): continue
    try:
        with open(os.path.join(output_dir, fname), encoding='utf-8') as f:
            for row in csv.DictReader(f):
                url = row.get('Link','').strip()
                body = row.get('Body_Text','').strip()
                headline = row.get('Headline','N/A').strip()
                if url and body and headline != 'N/A':
                    processed.add(url)
    except: pass

with open(input_csv, encoding='utf-8') as f:
    all_rows = list(csv.DictReader(f))

by_year = {}
for r in all_rows:
    if r['Link'] in processed: continue
    try: yr = r['Link'].split('/stories/')[1][:4]
    except: yr = 'unk'
    by_year[yr] = by_year.get(yr, 0) + 1

total = sum(by_year.values())
for yr in sorted(by_year):
    print(yr + ': ' + str(by_year[yr]))
print('TOTAL: ' + str(total))
