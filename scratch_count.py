import csv, os, sys, glob
csv.field_size_limit(sys.maxsize)

input_csv = 'c:/Users/ayo/Desktop/Grants_Alignment/media_data/allafrica_results_unique.csv'
expected = {}

try:
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row['Link']
            parts = url.split('/stories/')
            if len(parts) > 1:
                year = parts[1][:4]
                expected[year] = expected.get(year, 0) + 1
except Exception as e:
    print(f"Error reading unique results: {e}")

files = sorted(glob.glob('c:/Users/ayo/Desktop/Grants_Alignment/media_data/articles_by_year/allafrica_*.csv'))
fetched = {}

for f in files:
    year = os.path.basename(f).replace('allafrica_','').replace('.csv','')
    count = 0
    try:
        with open(f, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for _ in reader:
                count += 1
    except Exception as e:
        print(f"Error reading {f}: {e}")
    fetched[year] = count

print("Year | Unfetched (Expected - Fetched)")
print("-" * 40)
for y in sorted(expected.keys()):
    if '2000' <= y <= '2024':
        e = expected[y]
        f_count = fetched.get(y, 0)
        u = e - f_count
        print(f"{y}: {u} (Expected: {e}, Fetched: {f_count})")
