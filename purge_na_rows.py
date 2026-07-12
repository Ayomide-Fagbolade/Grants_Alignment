import csv
import sys
import os
import glob
import shutil

csv.field_size_limit(sys.maxsize)

output_dir = r'c:\Users\ayo\Desktop\Grants_Alignment\media_data\articles_by_year'
files = sorted(glob.glob(os.path.join(output_dir, 'allafrica_*.csv')))

total_kept = 0
total_purged = 0

print(f"{'Year':<6} {'Kept':>8} {'Purged':>8}")
print("-" * 26)

for f in files:
    year = os.path.basename(f).replace('allafrica_', '').replace('.csv', '')
    kept_rows = []
    purged = 0

    try:
        with open(f, 'r', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            fieldnames = reader.fieldnames
            for row in reader:
                pub_url = row.get('Publisher_URL', '').strip()
                src_url = row.get('Source_URL', '').strip()
                if pub_url == 'N/A' and src_url == 'N/A':
                    purged += 1
                else:
                    kept_rows.append(row)
    except Exception as e:
        print(f"Error reading {f}: {e}")
        continue

    # Write cleaned file back
    try:
        with open(f, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(kept_rows)
    except Exception as e:
        print(f"Error writing {f}: {e}")
        continue

    total_kept += len(kept_rows)
    total_purged += purged
    print(f"{year:<6} {len(kept_rows):>8,} {purged:>8,}")

print("-" * 26)
print(f"{'TOTAL':<6} {total_kept:>8,} {total_purged:>8,}")
print(f"\nRows purged (need re-scraping): {total_purged:,}")
