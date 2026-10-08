#!/usr/bin/env python3
"""Fetch publications from PubMed and write data/publications.json."""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

# Author-name search
QUERY = "Coyner AS[Author]"
EXCLUDE_PMIDS = set()  # add PMIDs of papers by other "Coyner AS" here
ME = re.compile(r"^Coyner AS$")
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
OUT = Path(__file__).resolve().parent.parent / "data" / "publications.json"


def get(endpoint, **params):
    url = BASE + endpoint + "?" + urllib.parse.urlencode({**params, "retmode": "json"})
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def main():
    ids = get("esearch.fcgi", db="pubmed", term=QUERY, retmax=500, sort="pub date")["esearchresult"]["idlist"]
    ids = [i for i in ids if i not in EXCLUDE_PMIDS]
    pubs = []
    for start in range(0, len(ids), 100):
        chunk = ids[start:start + 100]
        res = get("esummary.fcgi", db="pubmed", id=",".join(chunk))["result"]
        for pid in chunk:
            r = res.get(pid)
            if not r:
                continue
            doi = next((a["value"] for a in r.get("articleids", []) if a["idtype"] == "doi"), None)
            pubs.append({
                "pmid": pid,
                "title": r["title"].rstrip("."),
                "authors": [a["name"] for a in r.get("authors", [])],
                "journal": r.get("source", ""),
                "date": r.get("sortpubdate", "")[:10],
                "year": (r.get("pubdate") or "")[:4],
                "doi": doi,
            })
        time.sleep(0.4)
    pubs.sort(key=lambda p: (p["year"], p["date"]), reverse=True)  # year shown on the page first, then exact date
    OUT.write_text(json.dumps({"updated": time.strftime("%Y-%m-%d"), "publications": pubs}, indent=1) + "\n")
    print(f"Wrote {len(pubs)} publications")


if __name__ == "__main__":
    main()
