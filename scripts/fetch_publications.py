#!/usr/bin/env python3
"""
Fetch publications from Semantic Scholar API and save to JSON file.

Usage:
    python scripts/fetch_publications.py

Requirements:
    pip install requests
"""

import json
import os
import datetime
import sys
import time
import requests

SEMANTIC_SCHOLAR_AUTHOR_ID = '33665114'
BASE_URL = 'https://api.semanticscholar.org/graph/v1'
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'assets', 'data', 'publications.json'
)


def get(url, params=None, retries=3):
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=30)
            if r.status_code == 429:
                wait = 10 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    return None


def fetch_author():
    print(f"Fetching author {SEMANTIC_SCHOLAR_AUTHOR_ID}...")
    data = get(
        f"{BASE_URL}/author/{SEMANTIC_SCHOLAR_AUTHOR_ID}",
        params={'fields': 'name,citationCount,hIndex,paperCount'}
    )
    print(f"  Name: {data['name']}")
    print(f"  Citations: {data.get('citationCount', 0)}  h-index: {data.get('hIndex', 0)}")
    return data


def fetch_papers():
    print("Fetching papers...")
    papers = []
    offset = 0
    limit = 100
    while True:
        data = get(
            f"{BASE_URL}/author/{SEMANTIC_SCHOLAR_AUTHOR_ID}/papers",
            params={
                'fields': 'title,authors,year,venue,citationCount,externalIds,openAccessPdf,publicationTypes',
                'limit': limit,
                'offset': offset,
            }
        )
        batch = data.get('data', [])
        papers.extend(batch)
        print(f"  Fetched {len(papers)} papers so far...")
        if not data.get('next'):
            break
        offset += limit
        time.sleep(0.5)
    return papers


def make_pub(paper):
    external = paper.get('externalIds') or {}
    url = ''
    if external.get('DOI'):
        url = f"https://doi.org/{external['DOI']}"
    elif external.get('ArXiv'):
        url = f"https://arxiv.org/abs/{external['ArXiv']}"
    elif external.get('PubMed'):
        url = f"https://pubmed.ncbi.nlm.nih.gov/{external['PubMed']}/"

    eprint_url = ''
    if paper.get('openAccessPdf'):
        eprint_url = paper['openAccessPdf'].get('url', '')

    authors = ' and '.join(
        a.get('name', '') for a in (paper.get('authors') or [])
    )

    return {
        'title': paper.get('title', 'Untitled'),
        'authors': authors,
        'venue': paper.get('venue') or 'Unknown Venue',
        'year': paper.get('year') or '',
        'abstract': '',
        'citations': paper.get('citationCount') or 0,
        'url': url,
        'eprint_url': eprint_url,
        'author_id': [],
        'pub_type': 'article',
        'publication_types': paper.get('publicationTypes') or [],
        'external_ids': external,
    }


def categorize(publications):
    categories = {'journals': [], 'conferences': [], 'patents': [], 'thesis': [], 'other': []}

    for pub in publications:
        types = [t.lower() for t in pub.get('publication_types', [])]
        title_lower = pub['title'].lower()
        venue_lower = pub['venue'].lower()
        url = pub.get('url', '').lower()

        if 'patent' in types or 'patent' in url or 'patent' in venue_lower:
            categories['patents'].append(pub)
        elif any(k in title_lower for k in ['thesis', 'dissertation']):
            categories['thesis'].append(pub)
        elif 'journalarticle' in types or any(k in venue_lower for k in [
            'journal', 'transactions', 'access', 'letters', 'magazine'
        ]):
            categories['journals'].append(pub)
        elif 'conference' in types or any(k in venue_lower for k in [
            'conference', 'proceedings', 'workshop', 'symposium'
        ]):
            categories['conferences'].append(pub)
        elif pub['venue'] and pub['venue'] != 'Unknown Venue':
            categories['conferences'].append(pub)
        else:
            categories['other'].append(pub)

    for cat in categories:
        categories[cat].sort(key=lambda x: int(x['year']) if x['year'] else 0, reverse=True)

    return categories


def main():
    author = fetch_author()
    papers = fetch_papers()

    publications = [make_pub(p) for p in papers]
    print(f"\nProcessed {len(publications)} publications")

    categorized = categorize(publications)
    for cat, pubs in categorized.items():
        print(f"  {cat}: {len(pubs)}")

    metrics = {
        'total_citations': author.get('citationCount', 0),
        'total_citations_5y': 0,
        'h_index': author.get('hIndex', 0),
        'h_index_5y': 0,
        'i10_index': sum(1 for p in publications if p['citations'] >= 10),
        'i10_index_5y': 0,
        'five_years_ago': datetime.datetime.now().year - 5,
    }

    output = {
        'last_updated': datetime.datetime.now().isoformat(),
        'total_count': len(publications),
        'metrics': metrics,
        'categories': categorized,
        'all_publications': publications,
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to {OUTPUT_FILE}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
