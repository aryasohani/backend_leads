import csv
from typing import List, Dict

def parse_csv_file(file_path) -> List[Dict]:
    leads = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append({
                "name": row.get("name","").strip(),
                "role": row.get("role","").strip(),
                "company": row.get("company","").strip(),
                "industry": row.get("industry","").strip(),
                "location": row.get("location","").strip(),
                "linkedin_bio": row.get("linkedin_bio","").strip()
            })
    return leads
