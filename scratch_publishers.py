import csv, os, sys, glob
csv.field_size_limit(sys.maxsize)

files = glob.glob('c:/Users/ayo/Desktop/Grants_Alignment/media_data/articles_by_year/allafrica_*.csv')
publishers = set()

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # The column is called 'Publisher'
                pub = row.get('Publisher')
                if pub:
                    publishers.add(pub.strip())
    except Exception as e:
        print(f"Error reading {f}: {e}")

print("---BEGIN PUBLISHERS---")
for p in sorted(publishers):
    print(p)
print("---END PUBLISHERS---")
