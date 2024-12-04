import json
import csv
import os

# Nastavení složek
SOURCE_DIR = ".."  # Zdrojová složka
TARGET_DIR = "out"  # Cílová složka
DEBUG = False
min_index = 10000000000

# Vytvoření cílové složky, pokud neexistuje
os.makedirs(TARGET_DIR, exist_ok=True)


# Funkce pro vytvoření CSV souboru (s připojením dat)
def write_csv(filename, fieldnames, rows, append=False):
    filepath = os.path.join(TARGET_DIR, filename)
    mode = 'a' if append and os.path.exists(filepath) else 'w'
    with open(filepath, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if mode == 'w':  # Při prvním zápisu zapisujeme hlavičky
            writer.writeheader()
        writer.writerows(rows)


def get_index():
    global min_index
    min_index += 1
    return min_index


# Funkce pro zpracování jednoho JSON souboru
def process_json_file(filepath):
    print(f"Working on: {filepath}")
    data = load_json_file(filepath)

    # Příprava dat pro jednotlivé CSV soubory
    papers = []
    authors = []
    venues = []
    fields_of_study = []
    paper_author_rel = []
    paper_venue_rel = []
    paper_reference_rel = []
    paper_fos_rel = []

    for paper in data:
        # Přidání práce do CSV
        papers.append({
            "id": paper.get("id"),
            "title": paper.get("title", ""),
            "year": paper.get("year", ""),
            "n_citation": paper.get("n_citation", ""),
            "page_end": paper.get("page_end", ""),
            "doc_type": paper.get("doc_type", ""),
            "publisher": paper.get("publisher", ""),
            "volume": paper.get("volume", ""),
            "issue": paper.get("issue", ""),
            "doi": paper.get("doi", "")
        })

        # Přidání autorů a jejich vztahů
        for author in paper.get("authors", []):
            authors.append({
                "id": author.get("id"),
                "name": author.get("name", "")
            })
            paper_author_rel.append({
                "paper_id": paper.get("id"),
                "author_id": author.get("id"),
                "org": author.get("org", "")
            })

        # Přidání venue a jeho vztahu
        if "venue" in paper and paper["venue"]:
            new_id = 0
            if paper["venue"].get("id", "") == "":
                new_id = get_index()
            venues.append({
                "id": paper["venue"].get("id", new_id),
                "raw": paper["venue"].get("raw", ""),
                "type": paper["venue"].get("type", "")
            })
            paper_venue_rel.append({
                "paper_id": paper.get("id"),
                "venue_id": paper["venue"].get("id", new_id)
            })

        # Přidání vztahů citací
        for reference in paper.get("references", []):
            paper_reference_rel.append({
                "paper_id": paper.get("id"),
                "reference_id": reference
            })

        # Přidání fields of study a jejich vztahů
        for fos in paper.get("fos", []):
            fields_of_study.append({
                "name": fos.get("name")
            })
            paper_fos_rel.append({
                "paper_id": paper.get("id"),
                "fos_name": fos.get("name"),
                "weight": fos.get("w", "")
            })

    # Odstranění duplicit z dat
    authors = list({(author["id"], author["name"]): author for author in authors}.values())
    venues = list({(venue["id"], venue["raw"], venue["type"]): venue for venue in venues}.values())
    fields_of_study = list({fos["name"]: fos for fos in fields_of_study}.values())

    # Připojení dat do CSV souborů
    write_csv('papers.csv',
              ["id", "title", "year", "n_citation", "page_end", "doc_type", "publisher", "volume", "issue", "doi"],
              papers, append=True)
    write_csv('authors.csv', ["id", "name"], authors, append=True)
    write_csv('venues.csv', ["id", "raw", "type"], venues, append=True)
    write_csv('fields_of_study.csv', ["name"], fields_of_study, append=True)
    write_csv('paper_author_rel.csv', ["paper_id", "author_id", "org"], paper_author_rel, append=True)
    write_csv('paper_venue_rel.csv', ["paper_id", "venue_id"], paper_venue_rel, append=True)
    write_csv('paper_reference_rel.csv', ["paper_id", "reference_id"], paper_reference_rel, append=True)
    write_csv('paper_fos_rel.csv', ["paper_id", "fos_name", "weight"], paper_fos_rel, append=True)
    print(f"Working on {filepath} ended.")


# Načtení dat z JSON souborů
def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


# Postupné zpracování souborů 1.json až 20.json
if not DEBUG:
    for i in range(1, 13):
        filepath = os.path.join(SOURCE_DIR, f"file{i}.json")
        if os.path.exists(filepath):
            process_json_file(filepath)
        else:
            print(f"File {filepath} not exists, skipped.")

# DEBUG
if DEBUG:
    test_file = "dblp.v12"
    filepath = os.path.join(SOURCE_DIR, f"{test_file}.json")
    if os.path.exists(filepath):
        process_json_file(filepath)
    else:
        print(f"File {filepath} not exists.")

print("Parsing is completed.")
